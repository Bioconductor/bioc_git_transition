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

import git_script as gs
import svn_dump as sd
import os


# TODO: make this a function with arguments
def run_transition():
    """Update SVN local dump and run gitify-bioconductor.

    Step 0: Create dump
    `svnadmin create bioconductor-svn-mirror`
    `svnrdump dump https://hedgehog.fhcrc.org/bioconductor |
                svnadmin load bioconductor-svn-mirror`

    This function runs the steps in order needed.
    Step 1: Define variables, and paths for SVN dump, remote_svn_repo,
            'git package local repo'.
    Step 2: Update SVN local dump
    Step 3: Add git remote path.
    Step 4: Add release branches to each package in 'git package local repo'
    """
    # Step 0
    local_svn_dump = 'file:///home/nturaga/bioconductor-svn-mirror/'
    dump_location = "bioconductor-svn-mirror/"
    remote_svn_server = 'https://hedgehog.fhcrc.org/bioconductor'
    git_repo = "/home/nturaga/packages"
    update_file = "updt.svn"

    if not os.path.isdir(git_repo):
        os.mkdir(git_repo)

    # Step 1: Initial set up, get list of packs from trunk
	# TODO: BUG HERE in getting pack list
#    packs = sd.get_pack_list(local_svn_dump)
    # Create a local dump of SVN packages in a location
#    sd.svn_dump(local_svn_dump, packs, git_repo)

    # Step 2: Update
#    revision = sd.svn_get_revision(local_svn_dump)
#    sd.svn_dump_update(revision, remote_svn_server, local_svn_dump,
#                       update_file)
#    sd.update_local_svn_dump(dump_location, update_file)

    # Step 3: Add git remote branch, to make git package act as a server
    remote_path = "nturaga@git.bioconductor.org:/home/nturaga/packages/"
#    os.chdir(git_repo)
#    gs.git_add_remote(remote_path, git_repo)
#    os.chdir("..")

    # Step 4: Add release branches to all   packages
    gs.add_release_branches(local_svn_dump, git_repo)

    # Step 5: Add commit history
#    gs.add_commit_history(local_svn_dump)
    return


if __name__ == '__main__':
    run_transition()
