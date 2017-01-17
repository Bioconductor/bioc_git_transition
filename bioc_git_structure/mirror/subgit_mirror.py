#!/usr/bin/env python
###############################################################################
# By Jim Hester
# Created: 2015 Mar 31 10:17:20 AM
# Last Modified: 2015 Jun 26 01:36:42 PM
# Title:subgit_mirror.py
# Purpose:Create a new subgit mirror from a svn directory
###############################################################################

import argparse
import subprocess
import xml.etree.ElementTree as ET
import re
import fileinput
import os

def find_revision(package):

  log = subprocess.check_output(['svn', 'log', '--xml', '-r1:HEAD', '--limit', '1',
                         "{svn}/{trunk}/{package}".format(svn = args.svn,
                                                          trunk = args.trunk,
                                                          package = args.package)])
  # get the revision from the first (only) log entry
  return ET.fromstring(log).find('logentry').attrib['revision']

def main():
  parser = argparse.ArgumentParser(description='Create a new subgit mirror from a svn directory')
  parser.add_argument("--svn", default = 'https://hedgehog.fhcrc.org/bioconductor')
  parser.add_argument('--trunk', default = 'trunk/madman/Rpacks')
  parser.add_argument('--branch', default = 'branches/RELEASE_*/madman/Rpacks')
  parser.add_argument('--authors')
  parser.add_argument('--revision', help = 'revision to start with, automatically determined if not supplied')
  parser.add_argument('--install', help = 'additional arguments passed to subgit install')
  parser.add_argument('--configure', help = 'additional arguments passed to subgit configure')
  parser.add_argument('package', help = 'package to setup mirror for')
  parser.add_argument('location', nargs = '?')

  global args
  args = parser.parse_args()

  if not args.revision:
    args.revision = find_revision(args.package)

  if not args.location:
    args.location = args.package + '.git'

  configure_call = ['subgit',
                    'configure',
                    args.svn,
                    args.package + '.git']

  if args.configure:
    configure_call[2:2] = args.configure

  subprocess.check_call(configure_call)

  for line in fileinput.input(os.path.join(args.location, "subgit", "config"),
                              inplace = True):
    line = line.rstrip("\n")
    if re.search(r"^\s*\[svn\]", line):
      print line
      print "\tminimalRevision = {}".format(args.revision)
    elif re.search(r"^\s*trunk\s*=\s*", line):
      print "\ttrunk = {trunk}/{package}:refs/heads/master".format(trunk = args.trunk,
                                                                   package = args.package)
    elif re.search(r"^\s*branches\s*=\s*", line):
      print "\tbranches = {branch}/{package}:refs/heads/release-*".format(branch = args.branch,
                                                                   package = args.package)
    elif re.search(r"^\s*tags\s*=\s*", line):
      print "\ttags ="
    elif re.search(r"^\s*shelves\s*=\s*", line):
      print "\tshelves ="
    elif re.search(r"^\s*idleTimeout\s*=", line):
      print "\tidleTimeout = 0#"
    else:
      print line

  install_call = ['subgit', 'install', args.location]

  if args.install:
    install_call[2:2] = args.install

  subprocess.check_call(install_call)

if __name__ == "__main__":
  main()
