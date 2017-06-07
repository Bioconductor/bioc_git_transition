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
import sys
import subprocess
from src.git_api.git_api import git_filter_branch
from src.git_api.git_api import git_clone
from src.git_api.git_api import git_remote_add
from src.git_api.git_api import git_checkout
from local_svn_dump import Singleton
# Logging configuration
import logging


class GitManifestRepository(object):
    """Git Bioconductor Repository."""
    __metaclass__ = Singleton

    # TODO: change bare_git_repo to admin_repo
    def __init__(self, svn_root, temp_git_repo, bare_git_repo, remote_url,
                 package_path, manifest_name):
        """Initialize Git Bioconductor repository."""
        self.svn_root = svn_root
        self.temp_git_repo = temp_git_repo
        self.bare_git_repo = bare_git_repo
        self.remote_url = remote_url
        self.package_path = package_path
        self.manifest_name = manifest_name
        return

    def get_branch_list(self):
        """Get list of branches.

        Input:
            svn_root path.
        Return:
            List of branches in the reverse order of releases, i.e,
            latest first.
        """
        branch_url = os.path.join(self.svn_root, "branches")
        branch_list = [item.replace('/', '')
                       for item in
                       subprocess.check_output(['svn',
                                                'list',
                                                branch_url]).split()
                       if "RELEASE" in item]
        return branch_list

    def manifest_clone(self, new=True):
        if not new:
            return
        svndump_dir = self.svn_root + '/' + 'trunk' + self.package_path
        try:
            cmd = ['git', 'svn', 'clone',
                   '--include-paths=bioc_.*.manifest', svndump_dir]
            subprocess.check_call(cmd, cwd=self.temp_git_repo)
            logging.info("manifest clone pass %s" % cmd)
        except subprocess.CalledProcessError as e:
            logging.error("Error : %s in package %s" % e)
        except Exception as e:
            logging.error("Unexpected error: %s" % e)
        return

    def add_config(self, release):
        """Add git config options for manifest repo."""
        package_dir = self.temp_git_repo + "/" + "Rpacks"
        # TODO:Error in RELEASE_1_0_branch
        manifest_file = ('bioc_' +
                         release.replace("RELEASE_", "").replace("_", ".") +
                         '.manifest')
        try:
            # config add include path
            include_paths = ['git', 'config', '--add',
                             'svn-remote.' + release + '.include-paths',
                             manifest_file]
            subprocess.check_call(include_paths, cwd=package_dir)
            logging.debug("include paths: %s" % include_paths)
            remote_url = ['git', 'config', '--add',
                          'svn-remote.' + release + '.url',
                          self.svn_root + '/' + 'branches' + '/' + release +
                          self.package_path]
            subprocess.check_call(remote_url, cwd=package_dir)
            logging.debug("remote_url: %s" % remote_url)
            remote_fetch = ['git', 'config', '--add',
                            'svn-remote.' + release + '.fetch',
                            ':refs/remotes/git-svn-' + release]
            subprocess.check_call(remote_fetch, cwd=package_dir)
            logging.debug("remote_fetch: %s" % remote_fetch)
        except Exception as e:
            logging.error(e)
        return

    def add_orphan_branch_points(self):
        """Add orphan branch points to manifest repo."""
        package_dir = self.temp_git_repo + '/' + 'Rpacks'
        branches = self.get_branch_list()
        for release in branches:
            self.add_config(release)
        # Try git_svn_fetch('--all', cwd=package_dir)
        fetch = ['git', 'svn', 'fetch', '--all']
        subprocess.check_call(fetch, cwd=package_dir)
        logging.debug("add_orphan_branch_points: %s " % fetch)
        return

    def _svn_revision_branch_id(self, svn_url):
        """SVN stop on copy."""
        output = subprocess.check_output(['svn', 'log', '--stop-on-copy',
                                          '--verbose', svn_url])
        # parse output
        revision_id = re.findall('\(from [^:]+:([0-9]+)', output)[-1]
        return revision_id

    def release_revision_dict(self, branch_list):
        """Make a dictionary with key = svn_release and value = revision_id."""
        rel_rev_dict = {}  # Dictionary
        branch_url = self.svn_root + "/branches"
        for release in branch_list:
            svn_branch_url = branch_url + "/" + release
            revision = self._svn_revision_branch_id(svn_branch_url)
            rel_rev_dict[release] = revision
            logging.debug("release: %s, revision %s" % (release, revision))
        return rel_rev_dict

    def find_branch_points(self, from_revision, release):
        """Find branch points in the git revision history."""
        package_dir = self.temp_git_repo + '/' + 'Rpacks'
        # Get branch root from git-svn-RELEASE_x_y
        cmd = ['git', 'log', '--format=%H', 'git-svn-' + release]
        branch_root = subprocess.check_output(cmd, cwd=package_dir).split()[-1]
        logging.debug("find branch points:  %s" % cmd)
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

    def graft(self, release, release_revision_dict):
        """Write graft file in each pacakage, connecting the branches.

        The graft file contains the parent commit_id and the orphan-branch
        commit_id. It connects the two by adding the commit history.
        """
        package_dir = self.temp_git_repo + "/" + "Rpacks"
        logging.info("Graft package directory: %s" % package_dir)
        branch_point = self.find_branch_points(release_revision_dict, release)
        if branch_point:
            offspring_sha1, parent_sha1 = branch_point
            logging.debug("offspring_sha1: %s , parent_sha1: %s" %
                          (offspring_sha1, parent_sha1))
            with open(os.path.join(package_dir, ".git/info/grafts"), 'a') as f:
                f.write(offspring_sha1 + " " + parent_sha1 + "\n")
            graft_range = parent_sha1 + ".." + 'git-svn-' + release
            logging.debug("Graft range: %s" % graft_range)
            git_filter_branch(graft_range, cwd=package_dir)
        return

    def prune_branch(self, release):
        package_dir = self.temp_git_repo + "/" + "Rpacks"
        prune = ['git', 'filter-branch', '-f',
                 '--prune-empty', 'git-svn-' + release]
        logging.debug("Starting Pruning in branch: %s" % release)
        logging.debug("prune command: %s" % prune)
        subprocess.check_call(prune, cwd=package_dir)
        logging.debug("Pruning ended: %s" % release)
        return

    def add_commit_history(self, manifest_name):
        """
        Add commit history by fixing b.

        .git/info/grafts file. By calling git filter-branch the grafts
        are placed in the specific branch.
        """
        package_dir = self.temp_git_repo + '/' + 'Rpacks'
        # Get list of branches
        branch_list = self.get_branch_list()
        release_revision_dict = self.release_revision_dict(branch_list)
        l = ['RELEASE_1_0', 'RELEASE_1_0_branch',
             'RELEASE_1_4', 'RELEASE_1_4_branch',
             'RELEASE_1_5']
        branch_list_diff = list(set(branch_list) - set(l))
        for release in branch_list_diff:
            try:
                logging.info("Adding graft for release: %s" % release)
                # TODO: Bug here
                self.graft(release, release_revision_dict)
            except OSError as e:
                logging.error("Grafting Error: %s, Package not found: %s" %
                              (e, release))
                pass
            except:
                e = sys.exc_info()[0]  # Catch all exceptions
                logging.error("Unexpected Grafting Error: %s in package: %s" %
                              (e, release))
                pass

            # Prune branch
            self.prune_branch(release)
            # after prune checkout new branch
            logging.debug("Add commit history: git_checkout release")
            subprocess.check_call(['git', 'checkout',
                                  '-b', release, 'git-svn-' + release],
                                  cwd=package_dir)
            logging.debug("Add commit history:  git_checkout master")
            git_checkout('master', cwd=package_dir,  new=False)
        # rename repository to manifest
        os.rename(package_dir, self.temp_git_repo + '/' + self.manifest_name)
        return

    # TODO: bare_git_repo has to change to admin_repo
    def create_bare_repos(self):
        try:
            package_dir = os.path.join(self.temp_git_repo, self.manifest_name)
            git_clone(package_dir, self.bare_git_repo, bare=True)
        except Exception as e:
            logging.error("Error while making a bare clone for %s" %
                          package_dir)
            logging.error(e)
        return

    def add_remote(self):
        """Add git remote to make the directory.

        Usage: cd /home/git/packages and run function.
        """
        logging.info("Adding remote url to bare git repo.")
        try:
            remote = self.remote_url + self.manifest_file + ".git"
            # Run remote command
            package = os.path.join(self.bare_git_repo, self.manifest_file +
                                   ".git")
            git_remote_add('origin', remote, package)
            logging.info("Add remote to package: %s" % package)
        except Exception as e:
            logging.error(e)
        return
