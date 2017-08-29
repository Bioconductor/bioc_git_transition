#!/usr/bin/env python

import subprocess
import sys
import fileinput

# Global variables used by pre-recieve hook

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

def prevent_duplicate_commits(oldrev, newrev, refname):
    """Pre-receive hook to check for duplicate commits."""
    try:
        commit_list = subprocess.check_output(["git",
                                               "rev-list",
                                               newrev, "-n", "20"])
    except Exception as e:
        print("Exception: %s" % e)
        pass
    commit_list = commit_list.split("\n")
    commit_list = [item for item in commit_list if len(item)>0]
    # For each of the first 10 pairs, check diff

    for i in xrange(len(commit_list) - 1):
        first = commit_list[i]
        second = commit_list[i+1]

        # use 'show' to test for empty commits,
        # else git diff will report no diffs
        body1 = subprocess.check_output(["git", "show",
                                         "--format=%b", first]).strip()
        if not body1:
            continue

        body2 = subprocess.check_output(["git", "show",
                                         "--format=%b", second]).strip()
        if not body2:
            continue

        # Get diff of two commits
        diff = subprocess.check_output(["git", "diff", first, second])
        # If the diff of two commits is empty, means they are the same.
        # i.e duplicate
        if not diff:
            print(ERROR_DUPLICATE_COMMITS % (first, second))
            sys.exit(1)
    return
