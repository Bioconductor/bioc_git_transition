#!/usr/bin/env python
"""Bioconductor Git script docstrings.

This module provides functions for working with the Bioconductor
`git` repository. Once the SVN dump takes place, we add remote branches,
and commit history to each branch as needed.

Author: Nitesh Turaga
Ideas taken from Jim Hester's code in Bioconductor/mirror
"""


import os
import re
import subprocess
from src.git_api.git_api import git_clone
from src.git_api.git_api import git_remote_add
from src.git_api.git_api import git_svn_fetch
from src.git_api.git_api import git_svn_rebase
from src.git_api.git_api import git_remote_rename
from src.git_api.git_api import git_filter_branch
from src.git_api.git_api import git_checkout
from src.git_api.git_api import git_branch_exists
from local_svn_dump import Singleton
# Logging configuration
import logging as log


class GitBioconductorRepository(object):
    """Git Bioconductor Repository."""
    __metaclass__ = Singleton

    def __init__(self, svn_root, bioc_git_repo, bare_git_repo, remote_url):
        """Initialize Git Bioconductor repository."""
        self.svn_root = svn_root
        self.bioc_git_repo = bioc_git_repo
        self.bare_git_repo = bare_git_repo
        self.remote_url = remote_url
        return

    def get_branch_list(self):
        """Get list of branches.

        Input:
            svn_root path.
        Return:
            List of branches in the reverse order of releases, i.e,
            latest first.
        """
        branch_url = self.svn_root + "branches"
        branch_list = [item.replace('/', '')
                       for item in
                       subprocess.check_output(['svn', 'list', branch_url]).split()
                       if "RELEASE" in item]
        return branch_list

    # TODO: IS THIS EVEN NEEDED?
    def get_pack_list(self, path):
        """Get list of packages on SVN."""
        result = subprocess.check_output(['svn', 'list', path])
        return [item.replace('/', '') for item in result.split()]

    def add_remote(self):
        """Add git remote to make the directory.

        Usage: cd /home/nturaga/packages and run function.
        """
        for package in os.listdir(self.bioc_git_repo):
            if ((os.path.isdir(package)) and
                    (".git" in os.listdir(os.path.abspath(package)))):
                remote = self.remote_url + package
                # Run remote command
                git_remote_add('origin', remote, os.path.abspath(package))
                log.info("Added remote to package: %s" % package)
        return

    def add_orphan_branch_points(self, release, package):
        """Add orphan branch.

        Configure the remote and fetch urls for git-svn. Then, fetch from the
        svn remote repository. Checkout from the release branch, and rebase it
        to the fetched commits. Checkout master at the end.
        """
        branch_url = os.path.join(self.svn_root, "branches")
        package_url = os.path.join(branch_url, release, 'madman',
                                   'Rpacks', package)
        package_dir = os.path.join(self.bioc_git_repo, package)
        # Configure remote svn url
        config_remote_url = ['git', 'config', '--add',
                             'svn-remote.' + release + '.url', package_url]
        subprocess.check_call(config_remote_url, cwd=package_dir)
        #  remote svn 'fetch' url
        config_remote_fetch = ['git', 'config', '--add',
                               'svn-remote.' + release + '.fetch',
                               ':refs/remotes/git-svn-' + release]
        subprocess.check_call(config_remote_fetch, cwd=package_dir)
        # Fetch
        git_svn_fetch(release, cwd=package_dir)
        # Checkout and change to branch
        checkout = ['git', 'checkout', '-b', release, 'git-svn-' + release]
        subprocess.check_call(checkout, cwd=package_dir)
        # Rebase
        git_svn_rebase(cwd=package_dir)
        # Checkout master
        git_checkout('master', cwd=package_dir, new=False)
        return

    # TODO: Look at the Issue #3 on github to speed this up
    def add_release_branches(self):
        """Add release branches to each package.

        TODO: Extended description of how this works.
        svn_root = file:///home/nturaga/bioconductor-svn-mirror/
        bioc_git_repo: '/home/nturaga/packages_local'
        """
        # Get list of branches
        branch_url = os.path.join(self.svn_root, "branches")
        branch_list = self.get_branch_list()
        for branch in branch_list:
            # Special case to avoid badly named branches in SVN
            package_list_url = os.path.join(branch_url, branch, 'madman',
                                            'Rpacks')
            # Get list of packages for EACH branch
            # TODO: This is not CORRECT
            package_list = self.get_pack_list(package_list_url)
            for package in package_list:

                git_package_dir = os.path.join(self.bioc_git_repo, package)
                package_url = os.path.join(package_list_url, package)
                log.info("git_package_dir:\n %s, package_url:\n %s" %
                         (git_package_dir, package_url))
                if package in os.listdir(self.bioc_git_repo):
                    try:
                        log.info("Adding release branches to package: %s"
                                 % package)
                        if not git_branch_exists(branch, git_package_dir):
                            self.add_orphan_branch_points(branch, package)
                            log.info("Add orphan branch: %s" % git_package_dir)
                    except OSError as e:
                        log.error("Error: Package missing in repository")
                        log.error(e)
                        pass
                    except subprocess.CalledProcessError as e:
                        log.error("Branch: %s, Package: %s, Error: %s"
                                  % (branch, package, e.output))
                else:
                    log.warning("Package %s not in directory" % package)
        return "Finished adding release branches"

    def _svn_revision_branch_id(self, svn_url):
        """SVN stop on copy."""
        output = subprocess.check_output(['svn', 'log', '--stop-on-copy',
                                          '--verbose', svn_url])
        # parse output
        revision_id = re.findall('\(from [^:]+:([0-9]+)', output)[-1]
        return revision_id

    def find_branch_points(self, from_revision, package, release):
        """Find branch points in the git revision history."""
        package_dir = os.path.join(self.bioc_git_repo, package)
        cmd = ['git', 'log', '--format=%H', release]
        branch_root = subprocess.check_output(cmd, cwd=package_dir).split()[-1]
        # Be careful, as there is an empty string at end of list
        commits = subprocess.check_output(['git', 'svn', 'log',
                                           '--oneline', '--show-commit',
                                           'master'],
                                          cwd=package_dir).split("\n")
        # Remove new line char artifact
        commits = [item for item in commits if len(item) != 0]

        for commit in commits:
            commit_info = commit.split(" | ")
            revision = commit_info[0].strip()
            if (int(revision[1:]) <= int(from_revision[release])):
                sha1 = subprocess.check_output(['git', 'log', '-n', '1',
                                                '--format=%H',
                                                commit_info[1].strip()],
                                               cwd=package_dir)
                # Make tuple and strip sha's for whitespace
                branch_point = (branch_root.strip(), sha1.strip())
                return branch_point
        return None

    def release_revision_dict(self, branch_list):
        """Make a dictionary with key = svn_release and value = revision_id."""
        rel_rev_dict = {}  # Dictionary
        branch_url = self.svn_root + "/branches"
        for release in branch_list:
            svn_branch_url = branch_url + "/" + release
            revision = self._svn_revision_branch_id(svn_branch_url)
            rel_rev_dict[release] = revision
        return rel_rev_dict

    def graft(self, package, release, release_revision_dict):
        """Write graft file in each pacakage, connecting the branches.

        The graft file contains the parent commit_id and the orphan-branch
        commit_id. It connects the two by adding the commit history.
        """
        cwd = os.path.join(self.bioc_git_repo, package)
        log.info("Graft package directory: %s" % cwd)
        branch_point = self.find_branch_points(release_revision_dict, package, release)
        if branch_point:
            offspring_sha1, parent_sha1 = branch_point
            with open(os.path.join(cwd, ".git/info/grafts"), 'a') as f:
                f.write(offspring_sha1 + " " + parent_sha1 + "\n")
            graft_range = parent_sha1 + ".." + release
            git_filter_branch(graft_range, cwd=cwd)
        return

    def add_commit_history(self):
        """
        Add commit history by fixing b.

        .git/info/grafts file. By calling git filter-branch the grafts
        are placed in the specific branch.
        """
        # Get list of branches
        branch_list = self.get_branch_list()
        release_revision_dict = self.release_revision_dict(branch_list)
        branch_url = self.svn_root + "branches"
        for release in branch_list:
            packs = self.get_pack_list(os.path.join(branch_url, release,
                                                    'madman', 'Rpacks'))
            for package in packs:
                try:
                    self.graft(package, release, release_revision_dict)
                except OSError as e:
                    log.error("Package not found: %s" % package)
                    log.error(e)
                    pass
        return

    def create_bare_repos(self):
        """Create bare repos in the repository directory.

        This needs to be run from within the bioc_git_repo directory.
        """
        for package in os.listdir(os.path.abspath(self.bioc_git_repo)):
            try:
                git_clone(os.path.join(self.bioc_git_repo, package),
                          self.bare_git_repo, bare=True)
                # TODO: Check if this is needed if the repo is NOT coped.
                # Git update server, so that info/refs is populated,
                # making the server "smart".
                cmd = ['git', 'update-server-info']
                subprocess.check_call(cmd, cwd=os.path.join(self.bare_git_repo,
                                      package + ".git"))
            except subprocess.CalledProcessError as e:
                log.error("Package: %s, Error creating bare repository: %s" % (
                          package, e))
                pass
            except OSError as e:
                log.error("Package: %s, Error: %s" % (package, e))
                pass
        return

    def clone_new(self, new_package_url):
        """Clone a new package into Bioc Git repo.

        This function is used to add a new package to the bioconductor
        repository and reconfigure remotes after cloning the package.
        """
        log.info("Cloning NEW Bare repository to bioc_git_repo")
        package_dir = git_clone(new_package_url, self.bare_git_repo, bare=True)
        git_remote_rename(package_dir, 'origin', 'upstream')
        git_remote_add('origin', package_dir, package_dir)
        return
