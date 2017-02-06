#!/usr/bin/env python

"""Bioconductor Git user interaction script docstrings.

This module provides functions for working with the Bioconductor
`git` repository. This module gives the bioconductor core team,
to interact with the GIT server, and work with package authors.

Author: Nitesh Turaga
"""
import os
import subprocess
import yaml
import logging as log


def edit_repo(repo_dir, package):
    """Clone a package from repo_dir to make changes."""
    log.info("Set up a clone of package: %s, to push changes to repo_dir")

    return


def version_bump(repo_dir, package):
    description_file = os.path.join(repo_dir, package, 'DESCRIPTION')
    with open(description_file, 'r') as f:
        doc = yaml.load(f)
    version = doc['Version']
    return version


def release_branch(new_release, package_dir):
    """Create new release branch, make git call."""
    # TODO: DOES A VERSION BUMP HAPPEN AS WELL
    cmd = ['git', 'branch', new_release]
    subprocess.check_call(cmd, cwd=package_dir)
    return


def create_new_release_branch(new_release, repo_dir):
    """Create a new RELEASE from master.

    This function is used to create a new release version,
    from the 'master' branch going forward.
    Usage: create_new_release_branch('RELEASE_3_7', '/packages/')
    """
    for package in os.listdir(os.path.abspath(repo_dir)):
        release_branch(new_release, os.path.abspath(package))
    return
