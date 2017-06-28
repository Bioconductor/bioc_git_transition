#!/usr/bin/env python

"""Module to create Bioconductor SVN dump and update.

This module provides functions to create an SVN dump and
update the SVN dump before making the git transition.

Author: Nitesh Turaga
"""
import os
import subprocess
import logging


#class Singleton(type):
#    """Singleton Factory pattern."""
#    _instances = {}
#
#    def __call__(cls, *args, **kwargs):
#        if cls not in cls._instances:
#            cls._instances[cls] = super(Singleton, cls).__call__(*args,
#                                                                 **kwargs)
#        return cls._instances[cls]


class LocalSvnDump(object):
    """Local SVN dump."""
    #__metaclass__ = Singleton

    def __init__(self, svn_root, temp_git_repo, users_db, remote_svn_server,
                 package_path):
        """Initialize Loval SVN dump.

        Usage:
        svn_root = 'file:///home/git/hedgehog.fhcrc.org/
        # Initialize dump
        dump = svn_dump(svn_root=svn_root,
                        temp_git_repo="git_repo",
                        users_db="/home/nturaga/user_db.txt")
        """
        self.svn_root = svn_root
        self.svn_root_dir = svn_root.replace("file://", "")
        self.users_db = users_db
        self.remote_svn_server = remote_svn_server
        self.temp_git_repo = temp_git_repo
        self.package_path = package_path

    def get_pack_list(self, branch="trunk"):
        """Get list of packages on SVN."""
        if branch == "trunk":
            path = self.svn_root + "/" + 'trunk' + self.package_path
        else:
            path = os.path.join(self.svn_root, 'branches', branch,
                                self.package_path)
        result = subprocess.check_output(['svn', 'list', path])
        pack_list = result.split()
        packs = [pack.replace("/", "")
                 for pack in pack_list if pack.endswith("/")]
        return packs

    def manifest_package_list(self, manifest_file):
        """Get the package list from Bioconductor manifest file.

        Usage:
            dump.manifest_package_list("bioc_3.4.manifest")
        """
        manifest = (self.svn_root + "/" + "trunk" + self.package_path +
                    "/" + manifest_file)
        cmd = ['svn', 'cat', manifest]
        out = subprocess.check_output(cmd)
        # with open(manifest, 'r') as f:
        doc = out.split("\n")
        package_list = [line.replace("Package: ", "").strip()
                        for line in doc if line.startswith("Package")]
        return package_list

    def search_git_files(self, path):
        """Check if path has pre exisiting .git files."""
        cmd = 'svn list --depth=infinity ' + path + " | grep \\.git"
        try:
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
            output, error = proc.communicate()
        except Exception as e:
            logging.error("Error in search git files: %s" % path)
            logging.error(e)
        return output

    def svn_dump(self, packs):
        """
        Create git svn clone from SVN dump for each package.

        The SVN dump needs to be updated daily/nightly for the rest to
        work as planned.
        """
        package_dir = self.svn_root + '/' + 'trunk' + self.package_path
        for pack in packs:
            package_dump = os.path.join(package_dir, pack)
            # If .git files exsit in package, throw error.
            pre_exisiting_git = self.search_git_files(package_dump)
            if not pre_exisiting_git:
                try:
                    cmd = ['git', 'svn', 'clone',
                           '--authors-file=' + self.users_db, package_dump]
                    subprocess.check_call(cmd, cwd=self.temp_git_repo)
                    logging.debug("Finished git-svn clone for package: %s"
                                  % pack)
                except subprocess.CalledProcessError as e:
                    logging.error("Error : %s in package %s" % (e, pack))
                except Exception as e:  # All other errors
                    logging.error("Unexpected error: %s" % e)
        return

    def svn_get_revision(self):
        """Get revision of current SVN server."""
        # Get revision number
        p = subprocess.Popen(["svn", "info", self.svn_root],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        revision = [line.split(":")[1].strip() for line in out.split("\n")
                    if "Revision" in line]
        revision = int(revision[0])
        self.revision = revision
        logging.info("SVN dump revision: %s" % revision)
        return

    def svn_dump_update(self, update_file):
        """Update SVN dump."""
        # Get svn dump updates, from (revision + 1) till HEAD
        rev = "-r" + str(self.revision + 1) + ":HEAD"
        with open(update_file, 'w') as f:
            proc = subprocess.Popen(['svnrdump', 'dump',
                                    self.remote_svn_server,
                                    rev, '--incremental'], stdout=f,
                                    stderr=subprocess.PIPE)
            ret_code = proc.wait()
            # Write dump update to file
            f.flush()
        logging.info("Finshed dump to local file: %s" % update_file)
        return ret_code

    def update_local_svn_dump(self, update_file):
        """Update Local SVN dump."""
        cmd = ('svnadmin load ' + self.svn_root_dir + ' < ' +
               os.path.abspath(update_file))
        subprocess.call(cmd, shell=True)
        logging.info("Finished dump update")
        return
