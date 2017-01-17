#!/usr/bin/env python
###############################################################################
# By Jim Hester
# Created: 2015 Mar 31 10:17:20 AM
# Last Modified: 2015 Jul 08 02:24:19 PM
# Title:update_description.py
# Purpose:Parse the DESCRPITION file and create a GitHub Description
###############################################################################

import argparse
import requests
import apt_pkg
import os
import json
import re
import urllib
import subprocess
import StringIO
import tempfile
from contextlib import contextmanager

@contextmanager
def tempinput(data):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(data)
    temp.close()
    yield temp.name
    os.unlink(temp.name)

def parse_revision_info(lines):
  descriptions = set()
  path_re = re.compile('^ +[AM] /([^\s]+/DESCRIPTION)\s*')
  for line in lines.split("\n"):
    path_search = path_re.search(line)
    if path_search:
      description = path_search.group(1)
      descriptions.add(description)

  return sorted(list(descriptions))

def clean_whitespace(string):
  """ replace all whitespace with a single space """
  return re.sub(r'\s+', ' ', string)

def parse_description(filename):

  package = {}
  for section in apt_pkg.TagFile(filename):
    if "URL" in section:
      package["URL"] = clean_whitespace(section["URL"])
      if "BugReports" in section:
        package["BugReports"] = clean_whitespace(section["BugReports"])

  return package

def add_description(package):

  print "Adding description for {}".format(package["name"])

  description_text = u"""This is a read-only mirror of the Bioconductor SVN repository. Package\u00A0Homepage:\u00A0http://bioconductor.org/packages/devel/bioc/html/{package}.html{contributions} Bug\u00A0Reports:\u00A0https://support.bioconductor.org/p/new/post/?{encoded_package}{issues}.""".format(
    contributions = u" Contributions:\u00A0{URL}.".format(URL = package["URL"]) if "URL" in package else "",
    encoded_package = urllib.urlencode({'tag_val' : package["name"]}),
    package = package["name"],
    issues = u" or\u00A0{BugReports}".format(BugReports = package["BugReports"]) if "BugReports" in package else ""
  )

  url = args.github_api + '/repos/bioconductor-mirror/{}'.format(package["name"])
  headers = { 'Authorization': 'token {}'.format(args.token) }
  values = {
    'name': package["name"],
    'description': description_text,
    'homepage': ''
  }

  r = requests.patch(url, headers = headers, data = json.dumps(values))
  if not r:
    print r.json()

def main():
  parser = argparse.ArgumentParser(description='Parse the DESCRPITION file and create a GitHub Description')
  parser.add_argument('--token', help = 'Github API token', required = True)
  parser.add_argument('--github-api', help = 'specify the url to the Github API',
                      default = 'https://api.github.com')
  parser.add_argument('--svn', help = 'svn url',
                      default = 'https://hedgehog.fhcrc.org/bioconductor')
  group = parser.add_mutually_exclusive_group(required = True)
  group.add_argument('--package', help = 'the package to add a DESCRIPTION for')
  group.add_argument('--revision', help = 'the revisions to lookup a DESCRIPTION for')

  global args
  args = parser.parse_args()

  if args.package:
    package = parse_description(os.path.join(args.package, "DESCRIPTION"))
    package["name"] = os.path.basename(os.path.normpath(args.package))
    add_description(package)
  else:
    revision_info = subprocess.check_output(["svn", "log", "--verbose", "--stop-on-copy", "-r",
                                             args.revision, args.svn])
    descriptions = parse_revision_info(revision_info)
    for description_path in descriptions:
      description_text = subprocess.check_output(["svn", "cat", "-r", args.revision, os.path.join(args.svn, description_path)])
      with tempinput(description_text) as tempfile:
        package = parse_description(tempfile)
        package["name"] = os.path.basename(os.path.dirname(description_path))

  if package:
    add_description(package)
if __name__ == "__main__":
  main()
