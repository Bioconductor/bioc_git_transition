#!/usr/bin/env python
"""Bioconductor run git transition code.

This module assembles the functions from `git_script.py` and
`svn_dump.py` so that the Bioconductor SVN --> Git transition
can be run in a sequential manner.

Author: Nitesh Turaga
"""

from src.local_svn_dump import LocalSvnDump
from src.git_bioconductor_repository import GitBioconductorRepository
from src.git_experiment_repository import Lfs
from src.git_manifest_repository import GitManifestRepository
from src.git_manifest_repository import GitDataManifestRepository
from src.update_temp_git_repo import UpdateGitRepository
from src.helper.helper import get_branch_list
from src.helper.helper import get_union
from src.helper.helper import populate_manifest_dictionary
from src.helper.helper import union_of_data_manifest
import os
import shutil
import logging
import ConfigParser


def make_git_repo(svn_root, temp_git_repo, bare_git_repo, remote_url,
                  package_path, lfs_object=None):
    # Step 4: Add release branches to all   packages
    gitrepo = GitBioconductorRepository(svn_root, temp_git_repo,
                                        bare_git_repo, remote_url,
                                        package_path)
    logging.info("Make git repo: Adding release branches")
    gitrepo.add_release_branches()
    # Step 5: Add commit history
    logging.info("Make git repo: Adding commit history")
    gitrepo.add_commit_history()

    if lfs_object is not None:
        logging.info("Running LFS transtion")
        lfs_object.run_data_transition(temp_git_repo)
    # Step 6: Make Git repo bare
    logging.info("Make git repo: Creating bare repositories")
    gitrepo.create_bare_repos()
    logging.info("Make git repo: Adding remotes to make git server available")
    gitrepo.add_remote()
    # FIXME: delete gitrepo singleton
    try:
        del gitrepo
    except Exception as e:
        logging.error(e)
        pass
    return


def run_software_transition(configfile, new_svn_dump=False):
    """Update SVN local dump and run gitify-bioconductor.

    Step 0: Create dump
    `svnadmin create bioconductor-svn-mirror`
    `svnrdump dump https://hedgehog.fhcrc.org/bioconductor |
                svnadmin load bioconductor-svn-mirror`
    """

    # Settings
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    temp_git_repo = Config.get('Software', 'temp_git_repo')
    remote_url = Config.get('Software', 'remote_url')
    bare_git_repo = Config.get('Software', 'bare_git_repo')
    package_path = Config.get('Software', 'package_path')

    svn_root = Config.get('SVN', 'svn_root')
    remote_svn_server = Config.get('SVN', 'remote_svn_server')
    users_db = Config.get('SVN', 'users_db')

    logging.info("Bioconductor Software Transition Log File: \n")

    if not os.path.isdir(temp_git_repo):
        os.mkdir(temp_git_repo)

    # Step 1: Initial set up, get list of packs from trunk
    dump = LocalSvnDump(svn_root, temp_git_repo, users_db,
                        remote_svn_server, package_path)
    manifest_dictionary = populate_manifest_dictionary(svn_root, package_path)
#    packs = get_union(svn_root, package_path, manifest_dictionary)
    packs = ["STAN"]
    ##################################################
    # Create a local dump of SVN packages in a location
    if new_svn_dump:
        logging.info("Create a local SVN dump for software packages")
        # Git svn clone software packages
        dump.svn_dump(packs)
    ###################################################

    # Make bare repo, if it does not exist
    if not os.path.isdir(bare_git_repo):
        os.mkdir(bare_git_repo)

    # Make temp git repo, with all commit history
    logging.info("Make git repo")
    make_git_repo(svn_root, temp_git_repo, bare_git_repo, remote_url,
                  package_path)

    # EOF message
    logging.info("Finished setting up bare git repo")
    try:
        del dump
    except Exception as e:
        logging.error(e)
        pass
    return


def run_experiment_data_transition(configfile, new_svn_dump=False):
    """Run experiment data transtion."""
    # Settings
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    temp_git_repo = Config.get('ExperimentData', 'temp_git_repo')
    remote_url = Config.get('Software', 'remote_url')
    bare_git_repo = Config.get('ExperimentData', 'bare_git_repo')
    svn_root = Config.get('ExperimentData', 'svn_root')
    remote_svn_server = Config.get('ExperimentData',
                                   'remote_svn_server')
    package_path = Config.get('ExperimentData', 'package_path')
    users_db = Config.get('SVN', 'users_db')

    trunk = Config.get('SVN', 'trunk')
    data_store_path = Config.get('ExperimentData', 'data_store_path')
    ref_file = Config.get('ExperimentData', 'ref_file')

    logging.debug("Bioconductor Experiment data transition log File: \n")

    # Create temp_git_repo directory
    if not os.path.isdir(temp_git_repo):
        os.mkdir(temp_git_repo)

    # Step 1: Initial set up, get list of packs from trunk
    dump = LocalSvnDump(svn_root, temp_git_repo, users_db,
                        remote_svn_server, package_path)

    # TODO: replace this hack
    packs = union_of_data_manifest()
    ###################################################
    # Create a local dump of SVN packages in a location
    if new_svn_dump:
        logging.info("Create a local SVN dump of experiment data")
        # Git svn clone all packages
        dump.svn_dump(packs)
    ###################################################
    # Make bare repo, if it does not exist
    if not os.path.isdir(bare_git_repo):
        os.mkdir(bare_git_repo)

    # Make temp git repo, with all commit history
    logging.info("Make git repo for experiment data packages")
    # Create a new git LFS object
    lfs = Lfs(svn_root, trunk, data_store_path, ref_file, temp_git_repo)
    # Run make_git_repo, with new LFS object
    make_git_repo(svn_root, temp_git_repo, bare_git_repo,
                  remote_url, package_path, lfs_object=lfs)
    # EOF message
    logging.info("Completed bare git repo for experiment data packages")
    # FIXME: delete singleton instances
    try:
        del dump
        del lfs
    except Exception as e:
        logging.error(e)
        pass
    return


def run_manifest_transition(configfile, new_svn_dump=False):
    """Run manifest file transition."""
    # Settings
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    temp_git_repo = Config.get('Software', 'temp_git_repo')
    bare_git_repo = Config.get('Manifest', 'bare_git_repo')
    svn_root = Config.get('SVN', 'svn_root')
    package_path = Config.get('Software', 'package_path')

    include_path = Config.get("Manifest", "software_manifest_include_path")
    logging.debug("Bioconductor manifest files transition log file: \n")

    #####################################
    # Create new manifest repo for software
    ######################################
    manifest_repo = GitManifestRepository(svn_root, temp_git_repo,
                                          bare_git_repo,
                                          package_path, include_path)
    # 1. Create manifest clone
    logging.info("Create a new software manifest dump")
    manifest_repo.manifest_clone(new_svn_dump)
    # 2. Add orphan branch points
    logging.info("Add orphan branch points to manifest files")
    manifest_repo.add_orphan_branch_points()
    # 3. Add commit history
    logging.info("Add commit history to manifest files")
    manifest_repo.add_commit_history()
    manifest_repo.rename_files_in_branches()

    #####################################
    # Run data manifest transition
    ######################################
    data_svn_root = Config.get("ExperimentData", "svn_root")
    data_package_path = Config.get("ExperimentData", "package_path")
    data_include_path = Config.get("Manifest", "data_manifest_include_path")
    # A new class is defined which inherits from GitManifestRepo,
    # because it the parent class is a singleton.
    data_manifest_repo = GitDataManifestRepository(data_svn_root,
                                                   temp_git_repo,
                                                   data_package_path,
                                                   data_include_path)
    logging.info("Copy data manifest log files")
    data_manifest_repo.manifest_clone(new_svn_dump)
    logging.info("Create unified repo for software and data manifest")
    manifest_repo.create_unified_repo()
    #####################################
    # Create bare repos and add remote
    ######################################
    if not os.path.isdir(bare_git_repo):
        logging.info("Create bare_git_repo %s" % bare_git_repo)
        os.mkdir(bare_git_repo)
    logging.info("Create bare manifest repository")
    manifest_repo.create_bare_repos()
    logging.info("Add remote to manifest repo")
    manifest_repo.add_remote()
    # FIXME: Delete singleton instances
    try:
        del manifest_repo
        del data_manifest_repo
    except Exception as e:
        logging.error(e)
        pass
    return


def run_updates(configfile):
    """Run updates on all branches"""
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    software_temp_git_repo = Config.get('Software', 'temp_git_repo')
    svn_root = Config.get('SVN', 'svn_root')

    # FIXME: Get branch list, there has to be a simpler way to do this
    branch_list = get_branch_list(svn_root)
    logging.info("Start update of software temp git repo")
    updater = UpdateGitRepository(software_temp_git_repo, branch_list)
    updater.update_temp_git_repo()
    # FIXME: Delete singleton instances
    try:
        del updater
    except Exception as e:
        logging.error(e)
        pass
    return


def run_workflow_transition(configfile, new_svn_dump=False):
    """Run workflow transition."""
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    temp_git_repo = Config.get('Workflow', 'temp_git_repo')
    remote_url = Config.get('Software', 'remote_url')
    bare_git_repo = Config.get('Workflow', 'bare_git_repo')
    package_path = Config.get('Workflow', 'package_path')

    svn_root = Config.get('SVN', 'svn_root')
    remote_svn_server = Config.get('SVN', 'remote_svn_server')
    users_db = Config.get('SVN', 'users_db')
    logging.debug("Bioconductor Workflow Transition Log File: \n")

    # Print in the logging file.
    if not os.path.isdir(temp_git_repo):
        os.mkdir(temp_git_repo)

    ######################################
    # Create a local svn dump
    ######################################
    dump = LocalSvnDump(svn_root, temp_git_repo, users_db,
                        remote_svn_server, package_path)
    # TODO: Workflow packages should take in union of 
    # RELEASE_3_5 and RELEASE_3_6 manifest files
    packs = dump.get_pack_list(branch="trunk")
    # Git svn clone workflow packages
    if new_svn_dump:
        logging.info("Create workflow dump")
        dump.svn_dump(packs)
    ######################################
    # Make bare repo, if it does not exist
    ######################################
    if not os.path.isdir(bare_git_repo):
        os.mkdir(bare_git_repo)
    logging.info("Make workflow git repo")
    make_git_repo(svn_root, temp_git_repo, bare_git_repo, remote_url,
                  package_path)
    ######################################
    # Remove packages which are not supposed to be in the directory
    ######################################
    try:
        shutil.rmtree(os.path.join(temp_git_repo, "testproj"))
        shutil.rmtree(os.path.join(temp_git_repo, "packages"))
        shutil.rmtree(os.path.join(bare_git_repo, "testproj.git"))
        shutil.rmtree(os.path.join(bare_git_repo, "packages.git"))
    except Exception as e:
        logging.error("packages -testproj- and -packages- not deleted")
        logging.error(e)
        pass
    # EOF message
    logging.info("Finished setting up bare git repo")
    try:
        del dump
    except Exception as e:
        logging.error(e)
        pass
    return
