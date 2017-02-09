#!/usr/bin/env python

"""Bioconductor Clone new package docstrings.

This module provides functions for working with the Bioconductor
`git` repository. Once the SVN dump takes place, we add remote branches,
and commit history to each branch as needed.

Author: Nitesh Turaga
Ideas taken from Jim Hester's code in Bioconductor/mirror
"""

import logging as log
import os
import subprocess
from git_script import git_remote_rename
from git_script import git_remote_add


def clone(destination_dir, package_url, bare=True):
    """Make a clone of a git repository.

    Package will be cloned in `destination_dir`, and if `bare=True`
    are bare repository is created, else a regular clone.
    """
    package = package_url.split("/")[-1]
    package_dir = os.path.join(destination_dir, package)
    if bare:
        cmd = ['git', 'clone', '--bare', package_url, package_dir]
    else:
        package_dir = package_dir.replace(".git", "")
        cmd = ['git', 'clone', package_url, package_dir]
    subprocess.check_call(cmd)
    return package_dir


def clone_new(repo_dir, destination_dir, new_package_url):
    """Clone a new package.

    This function is used to add a new package to the bioconductor
    repository and reconfigure remotes after cloning the package.
    """
    log.info("Cloning NEW Bare repository to repo_dir")
    package_dir = clone(repo_dir, new_package_url, bare=True)
    git_remote_rename(package_dir, 'origin', 'upstream')
    git_remote_add('origin', package_dir, package_dir)
    return
