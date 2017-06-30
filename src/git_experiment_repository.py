"""Module to create LFS based experiment data packages.

Add data content to data package.

In this svn repository, the data directory of a package is
stored separately in svn.  add_data.py can be used to add
the data subdir to a given package.

The appropriate data dir will be added to the specified package.

Author: Nitesh Turaga
"""

import os
import subprocess
from git_api.git_api import git_add
from git_api.git_api import git_commit
import logging
#from local_svn_dump import Singleton


class Lfs:
    """Create git LFS based experiment data packages."""
#    __metaclass__ = Singleton

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
        with open(path, 'r') as f:
            refs = list(line for line in (l.strip() for l in f) if line)
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
            logging.error("Error: No data : missing file %s, in package %s "
                          % (err.filename, package))
            return
        for ref in refs:
            # TODO: PATH ISSUE here.
            src = self.svn_root + self.trunk + self.data_store_path + "/" + package + "/" + ref
            dest = "/".join([package_dir, ref])
            try:
                cmd = ['svn', 'export', '--username', 'readonly', '--password',
                       'readonly', '--non-interactive', src, dest]
                subprocess.check_call(cmd)
            except Exception as e:
                logging.error("Error adding ref: %s, package: %s"
                              % (ref, package))
                logging.error(e)
        after_files = self.list_files(package_dir)
        # Add list of files newly added to object.
        self.lfs_files = list(set(after_files) - set(before_files))
        return

    def add_data_as_git_objects(self, package):
        package_dir = os.path.join(self.temp_git_repo, package)
        try:
            # Leaving varible as lfs_files, but these are
            # all the new data files added.
            for item in self.lfs_files:
                # add files to git
                git_add(item, cwd=package_dir)
        except Exception as e:
            logging.error("Error in adding data, package %s" % package)
            logging.error(e)
        return

    def commit_data_as_git_objects(self, package):
        """Commit data as regular git objects."""
        try:
            package_dir = os.path.join(self.temp_git_repo, package)
            msg = "Committing experiment data for %s" % package
            git_commit(msg, cwd=package_dir)
        except Exception as e:
            logging.error("Error in commiting data in package %s" % package)
            logging.error(e)
        return

    def run_data_transition(self, temp_git_repo):
        """Run data transition on all package."""
        for package in os.listdir(os.path.abspath(temp_git_repo)):
            try:
                if "bioc-data-experiment" not in package:
                    logging.info("Experiment data: Add data to package %s"
                                 % package)
                    self.add_data(package)
                    logging.info("Experiment data: Add data to package %s"
                                 % package)
                    self.add_data_as_git_objects(package)
                    logging.info("Experiment data: Commit data to package %s"
                                 % package)
                    self.commit_data_as_git_objects(package)
            except Exception as e:
                logging.error("Experiment data: Error in package %s: "
                              % package)
                logging.error(e)
                pass
        return
