#! /usr/bin/env python
# Author: Nitesh Turaga
# nitesh.turaga@roswellpark.org
import os
import subprocess
from git_api.git_api import git_lfs_track
from git_api.git_api import git_add
from git_api.git_api import git_commit
import logging as log


class Lfs:
    """This is a modified version of add_data.py.

    Add data content to data package.

    In this svn repository, the data subdir of a package is
    stored separately in svn.  add_data.py can be used to add
    the data subdir to a given package.

    The appropriate data dir will be added to the specified package.
    """

    def __init__(self, svn_root, trunk, data_store_path, ref_file):
        self.svn_root = svn_root
        self.trunk = trunk
        self.data_store_path = data_store_path
        self.ref_file = ref_file
        return

    def parse_external_refs(self, package):
        path = package + "/" + self.ref_file
        with open(path) as f:
            refs = f.readlines()
            refs = map(str.strip, refs)
        return refs

    def list_files(self, path):
        ans = [os.path.join(root, f)
               for root, subdir, files in os.walk(path)
               for f in files]
        return [item[len(path)+1:] for item in ans]

    def add_data(self, package):
        before_files = self.list_files(package)
        try:
            refs = self.parse_external_refs(package)
        except IOError, err:
            log.debug("No data to add (no %s file)" % err.filename)
            return
        for ref in refs:
            src = "/".join([self.svn_root, self.trunk,
                            self.data_store_path, package, ref])
            dest = "/".join([package, ref])
            cmd = ['svn', 'export', '--username', 'readonly', '--password',
                   'readonly', '--non-interactive', src, dest]
            subprocess.check_call(cmd)

        after_files = self.list_files(package)
        self.lfs_files = list(set(after_files) - set(before_files))
        return self.lfs_files

    def add_data_as_lfs(self, package):
        """Add data as git LFS."""
        print ("Package path: ", os.path.abspath(package))
        for item in self.lfs_files:
            # Add files
            git_add(item, cwd=os.path.abspath(package))
            git_lfs_track(item, cwd=os.path.abspath(package))
            print("Adding file: ", item)
            # Track all files using lfs
        git_add(".gitattributes", cwd=os.path.abspath(package))
        for item in self.lfs_files:
            git_add(item, cwd=os.path.abspath(package))
        return self.lfs_files

    def commit_data_to_lfs(self, package):
        """Commit data as LFS to server."""
        git_commit(cwd=package)
        return
