#!/usr/bin/env python

"""Bioconductor Git repo user interaction script docstrings.

This module provides functions for working with the Bioconductor
`git` repository. This module gives the bioconductor core team,
to interact with the git server during the release process.

Author: Nitesh Turaga
"""
import os
import subprocess
from src.git_api.git_api import git_commit
from src.git_api.git_api import git_checkout
from local_svn_dump import Singleton
import logging


class ReleaseProcess(object):
    """Git Edit repository."""
    __metaclass__ = Singleton

    def __init__(self, bare_git_repo):
        """Initialize Git edit repo."""
        self.bare_git_repo = bare_git_repo
        return

    def version_bump(self, package, release=False):
        """Bump package version.

        release=False, assumes that version bump is not for a new
                       release branch.
        """
        description_file = os.path.join(self.bare_git_repo, package,
                                        'DESCRIPTION')
        with open(description_file, 'r') as f:
            doc = f.read()
        doc_list = doc.split("\n")
        for i in xrange(len(doc_list)):
            if doc_list[i].startswith("Version:"):
                version = doc_list[i]
                index = i
        x, y, z = version.split("Version: ")[1].split(".")
        if release:
            # Special case
            if int(y) == 99:
                x = int(x) + 1
                y = 0
            else:
                y = int(y) + 1
            z = 0
        else:
            z = int(z) + 1
        version = str(x) + "." + str(y) + "." + str(z)
        doc_list[index] = "Version: " + version
        with open(description_file, "w") as f:
            f.write("\n".join(doc_list))
        logging.info("Package: %s updated version to: %s" % (package, version))
        return

    def release_branch(self, package, new_release):
        """Create new release branch, make git call."""
        package_dir = os.path.join(self.bare_git_repo, package)
        # checkout master
        git_checkout(branch="master", cwd=package_dir, new=False)
        # on master, version bump, release = False
        self.version_bump(package, release=False)
        msg1 = ("bump x.y.z versions to even 'y' prior to creation of " +
                new_release)
        git_commit(msg1, cwd=package_dir)
        # IN THE BRANCH, version bump release=True
        git_checkout(branch=new_release, cwd=package_dir, new=True)
        self.version_bump(package, release=True)
        # commit messsage in branch
        git_commit("Creating branch for BioC " + new_release,
                   cwd=package_dir)
        # checkout master
        git_checkout(branch="master", cwd=package_dir, new=False)
        # version bump release=True
        self.version_bump(package, release=True)
        # Commit message
        msg2 = ("bump x.y.z versions to odd 'y' after creation of " +
                new_release)
        git_commit(msg2, cwd=package_dir)
        logging.info("New branch created for package %s" % package)
        return

    def create_new_release_branch(self, new_release):
        """Create a new RELEASE from master.

        This function is used to create a new release version,
        from the 'master' branch going forward.
        Usage: create_new_release_branch('RELEASE_3_7', '/packages/')
        """
        for package in os.listdir(os.path.abspath(self.bare_git_repo)):
            # Create a new release branch
            self.release_branch(new_release, package)
            # TODO: Push new release branch
            cmd = ['git', 'push', '-u', 'origin', new_release]
            subprocess.check_call(cmd, cwd=os.path.join(self.bare_git_repo,
                                  package))
        return
