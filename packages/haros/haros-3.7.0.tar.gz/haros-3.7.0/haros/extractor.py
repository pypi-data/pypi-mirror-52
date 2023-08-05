
#Copyright (c) 2017 Andre Santos
#
#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in
#all copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
#THE SOFTWARE.

###############################################################################
# Imports
###############################################################################

import logging
from operator import attrgetter
import os
import re
import subprocess
from urllib2 import urlopen, URLError
import xml.etree.ElementTree as ET
import yaml

from bonsai.model import CodeGlobalScope, pretty_str
from bonsai.cpp.model import CppFunctionCall, CppDefaultArgument, CppOperator
from bonsai.analysis import (
    CodeQuery, resolve_reference, resolve_expression, get_control_depth,
    get_conditions, is_under_loop
)
try:
    from bonsai.cpp.clang_parser import CppAstParser
except ImportError:
    CppAstParser = None
from rospkg import RosPack, RosStack, ResourceNotFound

from .cmake_parser import RosCMakeParser
from .launch_parser import LaunchParser, LaunchParserError
from .metamodel import (
    Project, Repository, Package, SourceFile, Node, Person, SourceCondition,
    Publication, Subscription, ServiceServerCall, ServiceClientCall, Location,
    ReadParameterCall, WriteParameterCall
)
from .util import cwd


###############################################################################
# Utility
###############################################################################

class LoggingObject(object):
    log = logging.getLogger(__name__)


###############################################################################
# Source Extractor
###############################################################################

class ProjectExtractor(LoggingObject):
    def __init__(self, index_file, env = None, pkg_cache = None,
                 repo_cache = None, repo_path = None, distro_url = None,
                 require_repos = False, parse_nodes = False, node_cache = None):
        self.log.debug("ProjectExtractor(%s, %s, %s)",
                       index_file, repo_path, distro_url)
        self.index_file = index_file
        self.repo_path = repo_path
        self.distribution = distro_url
        self.require_repos = require_repos
        self.parse_nodes = parse_nodes
        self.environment = env if not env is None else {}
        self.package_cache = pkg_cache if not pkg_cache is None else {}
        self.repo_cache = repo_cache if not repo_cache is None else {}
        self.node_cache = node_cache if not node_cache is None else {}
        self.project = None
        self.packages = None
        self.missing = None
        self.repositories = None
        self.configurations = None
        self.node_specs = None
        self.rules = None

    def index_source(self, settings=None):
        self.log.debug("ProjectExtractor.index_source()")
        self._setup()
        self._load_user_repositories()
        self._find_local_packages()
        if self.missing and self.distribution:
            self._load_distro_repositories()
            self._find_local_packages()
        self._topological_sort()
        for name in self.missing:
            self.log.warning("Could not find package " + name)
        self._populate_packages_and_dependencies(settings=settings)
        self._update_node_cache()
        self._find_nodes(settings)

    def _setup(self):
        try:
            with open(self.index_file, "r") as handle:
                data = yaml.safe_load(handle)
        except IOError as e:
            data = {}
        self.project = Project(data.get("project", "default"))
        self.repositories = data.get("repositories", {})
        self.packages = set(data.get("packages")
                            or RosPack.get_instance(["."]).list())
        self.missing = set(self.packages)
        self.configurations = data.get("configurations", {})
        self.node_specs = data.get("nodes", {})
        self.rules = data.get("rules", {})

    def _load_user_repositories(self):
        self.log.info("Looking up user provided repositories.")
        extractor = RepositoryExtractor()
        for name, data in self.repositories.iteritems():
            repo = self.repo_cache.get(name)
            if repo:
                self.project.repositories.append(repo)
            else:
                extractor.load_from_user(name, data, project = self.project)
        if self.repo_path:
            try:
                extractor.download(self.repo_path)
            except RepositoryCloneError as e:
                if self.require_repos:
                    raise e
                else:
                    self.log.warning("Could not download all repositories.")

    def _find_local_packages(self):
        self.log.info("Looking for packages locally.")
        cdir = os.path.abspath(".")
        alt_paths = [self.repo_path, cdir] if self.repo_path else [cdir]
        extractor = PackageExtractor(alt_paths = alt_paths)
        extractor.refresh_package_cache()
        found = []
        for name in self.missing:
            pkg = self.package_cache.get(name)
            if pkg:
                self.project.packages.append(pkg)
                found.append(name)
            elif extractor.find_package(name, project = self.project):
                found.append(name)
        self.missing.difference_update(found)

    def _load_distro_repositories(self):
        self.log.info("Looking up repositories from official distribution.")
        try:
            data = yaml.safe_load(urlopen(self.distribution).read())["repositories"]
        except URLError as e:
            self.log.warning("Could not download distribution data.")
            return
        extractor = RepositoryExtractor()
        extractor.load_needed_from_distro(data, self.missing, self.project)
        if self.repo_path:
            try:
                extractor.download(self.repo_path)
            except RepositoryCloneError as e:
                if self.require_repos:
                    raise e
                else:
                    self.log.warning("Could not download all repositories.")

    def _topological_sort(self):
        dependencies = {}
        pending = list(self.project.packages)
        for pkg in self.project.packages:
            pkg.topological_tier = -1
            dependencies[pkg.id] = set(p for p in pkg.dependencies.packages
                                       if p in self.packages)
        tier = 1
        emitted = []
        while pending:
            next_pending = []
            next_emitted = []
            for pkg in pending:
                deps = dependencies[pkg.id]
                deps.difference_update(emitted)
                if deps:
                    next_pending.append(pkg)
                else:
                    pkg.topological_tier = tier
                    next_emitted.append(pkg.name)
            if not next_emitted:
                # cyclic dependencies detected
                self.log.warning("Cyclic dependencies: %s", next_pending)
                for pkg in next_pending:
                    pkg.topological_tier = tier
                next_pending = None
            pending = next_pending
            emitted = next_emitted
            tier += 1
        self.project.packages.sort(key = attrgetter("topological_tier", "id"))

    def _populate_packages_and_dependencies(self, settings=None):
        found = set()
        extractor = PackageExtractor()
        extractor.packages = self.project.packages
        for pkg in self.project.packages:
            found.add(pkg.name)
            analysis_ignore = extractor._populate_package(pkg)
            if settings is not None:
                settings.ignored_lines.update(analysis_ignore)
        deps = extractor._extra
        extractor._extra = []
        while deps:
            pkg = deps.pop()
            assert pkg.name not in found
            pkg._analyse = False
            found.add(pkg.name)
            self.project.packages.append(pkg)
            analysis_ignore = extractor._populate_package(pkg)
            if settings is not None:
                settings.ignored_lines.update(analysis_ignore)
            deps.extend(extractor._extra)
            extractor._extra = []

    def _find_nodes(self, settings):
        pkgs = {pkg.name: pkg for pkg in self.project.packages if pkg._analyse}
        ws = settings.workspace if settings else None
        if CppAstParser is None:
            self.log.warning("C++ AST parser not found.")
        extractor = NodeExtractor(pkgs, self.environment, ws = ws,
                                  node_cache = self.node_cache,
                                  parse_nodes = self.parse_nodes)
        if self.parse_nodes and CppAstParser is not None:
            if settings is None:
                CppAstParser.set_library_path()
                db_dir = os.path.join(extractor.workspace, "build")
                if os.path.isfile(
                        os.path.join(db_dir, "compile_commands.json")):
                    CppAstParser.set_database(db_dir)
            else:
                CppAstParser.set_library_path(settings.cpp_parser_lib)
                CppAstParser.set_standard_includes(settings.cpp_includes)
                db_dir = settings.cpp_compile_db
                if db_dir and os.path.isfile(
                        os.path.join(db_dir, "compile_commands.json")):
                    CppAstParser.set_database(settings.cpp_compile_db)
        for pkg in self.project.packages:
            if pkg._analyse and pkg.name not in self.package_cache:
                extractor.find_nodes(pkg)

    def _update_node_cache(self):
        self.log.debug("Importing cached Nodes.")
        data = [datum for datum in self.node_cache.itervalues()]
        self.node_cache = {}
        for datum in data:
            try:
                pkg = self._get_package(datum["package"])
                source_files = self._get_files(pkg, datum["files"])
            except ValueError as e:
                # either a package or a file is no longer part of the analysis
                self.log.debug("Cached node %s: %s", datum["name"], e)
                continue
            mtime = datum["timestamp"]
            for sf in source_files:
                if sf.timestamp > mtime:
                    # a file was modified, needs to be parsed again
                    continue
            node = Node(datum["name"], pkg, rosname = datum["rosname"],
                        nodelet = datum["nodelet"])
            node.source_files = source_files
            for p in datum["advertise"]:
                node.advertise.append(self._pub_from_JSON(p))
            for p in datum["subscribe"]:
                node.subscribe.append(self._sub_from_JSON(p))
            for p in datum["service"]:
                node.service.append(self._srv_from_JSON(p))
            for p in datum["client"]:
                node.client.append(self._client_from_JSON(p))
            for p in datum["readParam"]:
                node.read_param.append(self._read_from_JSON(p))
            for p in datum["writeParam"]:
                node.write_param.append(self._write_from_JSON(p))
            self.node_cache[node.node_name] = node

    def _get_package(self, name):
        for pkg in self.project.packages:
            if pkg.name == name:
                return pkg
        raise ValueError("cannot find package: " + name)

    def _get_files(self, pkg, filenames):
        files = []
        for filename in filenames:
            found = False
            for sf in pkg.source_files:
                if sf.full_name == filename:
                    found = True
                    files.append(sf)
                    break
            if not found:
                raise ValueError("cannot find file: " + filename)
        return files

    def _pub_from_JSON(self, datum):
        l = self._location_from_JSON
        cs = [SourceCondition(c["condition"], location = l(c["location"]))
              for c in datum["conditions"]]
        return Publication(datum["name"], datum["namespace"], datum["type"],
                           datum["queue"], control_depth = datum["depth"],
                           repeats = datum["repeats"],
                           conditions = cs, location = l(datum["location"]))

    def _sub_from_JSON(self, datum):
        l = self._location_from_JSON
        cs = [SourceCondition(c["condition"], location = l(c["location"]))
              for c in datum["conditions"]]
        return Subscription(datum["name"], datum["namespace"], datum["type"],
                            datum["queue"], control_depth = datum["depth"],
                            repeats = datum["repeats"],
                            conditions = cs, location = l(datum["location"]))

    def _srv_from_JSON(self, datum):
        l = self._location_from_JSON
        cs = [SourceCondition(c["condition"], location = l(c["location"]))
              for c in datum["conditions"]]
        return ServiceServerCall(datum["name"], datum["namespace"],
                                 datum["type"], control_depth = datum["depth"],
                                 repeats = datum["repeats"],
                                 conditions = cs,
                                 location = l(datum["location"]))

    def _client_from_JSON(self, datum):
        l = self._location_from_JSON
        cs = [SourceCondition(c["condition"], location = l(c["location"]))
              for c in datum["conditions"]]
        return ServiceClientCall(datum["name"], datum["namespace"],
                                 datum["type"], control_depth = datum["depth"],
                                 repeats = datum["repeats"],
                                 conditions = cs,
                                 location = l(datum["location"]))

    def _read_from_JSON(self, datum):
        l = self._location_from_JSON
        cs = [SourceCondition(c["condition"], location = l(c["location"]))
              for c in datum["conditions"]]
        return ReadParameterCall(datum["name"], datum["namespace"],
                                 datum["type"], control_depth = datum["depth"],
                                 repeats = datum["repeats"],
                                 conditions = cs,
                                 location = l(datum["location"]))

    def _write_from_JSON(self, datum):
        l = self._location_from_JSON
        cs = [SourceCondition(c["condition"], location = l(c["location"]))
              for c in datum["conditions"]]
        return WriteParameterCall(datum["name"], datum["namespace"],
                                  datum["type"], control_depth = datum["depth"],
                                  repeats = datum["repeats"],
                                  conditions = cs,
                                  location = l(datum["location"]))

    def _location_from_JSON(self, datum):
        try:
            pkg = self._get_package(datum["package"])
            sf = None
            filename = datum["file"]
            if filename:
                sf = self._get_files(pkg, [filename])[0]
        except ValueError:
            return None
        return Location(pkg, file = sf, line = datum["line"],
                        fun = datum["function"], cls = datum["class"])


###############################################################################
# Repository Extractor
###############################################################################

class RepositoryCloneError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)


class RepositoryExtractor(LoggingObject):
    def __init__(self):
        self.repositories = []
        self.declared_packages = set()

    def load_from_user(self, name, data, project = None):
        self.log.debug("RepositoryExtractor.from_user(%s, %s)", name, data)
        repo = Repository(name, proj = project)
        repo.status = "private"
        repo.vcs = data["type"]
        repo.url = data["url"]
        repo.version = data["version"]
        repo.declared_packages = data["packages"]
        self.repositories.append(repo)
        self.declared_packages.update(repo.declared_packages)
        if project:
            project.repositories.append(repo)
        return repo

    def load_from_distro(self, name, data, project = None):
        self.log.debug("RepositoryExtractor.from_distro(%s, %s)", name, data)
        if not "source" in data:
            self.log.debug("There is no source in provided data.")
            return
        repo = Repository(name, proj = project)
        repo.status = data.get("status")
        src = data["source"]
        repo.vcs = src["type"]
        repo.url = src["url"]
        repo.version = src["version"]
        if "release" in data:
            repo.declared_packages = data["release"].get("packages", [name])
        self.repositories.append(repo)
        self.declared_packages.update(repo.declared_packages)
        if project:
            project.repositories.append(repo)
        return repo

    def load_needed_from_distro(self, data, pkgs, project = None):
        if not pkgs:
            return True
        remaining = set(pkgs)
        for name, info in data.iteritems():
            if not "release" in info:
                continue
            for pkg in info["release"].get("packages", [name]):
                try:
                    remaining.remove(pkg)
                    self.load_from_distro(name, info, project = project)
                except KeyError as e:
                    pass
            if not remaining:
                break
        return not remaining

    def download(self, repo_path):
        self.log.debug("RepositoryExtractor.download(%s)", repo_path)
        for repo in self.repositories:
            if not repo.url:
                self.log.debug("%s has no URL to download from.", repo.id)
                continue
            path = os.path.join(repo_path, repo.name)
            clone = False
            if not os.path.exists(path):
                os.makedirs(path)
                clone = True
            with cwd(path):
                if repo.vcs == "git":
                    self._download_git(repo, path, clone)
                elif repo.vcs == "hg":
                    self._download_hg(repo, path, clone)
                elif repo.vcs == "svn":
                    self._download_svn(repo, path, clone)
        return True

    GIT_INIT = ("git", "init")
    GIT_PULL = ("git", "pull")
    GIT_COUNT = ("git", "rev-list", "HEAD", "--count")

    def _download_git(self, repo, path, clone = False):
        self.log.debug("RepositoryExtractor._download_git(%s)", path)
        try:
            if clone:
                subprocess.check_call(self.GIT_INIT)
                subprocess.check_call(["git", "remote",
                                       "add", "-t", repo.version,
                                       "-f", "origin", repo.url])
                subprocess.check_call(["git", "checkout", repo.version])
            else:
                subprocess.check_call(self.GIT_PULL)
            repo.path = path
            repo.commits = int(subprocess.check_output(self.GIT_COUNT).rstrip())
        except subprocess.CalledProcessError as e:
            raise RepositoryCloneError("git error: " + str(e))

    HG_PULL = ("hg", "pull")
    HG_COUNT = ("hg", "id", "--num", "--rev", "tip")

    def _download_hg(self, repo, path, clone = False):
        self.log.debug("RepositoryExtractor._download_hg(%s)", path)
        try:
            if clone:
                subprocess.check_call(["hg", "clone", repo.url,
                                       "-r", repo.version])
            else:
                subprocess.check_call(self.HG_PULL)
            repo.path = path
            repo.commits = int(subprocess.check_output(self.HG_COUNT).rstrip())
        except subprocess.CalledProcessError as e:
            raise RepositoryCloneError("hg error: " + str(e))

    SVN_FETCH = ("git", "svn", "fetch")

    def _download_svn(self, repo, path, clone = False):
        self.log.debug("RepositoryExtractor._download_svn(%s)", path)
        try:
            if clone:
                if repo.version == "trunk":
                    version = repo.version
                else:
                    version = "branches/" + repo.version
                subprocess.check_call(["git", "svn", "clone",
                                       "-T", version, repo.url])
            else:
                subprocess.check_call(self.SVN_FETCH)
            self.path = path
            self.commits = int(subprocess.check_output(self.GIT_COUNT).rstrip())
        except subprocess.CalledProcessError as e:
            raise RepositoryCloneError("git-svn error: " + str(e))


###############################################################################
# Package Extractor
###############################################################################

class PackageExtractor(LoggingObject):
    def __init__(self, alt_paths = None):
        self.packages = []
        self.rospack = RosPack.get_instance()
        self.rosstack = RosStack.get_instance()
        if alt_paths is None:
            self.altpack = self.rospack
            self.altstack = self.rosstack
        else:
            self.altpack = RosPack.get_instance(alt_paths)
            self.altstack = RosStack.get_instance(alt_paths)
        self._pkg_cache = {}
        self._extra = []

    # Note: this method messes with private variables of the RosPack
    # class. This is needed because, at some point, we download new
    # repositories and the package cache becomes outdated.
    # RosPack provides no public method to refresh the cache, hence
    # changing private variables directly.
    def refresh_package_cache(self):
        self.rospack._location_cache = None
        self.altpack._location_cache = None
        self.rosstack._location_cache = None
        self.altstack._location_cache = None

    # To use with LaunchParser.
    def get(self, pkg_id):
        if pkg_id in self._pkg_cache:
            return self._pkg_cache[pkg_id]
        for pkg in self.packages:
            if pkg.id == pkg_id:
                self._pkg_cache[pkg_id] = pkg
                return pkg
        try:
            assert pkg_id.startswith("package:")
            pkg = self._find(pkg_id[8:], None)
            self._pkg_cache[pkg_id] = pkg
            self._extra.append(pkg)
        except (IOError, ET.ParseError, ResourceNotFound):
            return None
        return pkg

    def find_package(self, name, project=None, analyse=True):
        try:
            pkg = self._find(name, project)
            pkg._analyse = analyse
            self.packages.append(pkg)
            if project:
                project.packages.append(pkg)
                for repo in project.repositories:
                    if name in repo.declared_packages:
                        pkg.repository = repo
                        repo.packages.append(pkg)
                        break
            # self._populate_package(pkg)
        except (IOError, ET.ParseError, ResourceNotFound):
            return None
        return pkg

    def _find(self, name, project):
        try:
            path = self.altpack.get_path(name)
        except ResourceNotFound:
            try:
                path = self.altstack.get_path(name)
            except ResourceNotFound:
                try:
                    path = self.rospack.get_path(name)
                except ResourceNotFound:
                    path = self.rosstack.get_path(name)
        return PackageParser.parse(os.path.join(path, "package.xml"),
                                   project = project)

    EXCLUDED = (".git", "doc", "bin", "cmake")

    def _populate_package(self, pkg):
        self.log.debug("PackageExtractor.populate(%s)", pkg)
        if not pkg.path:
            self.log.debug("Package %s has no path", pkg.name)
            return
        self.log.info("Indexing source files for package %s", pkg.name)
        analysis_ignore = {}
        #pkgs = {pkg.id: pkg for pkg in self.packages}
        launch_parser = LaunchParser(pkgs=self)
        prefix = len(pkg.path) + len(os.path.sep)
        for root, subdirs, files in os.walk(pkg.path, topdown=True):
            subdirs[:] = [d for d in subdirs if d not in self.EXCLUDED]
            path = root[prefix:]
            for filename in files:
                self.log.debug("Found file %s at %s", filename, path)
                source = SourceFile(filename, path, pkg)
                ignore = source.set_file_stats()
                if any(v for v in ignore.itervalues()):
                    analysis_ignore[source.id] = ignore
                if pkg._analyse and source.language == "launch":
                    self.log.info("Parsing launch file: " + source.path)
                    try:
                        source.tree = launch_parser.parse(source.path)
                    except LaunchParserError as e:
                        self.log.warning("Parsing error in %s:\n%s",
                                         source.path, str(e))
                pkg.source_files.append(source)
                pkg.size += source.size
                pkg.lines += source.lines
                pkg.sloc += source.sloc
        return analysis_ignore


###############################################################################
# Package Parser
###############################################################################

class PackageParser(LoggingObject):
    @staticmethod
    def parse(pkg_file, project = None):
        PackageParser.log.debug("PkgParser.parse(%s, %s)", pkg_file, project)
        with open(pkg_file, "r") as handle:
            root = ET.parse(handle).getroot()
        name = root.find("name").text.strip()
        package = Package(name, proj = project)
        package.path = os.path.dirname(pkg_file)
        PackageParser.log.info("Found package %s at %s", package, package.path)
        PackageParser._parse_metadata(root, package)
        PackageParser._parse_export(root, package)
        PackageParser._parse_dependencies(root, package)
        return package

    @staticmethod
    def _parse_metadata(xml, package):
        package.description = xml.find("description").text.strip()
        for el in xml.findall("maintainer"):
            name = el.text.strip() or "?"
            email = el.get("email") or "email@example.com"
            package.maintainers.add(Person(name, email))
        for el in xml.findall("author"):
            name = el.text.strip() or "?"
            email = el.get("email") or "email@example.com"
            package.authors.add(Person(name, email))
        for el in xml.findall("license"):
            package.licenses.add(el.text.strip())
        for el in xml.findall("url"):
            value = el.get("type")
            if value is None or value == "website":
                if el.text:
                    package.website = el.text.strip()
            elif value == "repository":
                if el.text:
                    package.vcs_url = el.text.strip()
            elif value == "bugtracker":
                if el.text:
                    package.bug_url = el.text.strip()
        el = xml.find("version")
        if el is not None:
            package.version = el.text.strip()

    @staticmethod
    def _parse_export(xml, package):
        el = xml.find("export")
        if not el is None:
            package.is_metapackage = not el.find("metapackage") is None
            if not el.find("nodelet") is None:
                nodelets = el.find("nodelet").get("plugin")
                nodelets = nodelets.replace("${prefix}", package.path)
                with open(nodelets, "r") as handle:
                    root = ET.parse(handle).getroot()
                PackageParser.log.info("Found nodelets at %s", nodelets)
                if root.tag == "library":
                    libs = (root,)
                else:
                    libs = root.findall("library")
                for el in libs:
                    libname = el.get("path").rsplit(os.sep)[-1]
                    for cl in el.findall("class"):
                        nodelet = cl.get("type").split("::")[-1]
                        node = Node(libname, package, nodelet = nodelet)
                        package.nodes.append(node)

    @staticmethod
    def _parse_dependencies(xml, package):
        sources = ["build_depend"]
        if xml.get("format") == "2":
            sources.extend(("depend", "build_export_depend", "exec_depend"))
        else:
            sources.append("run_depend")
        for src in sources:
            for el in xml.findall(src):
                name = el.text.strip()
                if name:
                    package.dependencies.packages.add(name)


###############################################################################
# Hard-coded Node Parser
###############################################################################

class HardcodedNodeParser(LoggingObject):
    model_dir = None
    distro = None
    _cache = {}

    @classmethod
    def get(cls, pkg, node_type):
        cls.log.debug("Fetching hard-coded node: (%s, %s, %s)",
                      pkg, node_type, cls.distro)
        node_id = "node:" + pkg + "/" + node_type
        if node_id in cls._cache:
            cls.log.debug("Node already in cache.")
            return cls._cache[node_id]
        filename = os.path.join(cls.model_dir, pkg + ".yaml")
        try:
            with open(filename) as handle:
                data = yaml.load(handle)
        except IOError as e:
            cls.log.debug("YAML file not found: %s", filename)
            return None
        if not cls.distro in data:
            cls.log.debug("Package has no data for ROS %s.", cls.distro)
            return None
        if not node_type in data[cls.distro]:
            cls.log.debug("Node does not exist for ROS %s.", cls.distro)
            return None
        cls.log.debug("Building node from YAML data.")
        node = cls._build_node(node_type, cls.distro, Package(pkg), data)
        cls._cache[node_id] = node
        return node

    @classmethod
    def _build_node(cls, node_type, distro, pkg, data):
        node_data = data[distro][node_type]
        base = node_data.get("base")
        if base:
            node = cls._build_node(node_type, base, pkg, data)
        else:
            node = Node(node_type, pkg, rosname = node_data.get("rosname"),
                        nodelet = node_type if node_data["nodelet"] else None)
        for datum in node_data.get("advertise", ()):
            pub = Publication(datum["name"], datum["namespace"],
                    datum["type"], datum["queue"],
                    control_depth = datum["depth"],
                    repeats = datum["repeats"],
                    conditions = [SourceCondition(c)
                                  for c in datum["conditions"]])
            node.advertise.append(pub)
        for datum in node_data.get("subscribe", ()):
            sub = Subscription(datum["name"], datum["namespace"],
                    datum["type"], datum["queue"],
                    control_depth = datum["depth"],
                    repeats = datum["repeats"],
                    conditions = [SourceCondition(c)
                                  for c in datum["conditions"]])
            node.subscribe.append(sub)
        for datum in node_data.get("service", ()):
            srv = ServiceServerCall(datum["name"], datum["namespace"],
                    datum["type"], control_depth = datum["depth"],
                    repeats = datum["repeats"],
                    conditions = [SourceCondition(c)
                                  for c in datum["conditions"]])
            node.service.append(srv)
        for datum in node_data.get("client", ()):
            cli = ServiceClientCall(datum["name"], datum["namespace"],
                    datum["type"], control_depth = datum["depth"],
                    repeats = datum["repeats"],
                    conditions = [SourceCondition(c)
                                  for c in datum["conditions"]])
            node.client.append(cli)
        for datum in node_data.get("readParam", ()):
            par = ReadParameterCall(datum["name"], datum["namespace"],
                    datum["type"], control_depth = datum["depth"],
                    repeats = datum["repeats"],
                    conditions = [SourceCondition(c)
                                  for c in datum["conditions"]])
            node.read_param.append(par)
        for datum in node_data.get("writeParam", ()):
            par = WriteParameterCall(datum["name"], datum["namespace"],
                    datum["type"], control_depth = datum["depth"],
                    repeats = datum["repeats"],
                    conditions = [SourceCondition(c)
                                  for c in datum["conditions"]])
            node.write_param.append(par)
        return node


###############################################################################
# Node Extractor
###############################################################################

class NodeExtractor(LoggingObject):
    def __init__(self, pkgs, env, ws = None, node_cache = None,
                 parse_nodes = False):
        self.package = None
        self.packages = pkgs
        self.environment = env
        self.workspace = ws or self._find_workspace()
        self.node_cache = node_cache
        self.parse_nodes = parse_nodes
        self.nodes = []

    def find_nodes(self, pkg):
        self.log.debug("NodeExtractor.find_nodes(%s)", pkg)
        self.package = pkg
        srcdir = self.package.path[len(self.workspace):]
        srcdir = os.path.join(self.workspace, srcdir.split(os.sep, 1)[0])
        bindir = os.path.join(self.workspace, "build")
        parser = RosCMakeParser(srcdir, bindir, pkgs = self.packages,
                                env = self.environment,
                                vars = self._default_variables())
        parser.parse(os.path.join(self.package.path, "CMakeLists.txt"))
        self._update_nodelets(parser.libraries)
        self._register_nodes(parser.executables)
        if self.parse_nodes:
            self._extract_primitives()

    def _find_workspace(self):
        """This replicates the behaviour of `roscd`."""
        ws = self.environment.get("ROS_WORKSPACE")
        if ws:
            return ws
        paths = self.environment.get("CMAKE_PREFIX_PATH", "").split(os.pathsep)
        for path in paths:
            if os.path.exists(os.path.join(path, ".catkin")):
                if (path.endswith(os.sep + "devel")
                        or path.endswith(os.sep + "install")):
                    return os.path.abspath(os.path.join(path, os.pardir))
        raise KeyError("ROS_WORKSPACE")

    def _default_variables(self):
    # TODO: clean up these hardcoded values
        v = {}
        v["catkin_INCLUDE_DIRS"] = os.path.join(self.workspace, "devel/include")
        v["Boost_INCLUDE_DIRS"] = "/usr/include/"
        v["Eigen_INCLUDE_DIRS"] = "/usr/include/eigen3"
        v["ImageMagick_INCLUDE_DIRS"] = "/usr/include/ImageMagick"
        v["PROJECT_SOURCE_DIR"] = self.package.path
        return v

    def _get_file(self, path):
        for sf in self.package.source_files:
            if sf.path == path:
                return sf
        return None

    def _update_nodelets(self, libraries):
        lib_files = {}
        for target in libraries.itervalues():
            files = []
            for path in target.files:
                sf = self._get_file(path)
                if sf:
                    files.append(sf)
            for link in target.links:
                for path in link.files:
                    sf = self._get_file(path)
                    if sf:
                        files.append(sf)
            lib_files[target.prefixed_name] = files
        for nodelet in self.package.nodes:
            if not nodelet.is_nodelet:
                continue
            if nodelet.name in lib_files:
                nodelet.source_files = lib_files[nodelet.name]

    def _register_nodes(self, executables):
        for target in executables.itervalues():
            node = Node(target.output_name, self.package)
            for path in target.files:
                sf = self._get_file(path)
                if sf:
                    node.source_files.append(sf)
            for link in target.links:
                for path in link.files:
                    sf = self._get_file(path)
                    if sf:
                        node.source_files.append(sf)
            self.nodes.append(node)
            self.package.nodes.append(node)

    def _extract_primitives(self):
        for i in xrange(len(self.package.nodes)):
            node = self.package.nodes[i]
            self.log.debug("Extracting primitives for node %s", node.id)
            if node.source_tree is not None:
                self.log.debug("Node already has a source tree. Skipped.")
                continue
            if node.node_name in self.node_cache:
                self.log.debug("Using Node %s from cache.", node.node_name)
                node = self.node_cache[node.node_name]
                assert node.package is self.package
                self.package.nodes[i] = node
                continue
            node.source_tree = CodeGlobalScope()
            node.advertise = []
            node.subscribe = []
            node.service = []
            node.client = []
            node.read_param = []
            node.write_param = []
            if not node.source_files:
                self.log.warning("no source files for node " + node.id)
            if node.language == "cpp" and CppAstParser is not None:
                self._roscpp_analysis(node)
            elif node.language != "cpp":
                self.log.debug("Node written in %s.", node.language)

    def _roscpp_analysis(self, node):
        self.log.debug("Parsing C++ files for node %s", node.id)
        parser = CppAstParser(workspace = self.workspace)
        for sf in node.source_files:
            self.log.debug("Parsing C++ file %s", sf.path)
            if parser.parse(sf.path) is None:
                self.log.warning("no compile commands for " + sf.path)
        node.source_tree = parser.global_scope
    # ----- queries after parsing, since global scope is reused ---------------
        self._query_comm_primitives(node, parser.global_scope)
        self._query_nh_param_primitives(node, parser.global_scope)
        self._query_param_primitives(node, parser.global_scope)

    def _query_comm_primitives(self, node, gs):
        for call in CodeQuery(gs).all_calls.where_name("advertise").get():
            if call.canonical_type != "ros::Publisher":
                continue
            self._on_publication(node,
                self._resolve_node_handle(call.method_of), call)
        for call in CodeQuery(gs).all_calls.where_name("subscribe").get():
            if call.canonical_type != "ros::Subscriber":
                continue
            self._on_subscription(node,
                self._resolve_node_handle(call.method_of), call)
        for call in CodeQuery(gs).all_calls.where_name("advertiseService").get():
            if call.canonical_type != "ros::ServiceServer":
                continue
            self._on_service(node,
                self._resolve_node_handle(call.method_of), call)
        for call in CodeQuery(gs).all_calls.where_name("serviceClient").get():
            if call.canonical_type != "ros::ServiceClient":
                continue
            self._on_client(node,
                self._resolve_node_handle(call.method_of), call)
        self.log.debug("Looking for image_transport::SubscriberFilter calls.")
        for call in CodeQuery(gs).all_calls.where_name("SubscriberFilter").get():
            self.log.debug("Found: %s", call.pretty_str())
            self.log.debug("%s", type(call))
            self.log.debug("%s", call.__dict__)
            if isinstance(call.reference, str):
                if not call.reference.startswith("c:@N@image_transport@S@SubscriberFilter"):
                    continue
            if not "image_transport::SubscriberFilter" in call.canonical_type:
                continue
            n = call.arguments[0] if call.arguments else None
            self._on_subscription(node, self._resolve_it_node_handle(n),
                                  call, topic_pos = 1, queue_pos = 2,
                                  msg_type = "sensor_msgs/Image")
        self.log.debug("Looking for message_filters::Subscriber calls.")
        for call in CodeQuery(gs).all_calls.where_name("Subscriber").get():
            self.log.debug("Found: %s", call.pretty_str())
            self.log.debug("%s", type(call))
            self.log.debug("%s", call.__dict__)
            if isinstance(call.reference, str):
                if not call.reference.startswith("c:@N@message_filters@S@Subscriber"):
                    continue
            if not "message_filters::Subscriber" in call.canonical_type:
                continue
            n = call.arguments[0] if call.arguments else None
            self._on_subscription(node, self._resolve_node_handle(n),
                                  call, topic_pos = 1, queue_pos = 2)
        self.log.debug("Looking for image_transport::Subscriber calls.")
        for call in CodeQuery(gs).all_calls.where_name("subscribe").get():
            if call.canonical_type != "image_transport::Subscriber":
                continue
            self.log.debug("Found: %s", call.pretty_str())
            self.log.debug("%s", type(call))
            self.log.debug("%s", call.__dict__)
            n = call.method_of if call.method_of else None
            self._on_subscription(node, self._resolve_it_node_handle(n),
                                  call, msg_type = "sensor_msgs/Image")
        self.log.debug("Looking for image_transport::Publisher.")
        for call in CodeQuery(gs).all_calls.where_name("advertise").get():
            if call.canonical_type != "image_transport::Publisher":
                continue
            self.log.debug("Found: %s", call.pretty_str())
            self.log.debug("%s", type(call))
            self.log.debug("%s", call.__dict__)
            n = call.method_of if call.method_of else None
            self._on_publication(node, self._resolve_it_node_handle(n),
                                 call, msg_type = "sensor_msgs/Image")

    def _query_nh_param_primitives(self, node, gs):
        nh_prefix = "c:@N@ros@S@NodeHandle@"
        reads = ("getParam", "getParamCached", "param", "hasParam", "searchParam")
        for call in CodeQuery(gs).all_calls.where_name(reads).get():
            if (call.full_name.startswith("ros::NodeHandle")
                    or (isinstance(call.reference, str)
                        and call.reference.startswith(nh_prefix))):
                self._on_read_param(node,
                    self._resolve_node_handle(call.method_of), call)
        writes = ("setParam", "deleteParam")
        for call in CodeQuery(gs).all_calls.where_name(writes).get():
            if (call.full_name.startswith("ros::NodeHandle")
                    or (isinstance(call.reference, str)
                        and call.reference.startswith(nh_prefix))):
                self._on_write_param(node,
                    self._resolve_node_handle(call.method_of), call)

    def _query_param_primitives(self, node, gs):
        ros_prefix = "c:@N@ros@N@param@"
        reads = ("get", "getCached", "param", "has")
        for call in CodeQuery(gs).all_calls.where_name(reads).get():
            if (call.full_name.startswith("ros::param")
                    or (isinstance(call.reference, str)
                        and call.reference.startswith(ros_prefix))):
                self._on_read_param(node, "", call)
        for call in (CodeQuery(gs).all_calls.where_name("search")
                     .where_result("bool").get()):
            if (call.full_name.startswith("ros::param")
                    or (isinstance(call.reference, str)
                        and call.reference.startswith(ros_prefix))):
                if len(call.arguments) > 2:
                    ns = resolve_expression(call.arguments[0])
                    if not isinstance(ns, basestring):
                        ns = "?"
                else:
                    ns = "~"
                self._on_read_param(node, ns, call)
        writes = ("set", "del")
        for call in CodeQuery(gs).all_calls.where_name(writes).get():
            if (call.full_name.startswith("ros::param")
                    or (isinstance(call.reference, str)
                        and call.reference.startswith(ros_prefix))):
                self._on_write_param(node, "", call)

    def _on_publication(self, node, ns, call, topic_pos=0, queue_pos=1,
                        msg_type=None):
        if len(call.arguments) <= 1:
            return
        name = self._extract_topic(call, topic_pos=topic_pos)
        msg_type = msg_type or self._extract_message_type(call)
        queue_size = self._extract_queue_size(call, queue_pos=queue_pos)
        depth = get_control_depth(call, recursive=True)
        location = self._call_location(call)
        conditions = [SourceCondition(pretty_str(c), location=location)
                      for c in get_conditions(call, recursive=True)]
        pub = Publication(name, ns, msg_type, queue_size, location=location,
                          control_depth=depth, conditions=conditions,
                          repeats=is_under_loop(call, recursive=True))
        node.advertise.append(pub)
        self.log.debug("Found Publication on %s/%s (%s)", ns, name, msg_type)

    def _on_subscription(self, node, ns, call, topic_pos=0, queue_pos=1,
                         msg_type=None):
        if len(call.arguments) <= 1:
            return
        name = self._extract_topic(call, topic_pos=topic_pos)
        msg_type = msg_type or self._extract_message_type(call)
        queue_size = self._extract_queue_size(call, queue_pos=queue_pos)
        depth = get_control_depth(call, recursive=True)
        location = self._call_location(call)
        conditions = [SourceCondition(pretty_str(c), location=location)
                      for c in get_conditions(call, recursive=True)]
        sub = Subscription(name, ns, msg_type, queue_size, location=location,
                           control_depth=depth, conditions=conditions,
                           repeats=is_under_loop(call, recursive=True))
        node.subscribe.append(sub)
        self.log.debug("Found Subscription on %s/%s (%s)", ns, name, msg_type)

    def _on_service(self, node, ns, call):
        if len(call.arguments) <= 1:
            return
        name = self._extract_topic(call)
        msg_type = self._extract_message_type(call)
        depth = get_control_depth(call, recursive = True)
        location = self._call_location(call)
        conditions = [SourceCondition(pretty_str(c), location = location)
                      for c in get_conditions(call, recursive = True)]
        srv = ServiceServerCall(name, ns, msg_type, location = location,
                                control_depth = depth, conditions = conditions,
                                repeats = is_under_loop(call, recursive = True))
        node.service.append(srv)
        self.log.debug("Found Service on %s/%s (%s)", ns, name, msg_type)

    def _on_client(self, node, ns, call):
        if len(call.arguments) <= 1:
            return
        name = self._extract_topic(call)
        msg_type = self._extract_message_type(call)
        depth = get_control_depth(call, recursive = True)
        location = self._call_location(call)
        conditions = [SourceCondition(pretty_str(c), location = location)
                      for c in get_conditions(call, recursive = True)]
        cli = ServiceClientCall(name, ns, msg_type, location = location,
                                control_depth = depth, conditions = conditions,
                                repeats = is_under_loop(call, recursive = True))
        node.client.append(cli)
        self.log.debug("Found Client on %s/%s (%s)", ns, name, msg_type)

    def _on_read_param(self, node, ns, call):
        if len(call.arguments) < 1:
            return
        name = self._extract_topic(call)
        depth = get_control_depth(call, recursive = True)
        location = self._call_location(call)
        conditions = [SourceCondition(pretty_str(c), location = location)
                      for c in get_conditions(call, recursive = True)]
        read = ReadParameterCall(name, ns, None, location = location,
                                 control_depth = depth, conditions = conditions,
                                 repeats = is_under_loop(call, recursive = True))
        node.read_param.append(read)
        self.log.debug("Found Read on %s/%s (%s)", ns, name, "string")

    def _on_write_param(self, node, ns, call):
        if len(call.arguments) < 1:
            return
        name = self._extract_topic(call)
        depth = get_control_depth(call, recursive = True)
        location = self._call_location(call)
        conditions = [SourceCondition(pretty_str(c), location = location)
                      for c in get_conditions(call, recursive = True)]
        wrt = WriteParameterCall(name, ns, None, location = location,
                                 control_depth = depth, conditions = conditions,
                                 repeats = is_under_loop(call, recursive = True))
        node.write_param.append(wrt)
        self.log.debug("Found Write on %s/%s (%s)", ns, name, "string")

    def _call_location(self, call):
        source_file = None
        if call.file:
            for sf in self.package.source_files:
                if sf.path == call.file:
                    source_file = sf
                    break
        function = call.function
        if function:
            function = function.name
        return Location(self.package, file = source_file,
                        line = call.line, fun = function)

    def _resolve_node_handle(self, value):
        ns = "?"
        value = resolve_reference(value) if value else None
        if not value is None:
            if isinstance(value, CppFunctionCall):
                if value.name == "NodeHandle":
                    if len(value.arguments) == 2:
                        value = value.arguments[0]
                        if isinstance(value, basestring):
                            ns = value
                        elif isinstance(value, CppDefaultArgument):
                            ns = ""
                    elif len(value.arguments) == 1:
                        value = value.arguments[0]
                        if isinstance(value, CppFunctionCall):
                            if value.name == "getNodeHandle":
                                ns = ""
                            elif value.name == "getPrivateNodeHandle":
                                ns = "~"
                elif value.name == "getNodeHandle":
                    ns = ""
                elif value.name == "getPrivateNodeHandle":
                    ns = "~"
            elif isinstance(value, CppDefaultArgument):
                ns = ""
        return ns

    def _resolve_it_node_handle(self, value):
        value = resolve_expression(value)
        if (isinstance(value, CppFunctionCall)
                and value.name == "ImageTransport"):
            return self._resolve_node_handle(value.arguments[0])
        return "?"

    def _extract_topic(self, call, topic_pos=0):
        name = resolve_expression(call.arguments[topic_pos])
        if not isinstance(name, basestring):
            name = "?"
        return name or "?"

    def _extract_message_type(self, call):
        if call.template:
            template = call.template[0]
            std_alloc = re.search("_<std::allocator<void>", template)
            if std_alloc is not None:
                template = template[:std_alloc.start()]
            assert re.match(r"\w+::\w+$", template)
            return template.replace("::", "/")
        if call.name != "subscribe" and call.name != "advertiseService":
            return "?"
        callback = call.arguments[2] if call.name == "subscribe" \
                                     else call.arguments[1]
        while isinstance(callback, CppOperator):
            callback = callback.arguments[0]
        type_string = callback.result
        type_string = type_string.split(None, 1)[1]
        if type_string.startswith("(*)"):
            type_string = type_string[3:]
        if type_string[0] == "(" and type_string[-1] == ")":
            type_string = type_string[1:-1]
            if call.name == "advertiseService":
                type_string = type_string.split(", ")[0]
            is_const = type_string.startswith("const ")
            if is_const:
                type_string = type_string[6:]
            is_ref = type_string.endswith(" &")
            if is_ref:
                type_string = type_string[:-2]
            is_ptr = type_string.endswith("::ConstPtr")
            if is_ptr:
                type_string = type_string[:-10]
            else:
                is_ptr = type_string.endswith("ConstPtr")
                if is_ptr:
                    type_string = type_string[:-8]
            if type_string.endswith("::Request"):
                type_string = type_string[:-9]
        if type_string.startswith("boost::function"):
            type_string = type_string[52:-25]
        return type_string.replace("::", "/")

    def _extract_queue_size(self, call, queue_pos=1):
        queue_size = resolve_expression(call.arguments[queue_pos])
        if isinstance(queue_size, (int, long, float)):
            return queue_size
        return None
