#!/usr/bin/env python
"""Bioconductor run git transition code.

This module assembles the functions from `git_script.py` and
`svn_dump.py` so that the Bioconductor SVN --> Git transition
can be run in a sequential manner.

Author: Nitesh Turaga
Ideas taken from Jim Hester's code in Bioconductor/mirror

Usage:
    `python run_transition.py`
"""

from src.local_svn_dump import LocalSvnDump
from src.git_bioconductor_repository import GitBioconductorRepository
from src.git_experiment_repository import Lfs
from src.git_manifest_repository import GitManifestRepository
from src.update_temp_git_repo import UpdateGitRepository
import os
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
    return


def run_transition(configfile, new_svn_dump=False):
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
    svn_transition_log = Config.get('SVN', 'svn_transition_log')

    logging.basicConfig(filename=svn_transition_log,
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
    logging.debug("Bioconductor Transition Log File: \n")

    # Print in the log file.
    for s in Config.sections():
        for k, v in Config.items(s):
            logging.info("%s: %s" % (k, v))

    if not os.path.isdir(temp_git_repo):
        os.mkdir(temp_git_repo)

    # Step 1: Initial set up, get list of packs from trunk
    dump = LocalSvnDump(svn_root, temp_git_repo, users_db,
                        remote_svn_server, package_path)
    packs = dump.get_pack_list(branch="trunk")
    ###################################################
    # Create a local dump of SVN packages in a location
    if new_svn_dump:
        logging.info("Create a local SVN dump")
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
    return


def run_experiment_data_transition(configfile, new_svn_dump=False):
    """Run experiment data transtion.
    """
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

    data_log = Config.get("ExperimentData", "data_log")
    logging.basicConfig(filename=data_log,
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
    logging.debug("Bioconductor Experiment data transition log File: \n")

    # Create temp_git_repo directory
    if not os.path.isdir(temp_git_repo):
        os.mkdir(temp_git_repo)

    # Step 1: Initial set up, get list of packs from trunk
    dump = LocalSvnDump(svn_root, temp_git_repo, users_db,
                        remote_svn_server, package_path)
    packs = dump.get_pack_list(branch="trunk")

    ###################################################
    # Create a local dump of SVN packages in a location
    if new_svn_dump:
        logging.info("Create a local SVN dump of experiment data")
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
    logging.info("Finished setting up bare git repo for experiment data packages")
    return


def run_manifest_transition(configfile, new_svn_dump=False):
    """Run manifest file transition."""
    # Settings
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    temp_git_repo = Config.get('Software', 'temp_git_repo')
    remote_url = Config.get('Software', 'remote_url')
    admin_repo = Config.get('Software', 'admin_repo')
    svn_root = Config.get('SVN', 'svn_root')
    package_path = Config.get('Software', 'package_path')

    manifest_log = Config.get("Software", "manifest_log")
    manifest_files = Config.get("Software", "manifest_files")
    logging.basicConfig(filename=manifest_log,
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
    logging.debug("Bioconductor manifest files transition log file: \n")

    # Create new manifest repo

    manifest_repo = GitManifestRepository(svn_root, temp_git_repo,
                                          admin_repo, remote_url,
                                          package_path, manifest_files)
    # 1. Create manifest clone
    manifest_repo.manifest_clone(new_svn_dump)
    # 2. Add orphan branch points
    manifest_repo.add_orphan_branch_points()
    # 3. Add commit history
    manifest_repo.add_commit_history()
    manifest_repo.rename_files_in_branch()
    manifest_repo.create_bare_repos()
    manifest_repo.add_remote()
    return

def run_data_manifest_transition(configfile, new_svn_dump=False):
    """Run data manifest transition."""
    return

def run_updates(configfile):
    """Run updates on all branches"""
    return

def run_workflow_transition(configfile, new_svn_dump=False):
    """Run workflow transition."""
    # Settings
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    temp_git_repo = Config.get('Workflow', 'temp_git_repo')
    remote_url = Config.get('Software', 'remote_url')
    bare_git_repo = Config.get('Workflow', 'bare_git_repo')
    package_path = Config.get('Workflow', 'package_path')

    svn_root = Config.get('SVN', 'svn_root')
    remote_svn_server = Config.get('SVN', 'remote_svn_server')
    users_db = Config.get('SVN', 'users_db')
    workflow_log = Config.get('Workflow', 'workflow_log')

    logging.basicConfig(filename=workflow_log,
                    level=logging.DEBUG,
                    format='%(asctime)s %(message)s')
    logging.debug("Bioconductor Workflow Transition Log File: \n")

    # Print in the logging file.
    if not os.path.isdir(temp_git_repo):
        os.mkdir(temp_git_repo)
    dump = LocalSvnDump(svn_root, temp_git_repo, users_db,
						remote_svn_server, package_path)
    packs = dump.get_pack_list(branch="trunk")
    if new_svn_dump:
        logging.info("Create workflow dump")
        dump.svn_dump(packs)
    # Make bare repo, if it does not exist
    if not os.path.isdir(bare_git_repo):
        os.mkdir(bare_git_repo)

    logging.info("Make workflow git repo")
    make_git_repo(svn_root, temp_git_repo, bare_git_repo, remote_url,
                  package_path)
    # EOF message
    logging.info("Finished setting up bare git repo")
    return

if __name__ == '__main__':
    conf = "./settings.ini"
    # run_manifest_transition(conf, new_svn_dump=True)
    run_data_manifest_transition(conf)
    # run_transition(conf ,new_svn_dump=True)
    # run_experiment_data_transition(conf, new_svn_dump=True)
    # run_workflow_transition(conf, new_svn_dump=True)
    # run_updates()
