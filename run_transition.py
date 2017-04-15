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
from src.graft_data_as_lfs import graft_data_as_lfs
import os
import logging as log
import ConfigParser


def make_git_repo(svn_root, temp_git_repo, bare_git_repo, remote_url,
                  package_path):
    # Step 4: Add release branches to all   packages
    gitrepo = GitBioconductorRepository(svn_root, temp_git_repo,
                                        bare_git_repo, remote_url,
                                        package_path)
    log.info("Make git repo: Adding release branches")
    gitrepo.add_release_branches()
    # Step 5: Add commit history
    log.info("Make git repo: Adding commit history")
    gitrepo.add_commit_history()
    # Step 6: Make Git repo bare
    log.info("Make git repo: Creating bare repositories")
    gitrepo.create_bare_repos()
    log.info("Make git repo: Adding remotes to make git server available")
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

    log.basicConfig(filename=svn_transition_log,
                    level=log.DEBUG,
                    format='%(asctime)s %(message)s')
    log.debug("Bioconductor Transition Log File: \n")

    # Print in the log file.
    for s in Config.sections():
        for k, v in Config.items(s):
            log.info("%s: %s" % (k, v))

    if not os.path.isdir(temp_git_repo):
        os.mkdir(temp_git_repo)

    # Step 1: Initial set up, get list of packs from trunk
    dump = LocalSvnDump(svn_root, temp_git_repo, users_db, remote_svn_server)
    packs = dump.get_pack_list(branch="trunk")
    ###################################################
    # Create a local dump of SVN packages in a location
    if new_svn_dump:
        log.info("Create a local SVN dump")
        dump.svn_dump(packs)
    ###################################################

    # Make bare repo, if it does not exist
    if not os.path.isdir(bare_git_repo):
        os.mkdir(bare_git_repo)

    # Make temp git repo, with all commit history
    log.info("Make git repo")
    make_git_repo(svn_root, temp_git_repo, bare_git_repo, remote_url,
                  package_path)

    # EOF message
    log.info("Finished setting up bare git repo")
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

    svn_dump_log = Config.get("SVN", "svn_dump_log")
    log.basicConfig(filename=svn_dump_log,
                    level=log.DEBUG,
                    format='%(asctime)s %(message)s')
    log.debug("Bioconductor Transition Log File: \n")

    # Print in the log file.
    for s in Config.sections():
        for k, v in Config.items(s):
            log.info("%s: %s" % (k, v))

    if not os.path.isdir(temp_git_repo):
        os.mkdir(temp_git_repo)

    # Step 1: Initial set up, get list of packs from trunk
    dump = LocalSvnDump(svn_root, temp_git_repo, users_db,
                        remote_svn_server)
    packs = dump.get_pack_list(branch="trunk")

    ###################################################
    # Create a local dump of SVN packages in a location
    if new_svn_dump:
        log.info("Create a local SVN dump")
        dump.svn_dump(packs)
    ###################################################
#    # Make bare repo, if it does not exist
#    if not os.path.isdir(bare_git_repo):
#        os.mkdir(bare_git_repo)
#
#    # Make temp git repo, with all commit history
#    log.info("Make git repo for experiment data packages")
#    make_git_repo(svn_root, temp_git_repo, bare_git_repo,
#                  remote_url, package_path)
#    # EOF message
#    log.info("Finished setting up bare git repo for experiment data packages")
#
#    # Add data to all packages
#    graft_data_as_lfs(svn_root, trunk, data_store_path, ref_file)
    return


if __name__ == '__main__':
    run_transition("./settings.ini", new_svn_dump=True)
    run_experiment_data_transition("./settings.ini", new_svn_dump=True)
