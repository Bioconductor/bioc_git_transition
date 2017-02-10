#!/usr/bin/env python

"""Bioconductor Clone new package docstrings.

This module provides functions for working with the Bioconductor
`git` repository. Once the SVN dump takes place, we add remote branches,
and commit history to each branch as needed.

Author: Nitesh Turaga
Ideas taken from Jim Hester's code in Bioconductor/mirror
"""
import logging as log
from git_api import git_clone
from git_api import git_remote_rename
from git_api import git_remote_add


def clone_new(bioc_git_repo, destination_dir, new_package_url):
    """Clone a new package.

    This function is used to add a new package to the bioconductor
    repository and reconfigure remotes after cloning the package.
    """
    log.info("Cloning NEW Bare repository to bioc_git_repo")
    package_dir = git_clone(new_package_url, bioc_git_repo, bare=True)
    git_remote_rename(package_dir, 'origin', 'upstream')
    git_remote_add('origin', package_dir, package_dir)
    return
