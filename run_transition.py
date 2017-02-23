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
from src.git_edit_repository import GitEditRepository
import os
import logging as log
import ConfigParser
log.basicConfig(filename='transition.log',
                level=log.DEBUG,
                format='%(asctime)s %(message)s')
log.debug("Bioconductor Transition Log File: \n")


def make_git_repo(svn_root, bioc_git_repo, bare_git_repo, remote_url):
    # Step 4: Add release branches to all   packages
    gitrepo = GitBioconductorRepository(svn_root, bioc_git_repo,
 					bare_git_repo, remote_url)
    gitrepo.add_release_branches()
    # Step 5: Add commit history
    gitrepo.add_commit_history()
    # Step 6: Make Git repo bare
    gitrepo.create_bare_repos()
    gitrepo.add_remote()
    return


def make_edit_repo(edit_repo, ssh_server):
    # Make Edit repo:
    editrepo = GitEditRepository(edit_repo, ssh_server)
    editrepo.clone_all_edit_repo()
    return


# TODO: Split run_transition into making dump, and adding new packages
def run_transition(configfile):
    """Update SVN local dump and run gitify-bioconductor.

    Step 0: Create dump
    `svnadmin create bioconductor-svn-mirror`
    `svnrdump dump https://hedgehog.fhcrc.org/bioconductor |
                svnadmin load bioconductor-svn-mirror`
    """
    # Settings
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)
    bioc_git_repo = Config.get('GitBioconductor', 'bioc_git_repo')
    remote_url = Config.get('GitBioconductor', 'remote_url')
    bare_git_repo = Config.get('GitBioconductor', 'bare_git_repo')

    edit_repo = Config.get('GitEditBioconductor', 'edit_repo')
    server = Config.get('GitEditBioconductor', 'server')
    ssh_server = Config.get('GitEditBioconductor', 'ssh_server')

    svn_root = Config.get('SVN', 'svn_root')
    remote_svn_server = Config.get('SVN', 'remote_svn_server')
    users_db = Config.get('SVN', 'users_db')

    # Print in the log file.
    for s in Config.sections():
       for k,v in Config.items(s):
           log.info("%s: %s" % (k,v))

    if not os.path.isdir(bioc_git_repo):
        os.mkdir(bioc_git_repo)

    # Step 1: Initial set up, get list of packs from trunk
    dump = LocalSvnDump(svn_root, bioc_git_repo, users_db, remote_svn_server)
    packs = dump.get_pack_list(branch="trunk")
    ###################################################
    # Create a local dump of SVN packages in a location
    dump.svn_dump(packs)
    ###################################################

    # Make temp git repo, with all commit history
    make_git_repo(svn_root, bioc_git_repo, bare_git_repo, remote_url)

    # Make edit repo
    make_edit_repo(edit_repo, ssh_server)

    # EOF message
    log.info("Finished setting up bare git repo")
    return


if __name__ == '__main__':
    run_transition("./settings.ini")
