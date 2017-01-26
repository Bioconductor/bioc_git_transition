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
    svn_root = 'file:///home/nturaga/bioconductor-svn-mirror/'
    dump_location = "bioconductor-svn-mirror/"
    remote_svn_server = 'https://hedgehog.fhcrc.org/bioconductor'
    repo_dir = "/home/nturaga/packages"
    update_file = "updt.svn"

    if not os.path.isdir(repo_dir):
        os.mkdir(repo_dir)

    # Step 1: Initial set up, get list of packs from trunk
    package_url = os.path.join(svn_root, 'trunk', 'madman', 'Rpacks')
    packs = sd.get_pack_list(package_url)
    # Create a local dump of SVN packages in a location
    sd.svn_dump(svn_root, packs, repo_dir)

    # Step 2: Update
    revision = sd.svn_get_revision(svn_root)
    sd.svn_dump_update(revision, remote_svn_server, svn_root,
                       update_file)
    sd.update_local_svn_dump(dump_location, update_file)

    # Step 3: Add git remote branch, to make git package act as a server
    remote_path = "nturaga@git.bioconductor.org:/home/nturaga/packages/"
    os.chdir(repo_dir)
    gs.add_remote(remote_path, repo_dir)
    os.chdir("..")

    # Step 4: Add release branches to all   packages
    gs.add_release_branches(svn_root, repo_dir)

    # Step 5: Add commit history
    gs.add_commit_history(svn_root)
    # Step 6: Make Git repo bare
    gs.create_bare_repos(repo_dir)
    return


if __name__ == '__main__':
    run_transition()
