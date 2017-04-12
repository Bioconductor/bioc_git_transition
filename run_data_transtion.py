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
from src.git_bioconductor_repository import ExperimentDataRepository
import os
import logging as log
import ConfigParser


def make_git_repo(svn_root, bioc_git_repo, bare_git_repo, remote_url):
    # Step 4: Add release branches to all   packages
    gitrepo = ExperimentDataRepository(svn_root, bioc_git_repo,
                                       bare_git_repo, remote_url)
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
    """Run experiment data transtion.
    """
    # Settings
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    temp_data_git_repo = Config.get('ExperimentData', 'temp_data_git_repo')
    remote_url = Config.get('GitBioconductor', 'remote_url')
    bare_data_git_repo = Config.get('ExperimentData', 'bare_git_repo')
    svn_exp_root = Config.get('ExperimentData', 'svn_exp_root')
    remote_svn_data_server = Config.get('ExperimentData',
                                        'remote_svn_data_server')
    # update_file_data = Config.get('ExperimentData', 'update_file_data')
    users_db = Config.get('SVN', 'users_db')

    svn_exp_log = Config.get('ExperimentData', 'svn_exp_log')
    log.basicConfig(filename=svn_exp_log,
                    level=log.DEBUG,
                    format='%(asctime)s %(message)s')
    log.debug("Bioconductor Transition Log File: \n")

    # Print in the log file.
    for s in Config.sections():
        for k, v in Config.items(s):
            log.info("%s: %s" % (k, v))

    if not os.path.isdir(temp_data_git_repo):
        os.mkdir(temp_data_git_repo)

    # Step 1: Initial set up, get list of packs from trunk
    dump = LocalSvnDump(svn_exp_root, temp_data_git_repo, users_db,
                        remote_svn_data_server)
    packs = dump.get_pack_list(branch="trunk")

    ###################################################
    # Create a local dump of SVN packages in a location
    if new_svn_dump:
        log.info("Create a local SVN dump")
        dump.svn_dump(packs)
    ###################################################

    # Make bare repo, if it does not exist
    if not os.path.isdir(bare_data_git_repo):
        os.mkdir(bare_data_git_repo)

    # Make temp git repo, with all commit history
    log.info("Make git repo for experiment data packages")
    make_git_repo(svn_exp_root, temp_data_git_repo, bare_data_git_repo,
                  remote_url)

    # EOF message
    log.info("Finished setting up bare git repo for experiment data packages")
    return


if __name__ == '__main__':
    run_transition("./settings.ini", new_svn_dump=True)
