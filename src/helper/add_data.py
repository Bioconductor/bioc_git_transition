#! /usr/bin/env python

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

TODO="""
* Add sanity checks:

  - Is the right svn working copy
  - PKG is found and is working copy

"""

import os
import os.path
import sys


def get_data_src_path(pkg, dir):
    p = [svn_root + trunk + data_store_path, pkg, dir]
    return '/'.join(p)

def get_data_dest_path(pkg, dir):
    p = ['.', pkg, dir]
    return '/'.join(p)

def parse_external_refs(pkg, fh):
    refs = []
    for line in fh:
        line = line.strip()
        if line:
            src = get_data_src_path(pkg, line)
            dest = get_data_dest_path(pkg, line)
            refs.append((src, dest))
    return refs

def add_data(pkg):
    if pkg[-1] == '/':
        pkg = pkg[0:-1]
    print ""
    print "add_data.py: ADDING DATA TO '%s' PACKAGE ..." % pkg
    try:
        fh = file(os.path.join(pkg, ref_file), 'r')
    except IOError, err:
        print "add_data.py: no data to add (no %s file)" % err.filename
        return
    refs = parse_external_refs(pkg, fh)
    for src, dest in refs:
        print "add_data.py: adding", dest
        cmd = ' '.join(['svn', 'export --username readonly --password readonly --non-interactive', src, dest])
        os.system(cmd)
    print "add_data.py: DONE."
    return

def show_help():
    print usage
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        show_help()
    for i in range(1, len(sys.argv)):
        add_data(sys.argv[i])
