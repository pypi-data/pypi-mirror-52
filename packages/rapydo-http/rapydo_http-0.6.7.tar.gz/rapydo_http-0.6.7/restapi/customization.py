# -*- coding: utf-8 -*-

"""
Customization based on configuration 'blueprint' files
"""

import os
import re
import glob
from utilities import CONF_PATH
from utilities import BACKEND_PACKAGE, CUSTOM_PACKAGE, SWAGGER_MODELS_FILE

# from utilities import PROJECT_CONF_FILENAME, DEFAULT_FILENAME, UTILS_PKGNAME
from utilities import helpers
from utilities import configuration as conf
from restapi.confs import API_URL, BASE_URLS
from utilities.meta import Meta
from utilities.myyaml import YAML_EXT, load_yaml_file
from restapi.services.detect import detector
from restapi.attributes import EndpointElements, ExtraAttributes
from restapi.swagger import BeSwagger

from utilities.logs import get_logger

log = get_logger(__name__)

CONF_FOLDERS = detector.load_group(label='project_confs')


########################
# Customization on the table
########################


class Customizer(object):
    """
    Customize your BACKEND:
    Read all of available configurations and definitions.
    """

    def __init__(self, testing=False, production=False, init=False):

        # Input
        self._testing = testing
        self._production = production
        self._initiliazing = init

        # Some initialization
        self._endpoints = []
        self._definitions = {}
        self._configurations = {}
        self._query_params = {}
        self._schemas_map = {}
        self._meta = Meta()

        # Do things
        self.read_configuration()

        if not self._initiliazing:
            self.do_schema()
            self.find_endpoints()
            self.do_swagger()

    def read_configuration(self):
        ##################
        # Reading configuration

        confs_path = helpers.current_dir(CONF_PATH)

        if 'defaults_path' in CONF_FOLDERS:
            defaults_path = CONF_FOLDERS['defaults_path']
        else:
            defaults_path = confs_path

        if 'base_path' in CONF_FOLDERS:
            base_path = CONF_FOLDERS['base_path']
        else:
            base_path = confs_path

        if 'projects_path' in CONF_FOLDERS:
            projects_path = CONF_FOLDERS['projects_path']
        else:
            projects_path = confs_path

        if 'submodules_path' in CONF_FOLDERS:
            submodules_path = CONF_FOLDERS['submodules_path']
        else:
            submodules_path = confs_path

        self._configurations, self._extended_project, self._extended_path = conf.read(
            default_file_path=defaults_path,
            base_project_path=base_path,
            projects_path=projects_path,
            submodules_path=submodules_path,
            from_container=True,
            do_exit=True,
        )

    def do_schema(self):
        """ Schemas exposing, if requested """

        name = '%s.%s.%s' % (BACKEND_PACKAGE, 'rest', 'schema')
        module = Meta.get_module_from_string(
            name, exit_if_not_found=True, exit_on_fail=True
        )
        schema_class = getattr(module, 'RecoverSchema')

        self._schema_endpoint = EndpointElements(
            cls=schema_class,
            exists=True,
            custom={
                'methods': {
                    'get': ExtraAttributes(auth=None),
                    # WHY DOES POST REQUEST AUTHENTICATION
                    # 'post': ExtraAttributes(auth=None)
                }
            },
            methods={},
        )

        # TODO: find a way to map authentication
        # as in the original endpoint for the schema 'get' method

        # TODO: find a way to publish on swagger the schema
        # if endpoint is enabled to publish and the developer asks for it

    def find_endpoints(self):

        ##################
        # Walk swagger directories looking for endpoints

        swagger_folders = []
        # base swagger dir (rapydo/http-api)
        swagger_folders.append(
            {
                'path': helpers.script_abspath(__file__),
                'isbase': True
            }
        )

        # swagger dir from extended project, if any
        if self._extended_project is not None:

            swagger_folders.append(
                {
                    'path': helpers.current_dir(self._extended_project),
                    'isbase': False
                }
            )

        # custom swagger dir
        swagger_folders.append(
            {
                'path': helpers.current_dir(CUSTOM_PACKAGE),
                'isbase': False
            }
        )

        simple_override_check = {}
        for swag_folder in swagger_folders:

            base_dir = swag_folder.get('path')
            isbase = swag_folder.get('isbase')

            swagger_dir = os.path.join(base_dir, 'swagger')
            log.verbose("Swagger dir: %s" % swagger_dir)

            for ep in os.listdir(swagger_dir):

                if ep in simple_override_check:
                    log.warning(
                        "%s already loaded from %s", ep, simple_override_check.get(ep)
                    )
                    continue
                simple_override_check[ep] = base_dir

                swagger_endpoint_dir = os.path.join(swagger_dir, ep)

                if os.path.isfile(swagger_endpoint_dir):
                    exception = '%s.yaml' % SWAGGER_MODELS_FILE
                    if not swagger_endpoint_dir.endswith('/' + exception):
                        log.debug(
                            "Found a file instead of a folder: %s", swagger_endpoint_dir
                        )
                    continue

                base_module = helpers.last_dir(base_dir)
                from utilities import ENDPOINTS_CODE_DIR

                if isbase:
                    apiclass_module = '%s.%s' % (base_module, 'resources')
                else:
                    apiclass_module = '%s.%s' % (base_module, ENDPOINTS_CODE_DIR)

                current = self.lookup(ep, apiclass_module, swagger_endpoint_dir, isbase)

                if current is not None and current.exists:
                    # Add endpoint to REST mapping
                    self._endpoints.append(current)

    def do_swagger(self):

        # SWAGGER read endpoints definition
        swag = BeSwagger(self._endpoints, self)
        swag_dict = swag.swaggerish()

        # TODO: update internal endpoints from swagger
        self._endpoints = swag._endpoints[:]

        # SWAGGER validation
        if not swag.validation(swag_dict):
            log.critical_exit("Current swagger definition is invalid")

        self._definitions = swag_dict

    def lookup(self, endpoint, apiclass_module, swagger_endpoint_dir, isbase):

        log.verbose("Found endpoint dir: '%s'" % endpoint)

        if os.path.exists(os.path.join(swagger_endpoint_dir, 'SKIP')):
            log.info("Skipping: %s", endpoint)
            return None

        # Find yaml files
        conf = None
        yaml_files = {}
        yaml_listing = os.path.join(swagger_endpoint_dir, "*.%s" % YAML_EXT)

        for file in glob.glob(yaml_listing):
            if file.endswith('specs.%s' % YAML_EXT):
                # load configuration and find file and class
                conf = load_yaml_file(file)
            else:
                # add file to be loaded from swagger extension
                p = re.compile(r'\/([^\.\/]+)\.' + YAML_EXT + '$')
                match = p.search(file)
                method = match.groups()[0]
                yaml_files[method] = file

        if len(yaml_files) < 1:
            raise Exception("%s: no methods defined in any YAML" % endpoint)
        if conf is None or 'class' not in conf:
            raise ValueError("No 'class' defined for '%s'" % endpoint)

        current = self.load_endpoint(endpoint, apiclass_module, conf, isbase)
        current.methods = yaml_files
        return current

    # def read_complex_config(self, configfile):
    #     """ A more complex configuration is available in JSON format """
    #     content = {}
    #     with open(configfile) as fp:
    #         content = json.load(fp)
    #     return content

    def load_endpoint(self, default_uri, apiclass_module, conf, isbase):

        endpoint = EndpointElements(custom={})

        # Load the endpoint class defined in the YAML file
        file_name = conf.pop('file', default_uri)
        class_name = conf.pop('class')
        name = '%s.%s' % (apiclass_module, file_name)
        module = Meta.get_module_from_string(name, exit_on_fail=False)

        # Error if unable to find the module in python
        if module is None:
            log.critical_exit("Could not find module %s (in %s)" % (name, file_name))

        # Check for dependecies and skip if missing
        for var in conf.pop('depends_on', []):

            negate = ''
            pieces = var.strip().split(' ')
            pieces_num = len(pieces)
            if pieces_num == 1:
                dependency = pieces.pop()
            elif pieces_num == 2:
                negate, dependency = pieces
            else:
                log.exit('Wrong parameter: %s', var)

            check = detector.get_bool_from_os(dependency)
            # Enable the possibility to depend on not having a variable
            if negate.lower() == 'not':
                check = not check

            # Skip if not meeting the requirements of the dependency
            if not check:
                if not self._testing:
                    log.debug("Skip '%s': unmet %s", default_uri, dependency)
                return endpoint

        # Get the class from the module
        endpoint.cls = self._meta.get_class_from_string(class_name, module)
        if endpoint.cls is None:
            log.critical("Could not extract python class '%s'", class_name)
            return endpoint
        else:
            endpoint.exists = True

        # Is this a base or a custom class?
        endpoint.isbase = isbase

        # DEPRECATED
        # endpoint.instance = endpoint.cls()

        # Global tags
        # to be applied to all methods
        endpoint.tags = conf.pop('labels', [])

        # base URI
        base = conf.pop('baseuri', API_URL)
        if base not in BASE_URLS:
            log.warning("Invalid base %s", base)
            base = API_URL
        base = base.strip('/')

        #####################
        # MAPPING
        schema = conf.pop('schema', {})
        mappings = conf.pop('mapping', [])
        if len(mappings) < 1:
            raise KeyError("Missing 'mapping' section")

        endpoint.uris = {}  # attrs python lib bug?
        endpoint.custom['schema'] = {
            'expose': schema.get('expose', False),
            'publish': {},
        }
        for label, uri in mappings.items():

            # BUILD URI
            total_uri = '/%s%s' % (base, uri)
            endpoint.uris[label] = total_uri

            # If SCHEMA requested create
            if endpoint.custom['schema']['expose']:

                schema_uri = '%s%s%s' % (API_URL, '/schemas', uri)

                p = hex(id(endpoint.cls))
                self._schema_endpoint.uris[label + p] = schema_uri

                endpoint.custom['schema']['publish'][label] = schema.get(
                    'publish', False
                )

                self._schemas_map[schema_uri] = total_uri

        # Description for path parameters
        endpoint.ids = conf.pop('ids', {})

        # Check if something strange is still in configuration
        if len(conf) > 0:
            raise KeyError("Unwanted keys: %s" % list(conf.keys()))

        return endpoint
