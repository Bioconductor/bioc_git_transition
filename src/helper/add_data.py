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

if 'BBS_SVN_CMD' in os.environ and os.environ['BBS_SVN_CMD'] != "":
    SVN = os.environ['BBS_SVN_CMD']
else:
    SVN = 'svn'

SVN_ROOT = 'file:///home/nturaga/bioc-data-mirror/trunk/experiment'
REF_FILE = 'external_data_store.txt'

def get_data_src_path(pkg, dir):
    p = [SVN_ROOT, 'data_store', pkg, dir]
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
        fh = file(os.path.join(pkg, REF_FILE), 'r')
    except IOError, err:
        print "add_data.py: no data to add (no %s file)" % err.filename
        return
    refs = parse_external_refs(pkg, fh)
    for src, dest in refs:
        print "add_data.py: adding", dest
        cmd = ' '.join([SVN, 'checkout --username readonly --password readonly --non-interactive', src, dest])
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
