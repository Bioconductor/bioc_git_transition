#! /usr/bin/env python
import os
import os.path
import sys
import subprocess
from git_api.git_api import git_lfs_track
from git_api.git_api import git_add

usage = """\
This is a modified version of add_data.py.
Author: Nitesh Turaga
nitesh.turaga@roswellpark.org

Usage: add_data.py PKG

Add data content to data package PKG.

Your working directory must contain the package dir PKG.

In this svn repository, the data subdir of a package is
stored separately in svn.  add_data.py can be used to add
the data subdir to a given package.

The appropriate data dir will be added to the specified package.
"""

TODO = """
* Add sanity checks:

  - Is the right svn working copy
  - PKG is found and is working copy
"""


def get_data_src_path(svn_root, trunk, data_store_path, pkg, dir):
    p = [svn_root + trunk + data_store_path, pkg, dir]
    return '/'.join(p)


def get_data_dest_path(pkg, dir):
    p = ['.', pkg, dir]
    return '/'.join(p)


def parse_external_refs(svn_root, trunk, data_store_path, pkg, fh):
    refs = []
    for line in fh:
        line = line.strip()
        if line:
            src = get_data_src_path(svn_root, trunk, data_store_path,
                                    pkg, line)
            dest = get_data_dest_path(pkg, line)
            refs.append((src, dest))
    return refs


def add_data(svn_root, trunk, data_store_path, ref_file, pkg):
    if pkg[-1] == '/':
        pkg = pkg[0:-1]
    print ""
    print "add_data.py: ADDING DATA TO '%s' PACKAGE ..." % pkg
    try:
        fh = file(os.path.join(pkg, ref_file), 'r')
    except IOError, err:
        print "add_data.py: no data to add (no %s file)" % err.filename
        return
    refs = parse_external_refs(svn_root, trunk, data_store_path, pkg, fh)
    for src, dest in refs:
        print "add_data.py: adding", dest
        cmd = ['svn', 'export', '--username', 'readonly', '--password',
               'readonly', '--non-interactive', src, dest]
        subprocess.check_call(cmd)
    print "add_data.py: DONE."
    return



def add_data_as_lfs(ref_file, pkg):
    """Add data as git LFS."""
    package_dir = "/".join(pkg, ref_file)
    files = os.listdir(ref_file)
    return





def show_help():
    print usage
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
    for i in range(1, len(sys.argv)):
        add_data(sys.argv[i])
