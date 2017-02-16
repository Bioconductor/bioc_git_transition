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
log.basicConfig(filename='transition.log', level=log.DEBUG)
log.debug("Bioconductor Transition Log File: \n")


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

    update_file = Config.get('SVN', 'update_file')
    svn_root = Config.get('SVN', 'svn_root')
    remote_svn_server = Config.get('SVN', 'remote_svn_server')
    users_db = Config.get('SVN', 'users_db')

    if not os.path.isdir(bioc_git_repo):
        os.mkdir(bioc_git_repo)

    # Step 1: Initial set up, get list of packs from trunk
    print(svn_root, bioc_git_repo, users_db, remote_svn_server, remote_url)
    dump = LocalSvnDump(svn_root, bioc_git_repo, users_db, remote_svn_server)
    packs = dump.get_pack_list(branch="trunk")
    print(packs)
    # Create a local dump of SVN packages in a location
    dump.svn_dump(packs)
    import pdb; pdb.set_trace()
    # Step 2: Update
#    dump.svn_get_revision()
#    dump.svn_dump_update(update_file)
#    dump.update_local_svn_dump(update_file)

    # # Step 4: Add release branches to all   packages
    # gitrepo = GitBioconductorRepository(svn_root, bioc_git_repo, remote_url)
    # gitrepo.add_release_branches()
    # # Step 5: Add commit history
    # gitrepo.add_commit_history()
    # # Add git remote branch, to make git package act as a server
    # os.chdir(bioc_git_repo)
    # gitrepo.add_remote()
    # os.chdir("..")
    # # Step 6: Make Git repo bare
    # gitrepo.create_bare_repos(bare_git_repo)

    # # Make Edit repo:
    # editrepo = GitEditRepository(edit_repo, bioc_git_repo, server)
    return


if __name__ == '__main__':
    run_transition("./settings.ini")
