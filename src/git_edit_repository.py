#!/usr/bin/env python

"""Bioconductor Git repo user interaction script docstrings.

This module provides functions for working with the Bioconductor
`git` repository. This module gives the bioconductor core team,
to interact with the GIT server, and work with package authors.

Author: Nitesh Turaga

# TODO: This needs to be edited to fit new constraints.
"""
import os
import subprocess
from src.git_api.git_api import git_clone
from src.git_api.git_api import git_remote_add
from src.git_api.git_api import git_checkout
from local_svn_dump import Singleton
import logging as log


class GitEditRepository(object):
    """Git Edit repository."""
    __metaclass__ = Singleton

    def __init__(self, edit_repo, ssh_server):
        """Initialize Git edit repo."""
        self.edit_repo = edit_repo
        self.ssh_server = ssh_server
        return

    # TODO: deprecate
    def extract_development_url(self, package):
        """Extract `DevelopmentURL` from DESCRIPTION file."""
        description = os.path.join(package, 'DESCRIPTION')
        with open(description, 'r') as f:
            doc = f.read()
        doc_list = doc.split("\n")
        for i in xrange(len(doc_list)):
            if doc_list[i].startswith("DevelopmentURL:"):
                url = doc_list[i]
        url = url.replace("DevelopmentURL:", "")
        url = url.strip()
        return url

    # TODO: deprecate
    def set_edit_repo(self, package):
        """
        Clone a package from bioc_git_repo to make changes.

        Use this function to set up a clone of an existing bioconductor-git
        package, to make changes and push back to the git-server.
        """
        log.info("Set up a clone of package: %s, "
                 "to push changes to bare_git_repo" % package)
        repository = self.ssh_server + "/" + package
        git_clone(repository, self.edit_repo, bare=False)
        development_url = self.extract_development_url(os.path.join(self.edit_repo, package))
        git_remote_add('upstream', development_url,
                       cwd=os.path.join(self.edit_repo, package))
        return

    # TODO: deprecate
    def clone_all_edit_repo(self):
        """Clone all packages in git server.

        This clone of the entire git server is located on a seperate instance,
        where contents of the pacakges may be edited. After the modifications
        in the `edit_repo`, the contents can be pushed to the `bioc_git_repo`.
        """
        # TODO: get list of package from servers
        # get list of packages from manifest file.
        for package in os.listdir(self.bare_git_repo):
            self.set_edit_repo(package)
        return

    # TODO: deprecate
    def daily_fetch_branch(self, package, branch):
        """Daily fetch from github repo.

        ## git checkout branch-1
        ## git pull upstream branch-1:branch-1
        ## git push origin branch-1
        """
        path = os.path.join(self.edit_repo, package)
        git_checkout(branch, cwd=path, new=False)
        # Git pull into a branch of the edit_repp
        cmd = ['git', 'pull', '-Xtheirs', '--no-edit', 'upstream',
               branch + ":" + branch]
        p = subprocess.Popen(cmd, cwd=path, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
        out, err = p.communicate()
        if ("CONFLICT" in out):
            log.error("Merge conflict in the package: %s" % package)
            log.error(out)
        else:  # Git push
            cmd = ['git', 'push', 'origin', branch]
            subprocess.check_call(cmd, cwd=path)
        return

    # TODO: deprecate
    def daily_fetch(self, branch):
        """Daily fetch of every package in the edit_repo.

        Daily fetch  needs to be run by the build system on
        the branch being updated e.g `master` or `RELEASE_3_4`
        """
        for package in os.listdir(self.edit_repo):
            self.daily_fetch_branch(package, branch)
        return

    def version_bump(self, package, release=False):
        """Bump package version.

        release=False, assumes that version bump is not for a new
                       release branch.
        """
        description_file = os.path.join(self.edit_repo, package, 'DESCRIPTION')
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
        log.info("Package: %s updated version to: %s" % (package, version))
        return

    # TODO: REMOVE commit_message and use the one in git_api
    def commit_message(self, msg, package):
        """Add a commit message to package during, bioc release."""
        cmd = ['git', 'commit', '-m', msg]
        subprocess.check_call(cmd, cwd=package)
        return

    def release_branch(self, package, new_release):
        """Create new release branch, make git call."""
        package_dir = os.path.join(self.edit_repo, package)
        # checkout master
        git_checkout(branch="master", cwd=package_dir, new=False)
        # on master, version bump, release = False
        self.version_bump(package, release=False)
        self.commit_message("bump x.y.z versions to even 'y' "
                            "prior to creation of " + new_release, package_dir)

        # IN THE BRANCH, version bump release=True
        git_checkout(branch=new_release, cwd=package_dir, new=True)
        self.version_bump(package, release=True)
        # commit messsage in branch
        self.commit_message(msg="Creating branch for BioC " + new_release,
                            package=package_dir)
        # checkout master
        git_checkout(branch="master", cwd=package_dir, new=False)
        # version bump release=True
        self.version_bump(package, release=True)
        # Commit message
        self.commit_message("bump x.y.z versions to odd 'y' "
                            "after creation of " + new_release, package_dir)
        log.info("New branch created for package %s" % package)
        return

    def create_new_release_branch(self, new_release):
        """Create a new RELEASE from master.

        This function is used to create a new release version,
        from the 'master' branch going forward.
        Usage: create_new_release_branch('RELEASE_3_7', '/packages/')
        """
        for package in os.listdir(os.path.abspath(self.edit_repo)):
            # Create a new release branch
            self.release_branch(new_release, package)
            # TODO: Push new release branch
            cmd = ['git', 'push', '-u', 'origin', new_release]
            subprocess.check_call(cmd, cwd=os.path.join(self.edit_repo, package))
        return
