#!/usr/bin/env python
"""Pre-receive hook to check for merge markers in commits.

This merge marker and merge conflict check pre-receive hook
tries to prevent maintainers from commiting files with <<<,
>>>, === merge markers in them. This keeps the commit history
clean.
"""

from __future__ import print_function
import subprocess
import sys


ZERO_COMMIT = "0000000000000000000000000000000000000000"


def git_diff_files_with_conflicts(oldrev, newrev):
    """Get list of files in diff."""
    files_modified = subprocess.check_output(['git',
                                              'diff',
                                              '--name-only',
                                              '-G"<<<<<|=====|>>>>>"',
                                              oldrev + ".." + newrev])
    return files_modified.splitlines()


def prevent_merge_markers(oldrev, newrev, refname):
    """Prevent merge markers in files.

    This function prevents merge markers in commits.
    """
    conflicts = git_diff_files_with_conflicts(oldrev, newrev)
    # If number of files with conflicts is > 0
    if conflicts:
        message = ("Error: You cannot commit without resolving merge conflicts.\n"
                   "Unresolved merge conlicts in these files: \n" +
                   ", ".join(conflicts))
        sys.exit(message)
    return
