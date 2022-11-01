#!/usr/bin/env python3

import subprocess
import sys
import re
import os

# Global variables used by pre-recieve hook


SVN_COMMIT_REGEX = re.compile(".*git-svn-id: .*@([0-9]{6})")
ZERO_COMMIT = "0000000000000000000000000000000000000000"
ERROR_DUPLICATE_COMMITS = """Error: duplicate commits.

There are duplicate commits in your commit history, These cannot be
pushed to the Bioconductor git server. Please make sure that this is
resolved.

Take a look at the documentation to fix this,
https://bioconductor.org/developers/how-to/git/sync-existing-repositories/,
particularly, point #8 (force Bioconductor master to Github master).

For more information, or help resolving this issue, contact
<bioc-devel@r-project.org>. Provide the error, the package name and
any other details we might need.

Use

    git show %s
    git show %s

to see body of commits.
"""

def bytes2str(line):
    if isinstance(line, str):
        return line
    try:
        line = line.decode()  # decode() uses utf-8 encoding by default
    except UnicodeDecodeError:
        line = line.decode("iso8859")  # typical Windows encoding
    return line

def get_svn_revision(commit):
    body = subprocess.check_output([ "git", "show", "--format=%b", commit ])
    body = bytes2str(body)
    revision = SVN_COMMIT_REGEX.match(body)
    if revision != None:
        revision = revision.group(1)
    return revision

def prevent_duplicate_commits(newrev):
    """Pre-receive hook to check for duplicate SVN commits."""
    try:
        commit_list = subprocess.check_output([
            "git", "rev-list", newrev, "-n", GIT_COMMIT_LIST_LENGTH
        ])
    except Exception as e:
        print("Exception: %s" % e)
        pass
    commit_list = bytes2str(commit_list)
    commit_list = commit_list.split("\n")
    commit_list = [item for item in commit_list if len(item)>0]

    # For each of the first GIT_COMMIT_LIST_LENGTH pairs, check diff
    for i in range(len(commit_list) - 1):
        first = commit_list[i]
        second = commit_list[i+1]

        rev1 = get_svn_revision(first)
        rev2 = get_svn_revision(second)
        if rev1 and (rev1 == rev2):
            diff = subprocess.check_output(["git", "diff", first, second])
            # If the diff of two commits is empty, means they are the same.
            # i.e duplicate
            if not diff:
                print(ERROR_DUPLICATE_COMMITS % (first, second))
                sys.exit(1)
    return


if __name__ == "__main__":
    print("""Usage: 
    python detect_duplicate_commits.py <package_path> <number_of_commits_to_check>
    
    example:

    'python detect_duplicate_commits.py /mypath/BiocGenerics 100'

    NOTE: this script will stop at the first instance of a duplicate commit.
    """)
    package_path = sys.argv[1]
    GIT_COMMIT_LIST_LENGTH = sys.argv[2]
    os.chdir(package_path)
    
    revs = subprocess.check_output([
        "git", "log", "-2", "--format=%H"
    ]).splitlines()
    newrev = revs[0].strip()
    prevent_duplicate_commits(newrev)
