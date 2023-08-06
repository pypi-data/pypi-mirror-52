# -*- coding: utf-8 -*-

import os.path
import time
from distutils.dir_util import copy_tree
import shutil
from glom import glom
from collections import OrderedDict
from datetime import datetime
from distutils.version import LooseVersion
from utilities import path
from utilities import checks
from utilities import helpers
from utilities import basher
from utilities import PROJECT_DIR
from utilities import CONTAINERS_YAML_DIRNAME
from utilities import configuration
from utilities import EXTENDED_PROJECT_DISABLED
from utilities.globals import mem
from utilities.time import date_from_string, get_online_utc_time
from controller import __version__
from controller import project
from controller import gitter
from controller import COMPOSE_ENVIRONMENT_FILE, PLACEHOLDER
from controller import SUBMODULES_DIR, RAPYDO_CONFS, RAPYDO_GITHUB, PROJECTRC
from controller import RAPYDO_TEMPLATE
from controller.builds import locate_builds
from controller.dockerizing import Dock
from controller.compose import Compose
from controller.configuration import load_yaml_file, SHORT_YAML_EXT
from controller.scaffold import EndpointScaffold
from controller.configuration import read_yamls
from utilities.logs import get_logger, suppress_stdout

log = get_logger(__name__)

# FIXME: move somewhere
STATUS_RELEASED = "released"
STATUS_DISCONTINUED = "discontinued"
STATUS_DEVELOPING = "developing"

ANGULARJS = 'angularjs'
ANGULAR = 'angular'
REACT = 'react'

ROOT_UID = 0
BASE_UID = 990


class Application(object):

    """
    ## Main application class

    It handles all implemented commands,
    which were defined in `argparser.yaml`
    """

    def __init__(self, arguments):
        self.arguments = arguments
        self.current_args = self.arguments.current_args
        self.reserved_project_names = self.get_reserved_project_names()
        self.vars_to_services_mapping = self.get_vars_to_services_mapping()

        create = self.current_args.get('action', 'unknown') == 'create'

        if not create:
            first_level_error = self.inspect_main_folder()
            cwd = os.getcwd()
            if first_level_error is not None:
                num_iterations = 0
                while cwd != '/' and num_iterations < 10:
                    num_iterations += 1
                    # TODO: use utils.path here
                    os.chdir("..")
                    cwd = os.getcwd()
                    if self.inspect_main_folder() is None:
                        log.warning(
                            "You are not in the rapydo main folder, "
                            + "changing working dir to %s",
                            cwd,
                        )
                        first_level_error = None
                        break
            if first_level_error is not None:
                if self.current_args.get('action') == 'version':
                    return self._version()
                else:
                    log.exit(first_level_error)

        # Initial inspection
        self.get_args()
        if not self.print_version:
            log.info("You are using rapydo version %s", __version__)
        self.check_installed_software()

        if self.create:

            self._create(
                self.current_args.get("name"), self.current_args.get("template")
            )
            return

        self.check_projects()
        self.preliminary_version_check()
        if not self.install or self.local_install:
            self.git_submodules(confs_only=True)
            self.read_specs()  # read project configuration
        if not self.install and not self.print_version:
            self.verify_rapydo_version()
            self.inspect_project_folder()

        # get user launching rapydo commands
        self.current_uid = basher.current_os_uid()
        if self.install or self.print_version:
            skip_check_perm = True
        elif self.current_uid == ROOT_UID:
            self.current_uid = BASE_UID
            self.current_os_user = 'privileged'
            skip_check_perm = True
            log.warning("Current user is 'root'")
        else:
            self.current_os_user = basher.current_os_user()
            skip_check_perm = not self.current_args.get('check_permissions', False)
            log.debug(
                "Current user: %s (UID: %d)" % (self.current_os_user, self.current_uid)
            )

        if not skip_check_perm:
            self.inspect_permissions()

        # Generate and get the extra arguments in case of a custom command
        if self.action == 'custom':
            self.custom_parse_args()
        else:
            try:
                argname = next(iter(self.arguments.remaining_args))
            except StopIteration:
                pass
            else:
                log.exit("Unknown argument:'%s'.\nUse --help to list options", argname)

        # Verify if we implemented the requested command
        function = "_%s" % self.action.replace("-", "_")
        func = getattr(self, function, None)
        if func is None:
            log.exit(
                "Command not yet implemented: %s (expected function: %s)"
                % (self.action, function)
            )

        if not self.install or self.local_install:
            self.git_submodules(confs_only=False)

        if not self.install and not self.print_version:
            # Detect if heavy ops are allowed
            git_checks = False
            git_checks = self.update or self.check
            if self.check and self.current_args.get('skip_heavy_git_ops', False):
                git_checks = False

            if git_checks:
                self.git_checks()  # NOTE: this might be an heavy operation
            else:
                log.verbose("Skipping heavy operations")

            self.make_env()

            # Compose services and variables
            self.read_composers()
            self.check_placeholders()

            # Build or check template containers images
            self.build_dependencies()

            # Install or check frontend libraries (onlye if frontend is enabled)
            self.frontend_libs()

        # Final step, launch the command

        if self.tested_connection:
            online_time = get_online_utc_time()
            sec_diff = (datetime.utcnow() - online_time).total_seconds()

            major_diff = abs(sec_diff) >= 300
            if major_diff:
                minor_diff = False
            else:
                minor_diff = abs(sec_diff) >= 60

            if major_diff:
                log.error("Date misconfiguration on the host.")
            elif minor_diff:
                log.warning("Date misconfiguration on the host.")

            if major_diff or minor_diff:
                current_date = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                tz_offset = time.timezone / -3600
                log.info("Current date: %s UTC", current_date)
                log.info("Expected: %s UTC", online_time)
                log.info("Current timezone: %s (offset = %dh)", time.tzname, tz_offset)

            if major_diff:
                tips = "To manually set the date: "
                tips += "sudo date --set \"%s\"" % online_time.strftime(
                    '%d %b %Y %H:%M:%S'
                )
                log.exit("Unable to continue, please fix the host date\n%s", tips)

        func()

    def get_args(self):

        # Action
        self.action = self.current_args.get('action')
        mem.action = self.action
        if self.action is None:
            log.exit("Internal misconfiguration")

        # Action aliases
        self.initialize = self.action == 'init'
        self.update = self.action == 'update'
        self.start = self.action == 'start'
        # self.upgrade = self.action == 'upgrade'
        self.check = self.action == 'check'
        self.install = self.action == 'install'
        self.print_version = self.action == 'version'
        self.local_install = self.install and self.current_args.get('editable')
        self.pull = self.action == 'pull'
        self.create = self.action == 'create'

        # Others
        self.tested_connection = False
        self.project = self.current_args.get('project')
        self.rapydo_version = None  # To be retrieved from projet_configuration
        self.project_title = None  # To be retrieved from projet_configuration
        self.project_description = None  # To be retrieved from projet_configuration
        self.version = None
        # self.releases = {}
        self.gits = {}

        if self.project is not None:
            if "_" in self.project:
                suggest = "\nPlease consider to rename %s into %s" % (
                    self.project,
                    self.project.replace("_", ""),
                )
                log.exit("Wrong project name, _ is not a valid character.%s" % suggest)

            if self.project in self.reserved_project_names:
                log.exit(
                    "You selected a reserved name, invalid project name: %s"
                    % self.project
                )

        self.development = self.current_args.get('development')

    def check_projects(self):

        try:
            projects = helpers.list_path(PROJECT_DIR)
        except FileNotFoundError:
            log.exit("Could not access the dir '%s'" % PROJECT_DIR)

        if self.project is None:
            prj_num = len(projects)

            if prj_num == 0:
                log.exit("No project found (%s folder is empty?)" % PROJECT_DIR)
            elif prj_num > 1:
                hint = "Hint: create a %s file to save default options" % PROJECTRC
                log.exit(
                    "Please select the --project option on one "
                    + "of the following:\n\n %s\n\n%s\n",
                    projects,
                    hint,
                )
            else:
                # make it the default
                self.project = projects.pop()
                self.current_args['project'] = self.project
        else:
            if self.project not in projects:
                log.exit(
                    "Wrong project '%s'.\n" % self.project
                    + "Select one of the following:\n\n %s\n" % projects
                )

        log.checked("Selected project: %s" % self.project)

    def check_installed_software(self):

        # Check if docker is installed
        self.check_program('docker', min_version="1.13")

        # Check for CVE-2019-5736 vulnerability
        # Checking version of docker server, since docker client is not affected
        # and the two versions can differ
        v = checks.executable(
            executable='docker',
            option=["version", "--format", "'{{.Server.Version}}'"],
            parse_ver=True,
        )

        safe_version = "18.09.2"
        if LooseVersion(safe_version) > LooseVersion(v):
            log.critical(
                """Your docker version is vulnerable to CVE-2019-5736

***************************************************************************************
Your docker installation (version %s) is affected by a critical vulnerability
that allows specially-crafted containers to gain administrative privileges on the host.
For details please visit: https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2019-5736
***************************************************************************************
To fix this issue, please update docker to version %s+
            """,
                v,
                safe_version,
            )

        # Use it
        self.docker = Dock()

        # Check docker-compose version
        # self.check_python_package('pip', max_version="10.0.1")
        self.check_python_package('compose', min_version="1.18")
        # self.check_python_package('docker', min_version="2.4.2")
        self.check_python_package('docker', min_version="2.6.1")
        self.check_python_package('requests', min_version="2.6.1")
        self.check_python_package(
            'utilities', min_version=__version__, max_version=__version__
        )

        # Check if git is installed
        self.check_program('git')  # , max_version='2.14.3')

    @staticmethod
    def check_program(program, min_version=None, max_version=None):
        found_version = checks.executable(executable=program)
        if found_version is None:

            hints = ""

            if program == "docker":
                hints = "To install docker visit: https://get.docker.com"

            if len(hints) > 0:
                hints = "\n\n%s" % hints

            log.exit("Missing requirement: '%s' not found.%s" % (program, hints))
        if min_version is not None:
            if LooseVersion(min_version) > LooseVersion(found_version):
                version_error = "Minimum supported version for %s is %s" % (
                    program,
                    min_version,
                )
                version_error += ", found %s " % (found_version)
                log.exit(version_error)

        if max_version is not None:
            if LooseVersion(max_version) < LooseVersion(found_version):
                version_error = "Maximum supported version for %s is %s" % (
                    program,
                    max_version,
                )
                version_error += ", found %s " % (found_version)
                log.exit(version_error)

        log.checked("%s version: %s" % (program, found_version))

    @staticmethod
    def check_python_package(package, min_version=None, max_version=None):

        found_version = checks.package(package)
        if found_version is None:
            log.exit("Could not find the following python package: %s" % package)

        if min_version is not None:
            if LooseVersion(min_version) > LooseVersion(found_version):
                version_error = "Minimum supported version for %s is %s" % (
                    package,
                    min_version,
                )
                version_error += ", found %s " % (found_version)
                log.exit(version_error)

        if max_version is not None:
            if LooseVersion(max_version) < LooseVersion(found_version):
                version_error = "Maximum supported version for %s is %s" % (
                    package,
                    max_version,
                )
                version_error += ", found %s " % (found_version)
                log.exit(version_error)

        log.checked("%s version: %s" % (package, found_version))

    @staticmethod
    def inspect_main_folder():
        """
        Rapydo commands only works on rapydo projects, we want to ensure that
        the current folder have a rapydo-like structure. These checks are based
        on file existence. Further checks are performed in the following steps
        """

        if gitter.get_local(".") is None:
            return """You are not in a git repository
\nPlease note that this command only works from inside a rapydo-like repository
Verify that you are in the right folder, now you are in: %s
                """ % (
                os.getcwd()
            )

        required_files = [PROJECT_DIR, 'data', 'projects', 'submodules']

        for fname in required_files:
            if not os.path.exists(fname):

                if fname == 'data':
                    extra = """
\nPlease also note that the data dir is not automatically created,
if you are in the right repository consider to create it by hand
"""
                else:
                    extra = ""

                return """File or folder not found %s
\nPlease note that this command only works from inside a rapydo-like repository
Verify that you are in the right folder, now you are in: %s%s
                    """ % (
                    fname,
                    os.getcwd(),
                    extra,
                )

        return None

    def inspect_project_folder(self):

        required_files = [
            'confs',
            'backend',
            'backend/apis',
            'backend/models',
            'backend/swagger',
            'backend/tests',
        ]
        obsolete_files = ['backend/__main__.py']

        if self.frontend is not None:
            required_files.extend(
                [
                    'frontend',
                    'frontend/package.json',
                    'frontend/custom.ts',
                    'frontend/app',
                    'frontend/app/custom.project.options.ts',
                    'frontend/app/custom.module.ts',
                    'frontend/app/custom.navbar.ts',
                    'frontend/app/custom.navbar.links.html',
                    'frontend/app/custom.navbar.brand.html',
                    'frontend/css/style.css',
                ]
            )

            obsolete_files.extend(
                [
                    'frontend/app/app.routes.ts',
                    'frontend/app/app.declarations.ts',
                    'frontend/app/app.providers.ts',
                    'frontend/app/app.imports.ts',
                    'frontend/app/app.custom.navbar.ts',
                    'frontend/app/app.entryComponents.ts',
                    'frontend/app/app.home.ts',
                    'frontend/app/app.home.html',
                    'frontend/app/custom.declarations.ts',
                    'frontend/app/custom.routes.ts',
                ]
            )

            if self.frontend == ANGULARJS:
                required_files.extend(
                    [
                        'frontend/js',
                        'frontend/js/app.js',
                        'frontend/js/routing.extra.js',
                        'frontend/templates',
                    ]
                )

        for fname in required_files:
            fpath = os.path.join(PROJECT_DIR, self.project, fname)
            if not os.path.exists(fpath):
                log.exit(
                    """Project %s is invalid: file or folder not found %s
                    """
                    % (self.project, fpath)
                )

        for fname in obsolete_files:
            fpath = os.path.join(PROJECT_DIR, self.project, fname)
            if os.path.exists(fpath):
                log.exit(
                    "Project %s contains an obsolete file or folder: %s",
                    self.project,
                    fpath,
                )

    def check_permissions(self, path):

        # if os.path.islink(path):
        #     log.warning("Skipping checks on %s (symbolic link)", path)
        #     return True

        if path.endswith("/node_modules"):
            return False

        if not basher.path_is_readable(path):
            if os.path.islink(path):
                log.warning("%s: path cannot be read [BROKEN LINK?]", path)
            else:
                log.warning("%s: path cannot be read", path)
            return False

        if not basher.path_is_writable(path):
            log.warning("%s: path cannot be written", path)
            return False
        try:
            owner = basher.file_os_owner(path)
        except KeyError:
            owner = basher.file_os_owner_raw(path)

        if owner != self.current_os_user:
            if owner == 990:
                log.debug("%s: wrong owner (%s)", path, owner)
            else:
                log.warning("%s: wrong owner (%s)", path, owner)
            return False
        return True

    def inspect_permissions(self, root='.'):

        for root, sub_folders, files in os.walk(root):

            counter = 0
            for folder in sub_folders:
                if folder == '.git':
                    continue
                # produced by virtual-env?
                if folder == 'lib':
                    continue
                if folder.endswith("__pycache__"):
                    continue
                if folder.endswith(".egg-info"):
                    continue

                path = os.path.join(root, folder)
                if self.check_permissions(path):
                    self.inspect_permissions(root=path)

                counter += 1
                if counter > 20:
                    log.warning("Too many folders, stopped checks in %s", root)
                    break

            counter = 0
            for file in files:
                if file.endswith(".pyc"):
                    continue

                path = os.path.join(root, file)
                self.check_permissions(path)

                counter += 1
                if counter > 100:
                    log.warning("Too many files, stopped checks in %s", root)
                    break

            break

    def read_specs(self, read_only_project=False):
        """ Read project configuration """

        project_file_path = helpers.project_dir(self.project)
        if read_only_project:
            default_file_path = None
        else:
            default_file_path = os.path.join(SUBMODULES_DIR, RAPYDO_CONFS)
        try:
            if self.initialize:
                read_extended = False
            elif self.install:
                read_extended = False
            else:
                read_extended = True

            self.specs, self.extended_project, self.extended_project_path = configuration.read(
                default_file_path=default_file_path,
                base_project_path=project_file_path,
                projects_path=PROJECT_DIR,
                read_extended=read_extended,
                submodules_path=SUBMODULES_DIR,
                do_exit=False,
            )

            self.specs = configuration.mix(
                self.specs, self.arguments.host_configuration
            )

        except AttributeError as e:

            log.exit(e)

        self.vars = self.specs.get('variables', {})
        log.verbose("Configuration loaded")

        framework = glom(self.specs, "variables.frontend.framework", default=None)

        if framework == 'None':
            framework = None

        self.frontend = framework

        if self.frontend is not None:
            log.very_verbose("Frontend framework: %s" % self.frontend)

        self.project_title = glom(self.specs, "project.title", default='Unknown title')
        self.version = glom(self.specs, "project.version", default=None)
        self.rapydo_version = glom(self.specs, "project.rapydo", default=None)
        self.project_description = glom(
            self.specs, "project.description", default='Unknown description'
        )

        if self.rapydo_version is None:
            log.exit("Rapydo version not found in your project_configuration file")

    def preliminary_version_check(self):

        project_file_path = helpers.project_dir(self.project)
        specs = configuration.load_project_configuration(project_file_path)
        v = glom(specs, "project.rapydo", default=None)

        self.verify_rapydo_version(rapydo_version=v)

    def verify_rapydo_version(self, do_exit=True, rapydo_version=None):
        """
        If your project requires a specific rapydo version, check if you are
        the rapydo-controller matching that version
        """
        if self.install or self.print_version:
            return True

        if rapydo_version is None:
            rapydo_version = self.rapydo_version

        if rapydo_version is None:
            return True

        r = LooseVersion(rapydo_version)
        c = LooseVersion(__version__)
        if r == c:
            return True

        if r > c:
            action = "Upgrade your controller to version %s" % r
        else:
            action = "Downgrade your controller to version %s" % r
            action += " or upgrade your project"

        # action += "\n\nrapydo install --git %s" % r
        action += "\n\nrapydo install --git auto"

        msg = "Rapydo version is not compatible"
        msg += "\n\nThis project requires rapydo %s but you are using %s" % (r, c)
        msg += "\n\n%s\n" % action

        if do_exit:
            log.exit(msg)
        else:
            log.warning(msg)

        return False

    def verify_connected(self):
        """ Check if connected to internet """

        connected = checks.internet_connection_available()
        if not connected:
            log.exit('Internet connection is unavailable')
        else:
            log.checked("Internet connection is available")
            self.tested_connection = True
        return

    def working_clone(self, name, repo, confs_only=False, from_path=None):

        # substitute values starting with '$$'
        if confs_only:
            myvars = {}
        else:
            myvars = {
                ANGULARJS: self.frontend == ANGULARJS,
                ANGULAR: self.frontend == ANGULAR,
                REACT: self.frontend == REACT,
                'devel': self.development,
            }
        repo = project.apply_variables(repo, myvars)

        # Is this single repo enabled?
        repo_enabled = repo.pop('if', False)
        if not repo_enabled:
            return

        # if self.upgrade and self.current_args.get('current'):
        #     repo['do'] = True
        # else:
        repo['do'] = self.initialize
        repo['check'] = not self.install and not self.print_version

        # This step may require an internet connection in case of 'init'
        if not self.tested_connection and self.initialize:
            self.verify_connected()

        ################
        # - repo path to the repo name
        if 'path' not in repo:
            repo['path'] = name
        # - version is the one we have on the working controller
        if 'branch' not in repo:
            if confs_only or self.rapydo_version is None:
                repo['branch'] = __version__
            else:
                repo['branch'] = self.rapydo_version

        if from_path is not None:

            local_path = os.path.join(from_path, name)
            if not os.path.exists(local_path):
                log.exit("Submodule %s not found in %s", repo['path'], from_path)

            submodule_path = os.path.join(
                helpers.current_dir(), SUBMODULES_DIR, repo['path']
            )

            if os.path.exists(submodule_path):
                log.warning("Path %s already exists, removing", submodule_path)
                if os.path.isfile(submodule_path):
                    os.remove(submodule_path)
                elif os.path.islink(submodule_path):
                    os.remove(submodule_path)
                else:
                    shutil.rmtree(submodule_path)

            os.symlink(local_path, submodule_path)

        return gitter.clone(**repo)

    def git_submodules(self, confs_only=False):
        """ Check and/or clone git projects """

        from_local_path = self.current_args.get('submodules_path')
        if from_local_path is not None:
            if not os.path.exists(from_local_path):
                log.exit("Local path not found: %s", from_local_path)

        if confs_only:
            repos = {}
            repos[RAPYDO_CONFS] = {
                "online_url": "%s/%s.git" % (RAPYDO_GITHUB, RAPYDO_CONFS),
                "if": "true",
            }
        else:
            repos = self.vars.get('submodules', {}).copy()

        self.gits['main'] = gitter.get_repo(".")

        for name, repo in repos.items():
            self.gits[name] = self.working_clone(
                name, repo, confs_only=confs_only, from_path=from_local_path
            )

    def git_update_repos(self):

        for name, gitobj in self.gits.items():
            if gitobj is not None:
                gitter.update(name, gitobj)

    def prepare_composers(self):

        # substitute values starting with '$$'

        load_commons = not self.current_args.get('no_commons')

        myvars = {
            'backend': not self.current_args.get('no_backend'),
            ANGULARJS: self.frontend == ANGULARJS and not self.current_args.get('no_frontend'),
            ANGULAR: self.frontend == ANGULAR and not self.current_args.get('no_frontend'),
            REACT: self.frontend == REACT and not self.current_args.get('no_frontend'),
            'logging': self.current_args.get('collect_logs'),
            'devel': self.development,
            'commons': load_commons,
            'extended-commons': self.extended_project is not None and load_commons,
            'mode': self.current_args.get('mode'),
            'extended-mode': self.extended_project is not None,
            'baseconf': helpers.current_dir(
                SUBMODULES_DIR, RAPYDO_CONFS, CONTAINERS_YAML_DIRNAME
            ),
            'customconf': helpers.project_dir(self.project, CONTAINERS_YAML_DIRNAME),
        }

        if self.extended_project_path is None:
            myvars['extendedproject'] = None
        else:
            myvars['extendedproject'] = os.path.join(
                self.extended_project_path, CONTAINERS_YAML_DIRNAME
            )

        compose_files = OrderedDict()

        confs = self.vars.get('composers', {})
        for name, conf in confs.items():
            compose_files[name] = project.apply_variables(conf, myvars)

        # TOFIX: temporary fix to let to use both angularjs and angular
        # One completed the porting from angularjs to angular
        # rename rapydo-confs/frontend-a2.yml into rapydo-confs/frontend.yml
        # and remove this piece of code
        if 'frontend' in compose_files:

            branch = glom(
                self.specs, "variables.repos.frontend.branch", default='master'
            )

            if branch != 'master':
                compose_files['frontend']['file'] = 'frontend-a2'
        # ################################################################# #

        return compose_files

    def read_composers(self):

        # Find configuration that tells us which files have to be read
        compose_files = self.prepare_composers()

        # Read necessary files
        self.services, self.files, self.base_services, self.base_files = read_yamls(
            compose_files
        )
        log.verbose("Configuration order:\n%s" % self.files)

    def build_dependencies(self):
        """ Look up for builds which are depending on templates """

        if self.action not in ['check', 'update', 'build']:
            return

        # Compare builds depending on templates (slow operation!)
        self.builds, self.template_builds, overriding_imgs = locate_builds(
            self.base_services, self.services
        )

        if self.action == 'build':
            # Nothing more to do now, builds will be performed later (in _build method)
            return

        # we are in check or build case
        dimages = self.docker.images()
        # if rebuild templates is on build is forced, these checks are not needed
        if not self.current_args.get('rebuild_templates', False):
            rebuilt = self.verify_template_builds(dimages, self.template_builds)
            if rebuilt:
                # locate again builds
                self.builds, self.template_builds, overriding_imgs = locate_builds(
                    self.base_services, self.services
                )

        self.verify_obsolete_builds(
            dimages, self.builds, overriding_imgs, self.template_builds
        )

    def get_build_timestamp(self, timestamp, as_date=False):

        if timestamp is None:
            log.warning("Received a null timestamp, defaulting to zero")
            timestamp = 0
        # Prior of dockerpy 2.5.1 image build timestamps were given as epoch
        # i.e. were convertable to float
        # From dockerpy 2.5.1 we are obtaining strings like this:
        # 2017-09-22T07:10:35.822772835Z as we need to convert to epoch
        try:
            # verify if timestamp is already an epoch
            float(timestamp)
        except ValueError:
            # otherwise, convert it
            timestamp = date_from_string(timestamp).timestamp()

        if as_date:
            return datetime.fromtimestamp(timestamp)
        return timestamp

    def build_is_obsolete(self, build):
        # compare dates between git and docker
        path = build.get('path')
        build_templates = self.gits.get('build-templates')
        vanilla = self.gits.get('main')

        if path.startswith(build_templates.working_dir):
            git_repo = build_templates
        elif path.startswith(vanilla.working_dir):
            git_repo = vanilla
        else:
            log.exit("Unable to find git repo %s" % path)

        build_timestamp = self.get_build_timestamp(build.get('timestamp'))

        files = helpers.list_path(path)
        for f in files:
            local_file = os.path.join(path, f)

            obsolete, build_ts, last_commit = gitter.check_file_younger_than(
                gitobj=git_repo, filename=local_file, timestamp=build_timestamp
            )

            if obsolete:
                log.info("File changed: %s", f)
                return obsolete, build_ts, last_commit

        return False, 0, 0

    @staticmethod
    def get_compose(files):
        return Compose(files=files)

    def verify_template_builds(self, docker_images, builds):

        if len(builds) == 0:
            log.debug("No template build to be verified")
            return False

        rebuilt = False
        found_obsolete = 0
        fmt = "%Y-%m-%d %H:%M:%S"
        for image_tag, build in builds.items():

            is_active = False
            for service in build['services']:
                if service in self.active_services:
                    is_active = True
                    break
            if not is_active:
                log.very_verbose(
                    "Checks skipped: template %s not enabled (service list = %s)",
                    image_tag,
                    build['services'],
                )
                continue

            if image_tag not in docker_images:

                found_obsolete += 1
                message = "Missing template build for %s (%s)" % (
                    build['services'],
                    image_tag,
                )
                if self.action == 'check':
                    message += "\nSuggestion: execute the init command"
                    log.exit(message)
                else:
                    log.debug(message)
                    dc = self.get_compose(files=self.base_files)
                    dc.build_images(
                        builds={image_tag: build},
                        current_version=__version__,
                        current_uid=self.current_uid,
                    )
                    rebuilt = True

                continue

            obsolete, build_ts, last_commit = self.build_is_obsolete(build)
            if obsolete:
                found_obsolete += 1
                b = datetime.fromtimestamp(build_ts).strftime(fmt)
                c = last_commit.strftime(fmt)
                message = "Template image %s is obsolete" % image_tag
                message += " (built on %s" % b
                message += " but changed on %s)" % c
                if self.current_args.get('rebuild'):
                    log.info("%s, rebuilding", message)
                    dc = self.get_compose(files=self.base_files)
                    dc.build_images(
                        builds={image_tag: build},
                        current_version=__version__,
                        current_uid=self.current_uid,
                    )
                    rebuilt = True
                else:
                    message += "\nRebuild it with:\n"
                    message += "$ rapydo --services %s" % build.get('service')
                    message += " build --rebuild-templates"
                    log.warning(message)

        if found_obsolete == 0:
            log.debug("No template build to be updated")

        return rebuilt

    def verify_obsolete_builds(
        self, docker_images, builds, overriding_imgs, template_builds
    ):

        if len(builds) == 0:
            log.debug("No build to be verified")
            return

        found_obsolete = 0
        fmt = "%Y-%m-%d %H:%M:%S"
        for image_tag, build in builds.items():

            if image_tag not in docker_images:
                # Missing images will be created at startup
                continue

            is_active = False
            for service in build['services']:
                if service in self.active_services:
                    is_active = True
                    break
            if not is_active:
                log.very_verbose(
                    "Checks skipped: template %s not enabled (service list = %s)",
                    image_tag,
                    build['services'],
                )
                continue

            build_is_obsolete = False
            message = ""

            # if FROM image is newer, this build should be re-built
            if image_tag in overriding_imgs:
                from_img = overriding_imgs.get(image_tag)
                from_build = template_builds.get(from_img)
                from_timestamp = self.get_build_timestamp(
                    from_build.get('timestamp'), as_date=True
                )
                build_timestamp = self.get_build_timestamp(
                    build.get('timestamp'), as_date=True
                )

                if from_timestamp > build_timestamp:
                    build_is_obsolete = True
                    b = build_timestamp.strftime(fmt)
                    c = from_timestamp.strftime(fmt)
                    message = "Image %s is obsolete" % image_tag
                    message += " (built on %s FROM %s" % (b, from_img)
                    message += " that changed on %s)" % c

            if not build_is_obsolete:
                # Check if some recent commit modified the Dockerfile
                obsolete, build_ts, last_commit = self.build_is_obsolete(build)
                if obsolete:
                    build_is_obsolete = True
                    b = datetime.fromtimestamp(build_ts).strftime(fmt)
                    c = last_commit.strftime(fmt)
                    message = "Image %s is obsolete" % image_tag
                    message += " (built on %s" % b
                    message += " but changed on %s)" % c

            # TODO: for backend build check for any commit on utils o backend
            # TODO: for rapydo builds check for any commit on utils
            if build_is_obsolete:
                found_obsolete += 1
                if self.current_args.get('rebuild'):
                    log.info("%s, rebuilding", message)
                    dc = self.get_compose(files=self.files)

                    # Cannot force pull when building an image
                    # overriding a template build
                    force_pull = image_tag not in overriding_imgs
                    dc.build_images(
                        builds={image_tag: build},
                        force_pull=force_pull,
                        current_version=__version__,
                        current_uid=self.current_uid,
                    )
                else:
                    message += "\nRebuild it with:\n"
                    message += "$ rapydo --services %s" % build.get('service')
                    message += " build"
                    log.warning(message)

        if found_obsolete == 0:
            log.debug("No build to be updated")

    def frontend_libs(self):

        if self.frontend is None:
            return False

        if not any([self.check, self.initialize, self.update]):
            return False

        # What to do with REACT?
        if self.frontend != ANGULAR:
            return False

        libs_dir = os.path.join("data", self.project, "frontend")
        modules_dir = os.path.join(libs_dir, "node_modules")

        if not os.path.isdir(libs_dir):
            os.makedirs(libs_dir)
            log.warning("Libs folder not found, creating %s" % libs_dir)
        if not os.path.isdir(modules_dir):
            os.makedirs(modules_dir)
            log.warning("Modules folder not found, creating %s" % modules_dir)

        if not os.path.exists(os.path.join(libs_dir, "package.json")):
            log.warning("Package.json not found, will be created at startup")

        libs = helpers.list_path(modules_dir)

        if len(libs) <= 0:
            log.warning("Frontend libs not found, will be installed at startup")
        else:
            log.checked("Found %d frontend libs installed" % len(libs))

    def get_services(self, key='services', sep=',', default=None):

        value = self.current_args.get(key).split(sep)
        if default is None:
            return value

        # check if value is equal to the services default from the configuration
        config_default = glom(self.arguments.parse_conf, "options.services.default")
        if value == [config_default]:
            return default

        return value

    @staticmethod
    def read_env():
        envfile = os.path.join(helpers.current_dir(), COMPOSE_ENVIRONMENT_FILE)
        env = {}
        if not os.path.isfile(envfile):
            log.critical("Env file not found")
            return env

        with open(envfile, 'r') as f:
            lines = f.readlines()
            for line in lines:
                line = line.split("=")
                k = line[0].strip()
                v = line[1].strip()
                env[k] = v
        return env

    def make_env(self):
        envfile = os.path.join(helpers.current_dir(), COMPOSE_ENVIRONMENT_FILE)

        try:
            os.unlink(envfile)
            log.verbose("Removed cache of %s" % COMPOSE_ENVIRONMENT_FILE)
        except FileNotFoundError:
            log.very_verbose("No %s to remove" % COMPOSE_ENVIRONMENT_FILE)

        env = self.vars.get('env')
        if env is None:
            env = {}
        env['PROJECT_DOMAIN'] = self.current_args.get('hostname', 'localhost')
        env['COMPOSE_PROJECT_NAME'] = self.project
        # Relative paths from ./submodules/rapydo-confs/confs
        env['SUBMODULE_DIR'] = "../.."
        env['VANILLA_DIR'] = "../../.."
        env['PROJECT_DIR'] = os.path.join(env['VANILLA_DIR'], PROJECT_DIR, self.project)

        if self.extended_project_path is None:
            env['EXTENDED_PROJECT_PATH'] = env['PROJECT_DIR']
        else:
            env['EXTENDED_PROJECT_PATH'] = os.path.join(
                env['VANILLA_DIR'], self.extended_project_path
            )

        if self.extended_project is None:
            env['EXTENDED_PROJECT'] = EXTENDED_PROJECT_DISABLED
        else:
            env['EXTENDED_PROJECT'] = self.extended_project

        env['RAPYDO_VERSION'] = __version__
        env['CURRENT_UID'] = self.current_uid
        env['PROJECT_TITLE'] = self.project_title
        env['PROJECT_DESCRIPTION'] = self.project_description
        if self.current_args.get('privileged'):
            env['DOCKER_PRIVILEGED_MODE'] = "true"
        else:
            env['DOCKER_PRIVILEGED_MODE'] = "false"

        if self.action == "formatter" and self.current_args.get('folder') is not None:
            VANILLA_SUBMODULE = 'vanilla'
            submodule = self.current_args.get('submodule', VANILLA_SUBMODULE)

            if submodule == VANILLA_SUBMODULE:
                env['BLACK_SUBMODULE'] = ""
                env['BLACK_FOLDER'] = self.current_args.get('folder')
            else:
                env['BLACK_SUBMODULE'] = submodule
                env['BLACK_FOLDER'] = self.current_args.get('folder')

        net = self.current_args.get('net', 'bridge')
        env['DOCKER_NETWORK_MODE'] = net
        # env.update({'PLACEHOLDER': PLACEHOLDER})

        # # docker network mode
        # # https://docs.docker.com/compose/compose-file/#network_mode
        # nmode = self.current_args.get('net')
        # nmodes = ['bridge', 'hosts']
        # if nmode not in nmodes:
        #     log.warning("Invalid network mode: %s", nmode)
        #     nmode = nmodes[0]
        # env['DOCKER_NETWORK_MODE'] = nmode
        # print("TEST", nmode, env['DOCKER_NETWORK_MODE'])

        with open(envfile, 'w+') as whandle:
            for key, value in sorted(env.items()):
                if value is None:
                    value = ''
                else:
                    value = str(value)
                # log.print("ENV values. %s:*%s*" % (key, value))
                if ' ' in value:
                    value = "'%s'" % value
                whandle.write("%s=%s\n" % (key, value))
            log.checked("Created %s file" % COMPOSE_ENVIRONMENT_FILE)

    def check_placeholders(self):

        self.services_dict, self.active_services = project.find_active(self.services)

        if len(self.active_services) == 0:
            log.exit(
                """You have no active service
\nSuggestion: to activate a top-level service edit your project_configuration
and add the variable "ACTIVATE_DESIREDSERVICE: 1"
                """
            )
        else:
            log.checked("Active services: %s", self.active_services)

        missing = []
        for service_name in self.active_services:
            service = self.services_dict.get(service_name)

            for key, value in service.get('environment', {}).items():
                if PLACEHOLDER in str(value):
                    key = self.normalize_placeholder_variable(key)
                    missing.append(key)

        # Removed duplicates
        missing = set(missing)

        placeholders = []
        for key in missing:

            serv = self.vars_to_services_mapping.get(key)
            if serv is None:
                log.exit("Unexpected error, cannot find a service mapping with %s", key)
            active_serv = []
            for i in serv:
                if i in self.active_services:
                    active_serv.append(i)
            if len(active_serv) > 0:
                placeholders.append(
                    "%-20s\trequired by\t%s" % (key, ', '.join(active_serv))
                )
            else:
                log.verbose(
                    "Variable %s is missing, but %s service(s) not active", key, serv
                )

        if len(placeholders) > 0:
            m = "\n".join(placeholders)
            tips = "\n\nYou can fix this error by updating the "
            tips += "project_configuration.yaml file or you local .projectrc file\n"
            log.exit(
                "The following variables are missing in your configuration:\n\n%s%s",
                m,
                tips,
            )

        else:
            log.verbose("No placeholder variable to be replaced")

        return missing

    def container_info(self, service_name):
        return self.services_dict.get(service_name, None)

    def container_service_exists(self, service_name):
        return self.container_info(service_name) is not None

    def get_ignore_submodules(self):
        ignore_submodule = self.current_args.get('ignore_submodule', '')
        if ignore_submodule is None:
            return ''
        return ignore_submodule.split(",")

    def git_checks(self):

        # TODO: give an option to skip things when you are not connected
        if not self.tested_connection:
            self.verify_connected()

        # FIXME: give the user an option to skip this
        # or eventually print it in a clearer way
        # (a table? there is python ascii table plugin)

        ignore_submodule_list = self.get_ignore_submodules()

        for name, gitobj in sorted(self.gits.items()):
            if name in ignore_submodule_list:
                log.debug("Skipping %s on %s" % (self.action, name))
                continue
            if gitobj is not None:
                if self.update:
                    gitter.update(name, gitobj)
                elif self.check:
                    gitter.check_updates(name, gitobj)
                    gitter.check_unstaged(name, gitobj)

    def custom_parse_args(self):

        # custom options from configuration file
        self.custom_commands = glom(self.specs, "controller.commands", default={})

        if len(self.custom_commands) < 1:
            log.exit("No custom commands defined")

        for name, custom in self.custom_commands.items():
            self.arguments.extra_command_parser.add_parser(
                name, help=custom.get('description')
            )

        if len(self.arguments.remaining_args) != 1:
            self.arguments.extra_parser.print_help()
            import sys

            sys.exit(1)

        # parse it
        self.custom_command = vars(
            self.arguments.extra_parser.parse_args(self.arguments.remaining_args)
        ).get('custom')

    ################################
    # ##    COMMANDS    ##         #
    ################################

    # TODO: make the commands availabe in this file in alphabetical order

    def _check(self):

        # NOTE: Do we consider what we have here a SECURITY BUG?
        # dc = self.get_compose(files=self.files)
        # for container in dc.get_handle().project.containers():
        #     log.pp(container.client._auth_configs)
        #     exit(1)

        log.info("All checked")

    def _init(self):
        log.info("Project initialized")

    def _status(self):
        dc = self.get_compose(files=self.files)
        dc.command(
            'ps', {'-q': None, '--services': None, '--quiet': False, '--all': False}
        )

    def _clean(self):
        dc = self.get_compose(files=self.files)
        rm_volumes = self.current_args.get('rm_volumes', False)
        options = {
            '--volumes': rm_volumes,
            '--remove-orphans': True,
            '--rmi': 'local',  # 'all'
        }
        dc.command('down', options)

        log.info("Stack cleaned")

    def _update(self):
        log.info("All updated")

    def _start(self):

        services = self.get_services(default=self.active_services)

        dc = self.get_compose(files=self.files)
        dc.start_containers(services)

        log.info("Stack started")

    def _stop(self):
        services = self.get_services(default=self.active_services)

        options = {'SERVICE': services}

        dc = self.get_compose(files=self.files)
        dc.command('stop', options)

        log.info("Stack stopped")

    def _restart(self):
        services = self.get_services(default=self.active_services)

        options = {'SERVICE': services}

        dc = self.get_compose(files=self.files)
        dc.command('restart', options)

        log.info("Stack restarted")

    def _remove(self):
        services = self.get_services(default=self.active_services)

        dc = self.get_compose(files=self.files)

        options = {
            'SERVICE': services,
            # '--stop': True,  # BUG? not working
            '--force': True,
            '-v': False,  # dangerous?
        }
        dc.command('stop')
        dc.command('rm', options)

        log.info("Stack removed")

    def _toggle_freeze(self):
        services = self.get_services(default=self.active_services)

        options = {'SERVICE': services}
        dc = self.get_compose(files=self.files)
        command = 'pause'
        for container in dc.get_handle().project.containers():

            if container.dictionary.get('State').get('Status') == 'paused':
                command = 'unpause'
                break
        dc.command(command, options)

        if command == "pause":
            log.info("Stack paused")
        elif command == "unpause":
            log.info("Stack unpaused")

    def _logs(self):

        service = self.current_args.get('service')
        if service is None:
            services = self.get_services(default=self.active_services)
        else:
            services = [service]

        options = {
            '--follow': self.current_args.get('follow', False),
            '--tail': self.current_args.get('tail', "100"),
            '--no-color': False,
            '--timestamps': True,
            'SERVICE': services,
        }

        dc = self.get_compose(files=self.files)
        try:
            dc.command('logs', options)
        except KeyboardInterrupt:
            log.info("Stopped by keyboard")

    def _interfaces(self):
        # db = self.manage_one_service()
        db = self.current_args.get('service')
        service = db + 'ui'

        if not self.container_service_exists(service):
            log.exit("Container '%s' is not defined" % service)

        port = self.current_args.get('port')
        publish = []

        if port is not None:
            try:
                int(port)
            except TypeError:
                log.exit("Port must be a valid integer")

            info = self.container_info(service)
            try:
                current_ports = info.get('ports', []).pop(0)
            except IndexError:
                log.exit("No default port found?")

            publish.append("%s:%s" % (port, current_ports.target))

        dc = self.get_compose(files=self.files)

        host = self.current_args.get('hostname')
        # FIXME: to be completed
        uris = {
            'swaggerui':
            # 'http://%s/swagger-ui/?url=http://%s:%s/api/specs' %
            # (host, host, '8080'),
            'http://%s?docExpansion=none'
            % host
        }

        uri = uris.get(service)
        if uri is not None:
            log.info("You can access %s web page here:\n%s", service, uri)
        else:
            log.info("Launching interface: %s", service)
        with suppress_stdout():
            # NOTE: this is suppressing also image build...
            detach = self.current_args.get('detach')
            dc.create_volatile_container(service, publish=publish, detach=detach)

    def _shell(self, user=None, command=None, service=None):

        dc = self.get_compose(files=self.files)
        service = self.current_args.get('service')
        no_tty = self.current_args.get('no_tty')
        # service = self.manage_one_service(service)

        if user is None:
            user = self.current_args.get('user')
            # if 'user' is empty, put None to get the docker-compose default
            if user is not None and user.strip() == '':
                if service in ['backend', 'restclient']:
                    user = 'developer'
                else:
                    user = None
        log.verbose("Command as user '%s'" % user)

        if command is None:
            default = 'echo hello world'
            command = self.current_args.get('command', default)

        return dc.exec_command(service, user=user, command=command, disable_tty=no_tty)

    def _build(self):

        if self.current_args.get('rebuild_templates'):
            dc = self.get_compose(files=self.base_files)
            log.debug("Forcing rebuild of cached templates")
            dc.build_images(
                self.template_builds,
                current_version=__version__,
                current_uid=self.current_uid,
            )

        dc = self.get_compose(files=self.files)
        services = self.get_services(default=self.active_services)

        options = {
            'SERVICE': services,
            '--no-cache': self.current_args.get('force'),
            '--pull': False,
        }
        dc.command('build', options)

        log.info("Images built")

    def _pull(self):
        dc = self.get_compose(files=self.base_files)
        services = self.get_services(default=self.active_services)

        base_services_list = []
        for s in self.base_services:
            base_services_list.append(s.get('name'))

        # List of BASE active services (i.e. remove services not in base)
        services_intersection = list(set(services).intersection(base_services_list))

        options = {
            'SERVICE': services_intersection,
            # TODO: user should be allowed to set the two below from cli
            '--no-cache': False,
            '--pull': False,
        }
        dc.command('pull', options)

        log.info("Base images pulled from docker hub")

    def _custom(self):
        log.debug("Custom command: %s" % self.custom_command)
        meta = self.custom_commands.get(self.custom_command)
        meta.pop('description', None)

        service = meta.get('service')
        user = meta.get('user', None)
        command = meta.get('command', None)
        dc = self.get_compose(files=self.files)
        return dc.exec_command(service, user=user, command=command)

    def _ssl_certificate(self):
        chain = self.current_args.get('chain_file')
        key = self.current_args.get('key_file')
        no_tty = self.current_args.get('no_tty')

        if chain is not None or key is not None:
            if chain is None:
                log.exit("Invalid chain file (your provided none)")
            elif not os.path.exists(chain):
                log.exit("Invalid chain file (your provided %s)", chain)

            if key is None:
                log.exit("Invalid key file (your provided none)")
            elif not os.path.exists(key):
                log.exit("Invalid key file (your provided %s)", key)

        meta = glom(
            self.arguments.parse_conf,
            "subcommands.ssl-certificate.container_exec",
            default={},
        )

        # Verify all is good
        assert meta.pop('name') == 'letsencrypt'

        service = meta.get('service')
        user = meta.get('user', None)

        if chain is not None and key is not None:

            log.info("Unable to automatically perform the requested operation")
            log.info("You can execute the following commands by your-self:")

            print("")
            print(
                "docker cp %s %s_%s_1:/etc/letsencrypt/real/fullchain1.pem"
                % (chain, self.project, service)
            )
            print(
                "docker cp %s %s_%s_1:/etc/letsencrypt/real/privkey1.pem"
                % (key, self.project, service)
            )

            print("rapydo shell %s --command \"nginx -s reload\"" % service)
            print("")

            return True

        command = meta.get('command', None)
        dc = self.get_compose(files=self.files)

        if self.current_args.get('volatile'):
            # return dc.command('up', options)
            return dc.start_containers(["certificates-proxy"], detach=False)

        if self.current_args.get('force'):
            command = "%s --force" % command

        return dc.exec_command(service, user=user, command=command, disable_tty=no_tty)

    def _ssl_dhparam(self):
        meta = glom(
            self.arguments.parse_conf,
            "subcommands.ssl-dhparam.container_exec",
            default={},
        )

        # Verify all is good
        assert meta.pop('name') == 'dhparam'

        service = meta.get('service')
        user = meta.get('user', None)
        command = meta.get('command', None)
        dc = self.get_compose(files=self.files)
        return dc.exec_command(service, user=user, command=command)

    def _list(self):

        printed_something = False
        if self.current_args.get('args'):
            printed_something = True
            log.info("List of configured rapydo arguments:\n")
            for var in sorted(self.current_args):
                val = self.current_args.get(var)
                print("%-20s\t%s" % (var, val))

        if self.current_args.get('env'):
            printed_something = True
            log.info("List env variables:\n")
            env = self.read_env()
            for var in sorted(env):
                val = env.get(var)
                print("%-36s\t%s" % (var, val))

        if self.current_args.get('services'):
            printed_something = True
            log.info("List of active services:\n")
            pwd = helpers.current_fullpath()
            print("%-12s %-24s %s" % ("Name", "Image", "Path"))

            for service in self.services:
                name = service.get('name')
                if name in self.active_services:
                    image = service.get("image")
                    build = service.get("build")
                    if build is None:
                        print("%-12s %-24s" % (name, image))
                    else:
                        path = build.get('context')
                        path = path.replace(pwd, "")
                        if path.startswith("/"):
                            path = path[1:]
                        print("%-12s %-24s %s" % (name, image, path))

                    # ports = service.get("ports")
                    # if ports is not None:
                    #     for p in ports:
                    #         print("\t%s -> %s" % (p.target, p.published))

                    # volumes = service.get("volumes")
                    # if volumes is not None:
                    #     for volume in volumes:
                    #         vext = volume.external
                    #         vext = vext.replace(pwd, "")
                    #         if vext.startswith("/"):
                    #             vext = vext[1:]
                    #         vint = volume.internal
                    #         print("\t%s -> %s" % (vext, vint))

        if self.current_args.get('submodules'):
            printed_something = True
            log.info("List of submodules:\n")
            pwd = helpers.current_fullpath()
            print("%-18s %-18s %s" % ("Repo", "Branch", "Path"))
            for name in self.gits:
                repo = self.gits.get(name)
                if repo is None:
                    continue
                branch = gitter.get_active_branch(repo)
                path = repo.working_dir
                path = path.replace(pwd, "")
                if path.startswith("/"):
                    path = path[1:]
                print("%-18s %-18s %s" % (name, branch, path))

        if not printed_something:
            log.error(
                "You have to specify what to list, "
                + "please use rapydo list -h for available options"
            )

    def _template(self):

        service_name = self.current_args.get('service')
        if service_name is None:
            service_name = self.vars.get('env', {}).get('AUTH_SERVICE')

        force = self.current_args.get('yes')
        endpoint_name = self.current_args.get('endpoint')

        new_endpoint = EndpointScaffold(
            self.project, force, endpoint_name, service_name
        )
        new_endpoint.create()

    def _find(self):
        endpoint_name = self.current_args.get('endpoint')

        if endpoint_name is not None:
            lookup = EndpointScaffold(self.project, endpoint_name=endpoint_name)
            lookup.info()
        else:
            log.exit(
                "Please, specify something to look for.\n"
                + "Add --help to list available options."
            )

    def _scale(self):

        scaling = self.current_args.get('value', '')
        options = scaling.split('=')
        if len(options) != 2:
            log.exit("Please specify how to scale: SERVICE=NUM_REPLICA")
        else:
            service, nreplicas = options

        if not nreplicas.isnumeric():
            log.exit("Invalid number of replicas: %s", nreplicas)

        dc = self.get_compose(files=self.files)
        # dc.command('up', compose_options)
        dc.start_containers([service], scale=[scaling], skip_dependencies=True)

    def _verify(self):
        """ Verify one service connection (inside backend) """
        service = self.current_args.get('service')
        dc = self.get_compose(files=self.files)
        command = 'restapi verify --services %s' % service

        # super magic trick
        try:
            # test the normal container if already running
            return dc.exec_command('backend', command=command, nofailure=True)
        except AttributeError:
            # otherwise shoot a one-time backend container for that
            return dc.create_volatile_container('backend', command)

    def _volatile(self):
        """ One command container (NOT executing on a running one) """
        service = self.current_args.get('service')
        command = self.current_args.get('command')
        dc = self.get_compose(files=self.files)
        dc.create_volatile_container(service, command)

    def _create(self, project_name, template_name):

        if gitter.get_local(".") is not None:
            log.exit("You are on a git repo, unable to continue")

        if os.path.exists(project_name):
            log.exit("%s folder already exists, unable to continue", project_name)

        os.mkdir(project_name)

        if not os.path.exists(project_name):
            log.exit("Errors creating %s folder")

        template_tmp_dir = "__template"
        template_tmp_path = os.path.join(project_name, template_tmp_dir)
        online_url = "%s/%s.git" % (RAPYDO_GITHUB, RAPYDO_TEMPLATE)
        gitter.clone(
            online_url,
            template_tmp_path,
            branch=__version__,
            do=True,
            check=True,
            expand_path=False,
        )

        copy_tree(template_tmp_path, project_name)

        os.mkdir(os.path.join(project_name, 'data'))

        shutil.rmtree(template_tmp_path)

        if template_name is None:
            log.info("Project %s successfully created", project_name)
            print("")
            print("You can run one of the following templates:")

        project_dir = os.path.join(project_name, PROJECT_DIR)
        vanilla_dir = os.path.join(project_dir, project_name)
        template_path = os.path.join(project_dir, template_name)

        if not os.path.exists(template_path):
            log.exit("Invalid template name: %s", template_name)

        if not os.path.exists(vanilla_dir):

            os.mkdir(vanilla_dir)
            copy_tree(template_path, vanilla_dir)
            log.info("Copy from %s", template_path)

        with open(os.path.join(project_name, PROJECTRC), 'w+') as f:
            f.write("project: %s" % project_name)

        git_dir = os.path.join(project_name, ".git")
        shutil.rmtree(git_dir)

        log.info(
            "Project %s successfully created from %s template",
            project_name,
            template_name,
        )
        projects = helpers.list_path(project_dir)
        for p in projects:
            if p != project_name:
                pdir = os.path.join(project_dir, p)
                shutil.rmtree(pdir)
                log.info("Unused template project deleted: %s ", p)

        print("")
        print("Now you can enter the project and execute rapydo init")
        print("")
        print("cd %s" % project_name)
        print("git init")
        print("git remote add origin https://your_remote_git/your_project.git")
        print("rapydo init")

    def _version(self):
        # You are not inside a rapydo project, only printing rapydo version
        if not hasattr(self, "version"):
            print('\nrapydo version: %s' % __version__)
            return

        # Check if rapydo version is compatible with version required by the project
        if __version__ == self.rapydo_version:
            c = "\033[1;32m"  # Light Green
        else:
            c = "\033[1;31m"  # Light Red
        d = "\033[0m"

        cv = "%s%s%s" % (c, __version__, d)
        pv = "%s%s%s" % (c, self.version, d)
        rv = "%s%s%s" % (c, self.rapydo_version, d)
        print('\nrapydo: %s\t%s: %s\trequired rapydo: %s' % (cv, self.project, pv, rv))

        if __version__ != self.rapydo_version:
            c = LooseVersion(__version__)
            v = LooseVersion(self.rapydo_version)
            print(
                '\nThis project is not compatible with the current rapydo version (%s)'
                % __version__
            )
            if c < v:
                print(
                    "Please upgrade rapydo to version %s or modify this project"
                    % self.rapydo_version
                )
            else:
                print(
                    "Please downgrade rapydo to version %s or modify this project"
                    % self.rapydo_version
                )

            print("\n\033[1;31mrapydo install --git %s\033[0m" % self.rapydo_version)

    def read_conf_files(self, filename_base):
        """
        Generic method to find and list:
        - submodules/rapydo-confs/conf/YOURBASE.yml     # required
        - projects/CURRENT_PROJECT/conf/YOURBASE.yml    # optional
        """
        files = []

        basedir = helpers.current_dir(
            SUBMODULES_DIR, RAPYDO_CONFS, CONTAINERS_YAML_DIRNAME
        )
        customdir = helpers.project_dir(self.project, CONTAINERS_YAML_DIRNAME)

        main_yml = load_yaml_file(
            file=filename_base, path=basedir, extension=SHORT_YAML_EXT, return_path=True
        )
        files.append(main_yml)
        custom_yml = load_yaml_file(
            file=filename_base,
            path=customdir,
            extension=SHORT_YAML_EXT,
            return_path=True,
            skip_error=True,
            logger=False,
        )
        if isinstance(custom_yml, str):
            log.debug("Found custom %s specs", filename_base)
            files.append(custom_yml)

        return files

    def _formatter(self):

        command = 'run'
        dc = self.get_compose(files=self.read_conf_files('formatter'))
        options = dc.command_defaults(command=command)

        VANILLA_SUBMODULE = 'vanilla'
        if self.current_args.get('submodule', VANILLA_SUBMODULE) == VANILLA_SUBMODULE:
            options['SERVICE'] = 'vanilla-formatter'
        else:
            options['SERVICE'] = 'submodules-formatter'

        dc.command(command, options)

    def _dump(self):

        #################
        # 1. base dump
        mybin = 'docker-compose'
        # NOTE: can't figure it out why, but 'dc' on config can't use files
        # so I've used basher (since it's already imported)
        bash = basher.BashCommands()
        params = []
        for file in self.files:
            params.append('-f')
            params.append(file)
        params.append('config')
        yaml_string = bash.execute_command(mybin, parameters=params)

        #################
        # 2. filter active services
        from utilities.myyaml import yaml

        # replacing absolute paths with relative ones
        main_dir = path.current_dir()
        obj = yaml.load(yaml_string.replace(main_dir, '.'))

        active_services = {}
        for key, value in obj.get('services', {}).items():
            if key in self.active_services:
                active_services[key] = value
        obj['services'] = active_services

        #################
        # 3. write file
        filename = '%s.yml' % mybin
        with open(filename, 'w') as fh:
            fh.write(yaml.dump(obj, default_flow_style=False))
        log.warning("Config dump: %s", filename)

    def _install(self):
        version = self.current_args.get('version')
        git = self.current_args.get('git')
        editable = self.current_args.get('editable')

        if git and editable:
            log.exit("--git and --editable options are not compatible")

        if version == 'auto':
            self.read_specs(read_only_project=True)
            version = self.rapydo_version
            log.info("Detected version %s to be installed", version)

        if git:
            return self.install_controller_from_git(version)
        elif editable:
            return self.install_controller_from_folder(version)
        else:
            return self.install_controller_from_pip(version)

    def install_controller_from_pip(self, version):

        # BEWARE: to not import this package outside the function
        # Otherwise pip will go crazy
        # (we cannot understand why, but it does!)
        from utilities.packing import install

        # from utilities.packing import check_version

        log.info("You asked to install rapydo-controller %s from pip", version)

        package = "rapydo-controller"
        controller = "%s==%s" % (package, version)
        installed = install(controller)
        if not installed:
            log.error("Unable to install controller %s from pip", version)
        else:
            log.info("Controller version %s installed from pip", version)
            # installed_version = check_version(package)
            # log.info("Check on installed version: %s", installed_version)

    @staticmethod
    def install_controller_from_git(version):

        # BEWARE: to not import this package outside the function
        # Otherwise pip will go crazy
        # (we cannot understand why, but it does!)
        from utilities.packing import install, check_version

        log.info("You asked to install rapydo-controller %s from git", version)

        package = "rapydo-controller"
        controller_repository = "do"
        utils_repository = "utils"
        rapydo_uri = "https://github.com/rapydo"
        utils = "git+%s/%s.git@%s" % (rapydo_uri, utils_repository, version)
        controller = "git+%s/%s.git@%s" % (rapydo_uri, controller_repository, version)

        installed = install(utils)
        if installed:
            installed = install(controller)

        if not installed:
            log.error("Unable to install controller %s from git", version)
        else:
            log.info("Controller version %s installed from git", version)
            installed_version = check_version(package)
            log.info("Check on installed version: %s", installed_version)

    def install_controller_from_folder(self, version):

        # BEWARE: to not import this package outside the function
        # Otherwise pip will go crazy
        # (we cannot understand why, but it does!)
        from utilities.packing import install, check_version

        log.info("You asked to install rapydo-controller %s from local folder", version)

        package = "rapydo-controller"
        utils_path = os.path.join(SUBMODULES_DIR, "utils")
        do_path = os.path.join(SUBMODULES_DIR, "do")

        if not os.path.exists(utils_path):
            log.exit("%s path not found", utils_path)
        if not os.path.exists(do_path):
            log.exit("%s path not found", do_path)

        utils_repo = self.gits.get('utils')
        do_repo = self.gits.get('do')

        utils_switched = False
        b = gitter.get_active_branch(utils_repo)

        if b is None:
            log.error("Unable to read local utils repository")
        elif b == version:
            log.info("Utilities repository already at %s", version)
        elif gitter.switch_branch(utils_repo, version):
            log.info("Utilities repository switched to %s", version)
            utils_switched = True
        else:
            log.exit("Unable to switch utilities repository to %s", version)

        b = gitter.get_active_branch(do_repo)

        if b is None:
            log.error("Unable to read local controller repository")
        elif b == version:
            log.info("Controller repository already at %s", version)
        elif gitter.switch_branch(do_repo, version):
            log.info("Controller repository switched to %s", version)
        else:
            if utils_switched:
                log.warning("Unable to switch back utilities repository")
            log.exit("Unable to switch controller repository to %s", version)

        installed = install(utils_path, editable=True)
        if installed:
            installed = install(do_path, editable=True)

        if not installed:
            log.error("Unable to install controller %s from local folder", version)
        else:
            log.info("Controller version %s installed from local folder", version)
            installed_version = check_version(package)
            log.info("Check on installed version: %s", installed_version)

    # issues/57
    # I'm temporary here... to be decided how to handle me
    @staticmethod
    def get_reserved_project_names():
        names = [
            'abc',
            'attr',
            'base64',
            'better_exceptions',
            'bravado_core',
            'celery',
            'click',
            'collections',
            'datetime',
            'dateutil',
            'elasticsearch_dsl',
            'email',
            'errno',
            'flask',
            'flask_injector',
            'flask_oauthlib',
            'flask_restful',
            'flask_sqlalchemy',
            'functools',
            'glob',
            'hashlib',
            'hmac',
            'injector',
            'inspect',
            'io',
            'irods',
            'iRODSPickleSession',
            'json',
            'jwt',
            'logging',
            'neo4j',
            'neomodel',
            'os',
            'platform',
            'pickle',
            'plumbum',
            'pymodm',
            'pymongo',
            'pyotp',
            'pyqrcode',
            'pytz',
            'random',
            're',
            'smtplib',
            'socket',
            'sqlalchemy',
            'string',
            'submodules',
            'sys',
            'time',
            'unittest',
            'werkzeug',
        ]
        return names

    @staticmethod
    def get_vars_to_services_mapping():
        return {
            'CELERYUI_USER': ['celeryui'],
            'CELERYUI_PASSWORD': ['celeryui'],
            'ALCHEMY_USER': ['postgres', 'mariadb'],
            'ALCHEMY_PASSWORD': ['postgres', 'mariadb'],
            'GRAPHDB_PASSWORD': ['neo4j'],
            'IRODS_ANONYMOUS': ['icat'],
        }

    @staticmethod
    def normalize_placeholder_variable(key):
        if key == 'NEO4J_AUTH':
            return 'GRAPHDB_PASSWORD'

        if key == 'POSTGRES_USER':
            return 'ALCHEMY_USER'
        if key == 'POSTGRES_PASSWORD':
            return 'ALCHEMY_PASSWORD'

        if key == 'MYSQL_USER':
            return 'ALCHEMY_USER'
        if key == 'MYSQL_PASSWORD':
            return 'ALCHEMY_PASSWORD'

        return key
