#! /usr/bin/env python
"""Module to create LFS based experiment data packages.

Add data content to data package.

In this svn repository, the data subdir of a package is
stored separately in svn.  add_data.py can be used to add
the data subdir to a given package.

The appropriate data dir will be added to the specified package.
"""

import os
import subprocess
from git_api.git_api import git_lfs_track
from git_api.git_api import git_add
from git_api.git_api import git_commit
import logging as log
from local_svn_dump import Singleton


class Lfs:
    """Create git LFS based experiment data packages."""
    __metaclass__ = Singleton

    def __init__(self, svn_root, trunk, data_store_path, ref_file,
                 temp_git_repo):
        """Initialize LFS class."""
        self.svn_root = svn_root
        self.trunk = trunk
        self.data_store_path = data_store_path
        self.ref_file = ref_file
        self.temp_git_repo = temp_git_repo
        return

    def parse_external_refs(self, package):
        """Parse external refs file, and return a list of data references."""
        path = package + "/" + self.ref_file
        with open(path) as f:
            refs = f.readlines()
            refs = map(str.strip, refs)
        return refs

    def list_files(self, path):
        """List files in a path."""
        ans = [os.path.join(root, f)
               for root, subdir, files in os.walk(path)
               for f in files]
        return [item[len(path)+1:] for item in ans]

    def add_data(self, package):
        """Add data from SVN data source to each package."""
        package_dir = os.path.join(self.temp_git_repo, package)
        before_files = self.list_files(package_dir)
        try:
            # Get references from external_data_source.txt
            refs = self.parse_external_refs(package_dir)
        except IOError, err:
            log.debug("Error: No data : missing file %s, in package %s "
                      % (err.filename, package))
            return
        for ref in refs:
            src = "/".join([self.svn_root, self.trunk,
                            self.data_store_path, package, ref])
            dest = "/".join([package_dir, ref])
            try:
                cmd = ['svn', 'export', '--username', 'readonly', '--password',
                       'readonly', '--non-interactive', src, dest]
                print "CMD to add data: ", cmd
                subprocess.check_call(cmd)
            except Exception as e:
                log.debug("Error adding ref: %s, package: %s" % (ref, package))
                log.debug(e)
                pass
        after_files = self.list_files(package_dir)
        # Add list of files newly added to object.
        self.lfs_files = list(set(after_files) - set(before_files))
        return

    def add_data_as_lfs(self, package):
        """Add data as git LFS."""
        package_dir = os.path.join(self.temp_git_repo, package)
        for item in self.lfs_files:
            # Add files
            git_add(item, cwd=package_dir)
            git_lfs_track(item, cwd=package_dir)
            # Track all files using lfs
        git_add(".gitattributes", cwd=package_dir)
        for item in self.lfs_files:
            git_add(item, cwd=package_dir)
        return

    def commit_data_to_lfs(self, package):
        """Commit data as LFS to server."""
        package_dir = os.path.join(self.temp_git_repo, package)
        git_commit(message="Adding external data files as LFS",
                   cwd=package_dir)
        return

    def run_lfs_transition(self, temp_git_repo):
        """Run LFS transition on all package."""
        try:
            for package in os.listdir(os.path.abspath(temp_git_repo)):
                if "bioc-data-experiment" not in package:
                    log.info("LFS: Add data to package %s" % package)
                    self.add_data(package)
                    log.info("LFS: Add data as LFS to package %s" % package)
                    self.add_data_as_lfs(package)
                    log.info("LFS: Commit data as LFS to package %s" % package)
                    self.commit_data_to_lfs(package)
        except Exception as e:
            log.debug("LFS: Error in package : %s : " % package)
            log.debug(e)
        return
