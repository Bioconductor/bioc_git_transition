#!/usr/bin/env python
"""Pre-receive hook to check legality of version bumps.

This version check follows the guidelines of the Bioconductor
project. The guidelines are given at this link,
http://bioconductor.org/developers/how-to/version-numbering/.
"""

from __future__ import print_function
import subprocess
import sys
import re


ZERO_COMMIT = "0000000000000000000000000000000000000000"


def eprint(*args, **kwargs):
    """Helper function to print to std err."""
    print(*args, file=sys.stderr, **kwargs)


def throw_error(prev_version, new_version):
    """Throw error message for every version bump failure."""
    message = ("Error: Illegal version bump from '%s' to '%s'. Check \n"
               "http://bioconductor.org/developers/how-to/version-numbering/ \n"
               "for details" % (prev_version, new_version))
    sys.exit(message)
    return


def git_diff(oldrev, newrev, fname):
    """Git diff between two commits."""
    diff = subprocess.check_output(["git",
                                    "diff",
                                    oldrev + ".." + newrev,
                                    "--", fname])
    return diff.splitlines()


def git_diff_pre_commit(fname):
    """Git diff for a pre-commit hook."""
    diff = subprocess.check_output(["git",
                                    "diff",
                                    "--cached", fname])
    return diff.splitlines()


def git_diff_files(oldrev, newrev):
    """Get list of files in diff."""
    files_modified = subprocess.check_output(["git",
                                              "diff",
                                              "--name-only",
                                              oldrev + ".." + newrev])
    return files_modified.splitlines()


def get_version_bump(diff):
    """Get the version bumps in DESCRIPTION file."""
    prev_version = [line.replace("-Version:", "")
                    for line in diff
                    if line.startswith("-Version")]
    new_version = [line.replace("+Version:", "")
                   for line in diff
                   if line.startswith("+Version")]
    ## If versions are equal, no version change
    if prev_version == new_version:
        return None, None
    ## No change in DESCRIPTION file from new package push
    if not prev_version or not new_version:
        return None, None
    return prev_version[0].strip(), new_version[0].strip()


def check_version_format(prev_version, new_version):
    """Check format of version."""
    regex = re.compile('\d{1}\.\d{1,2}\.\d{1,3}$')
    if not regex.match(new_version):
        throw_error(prev_version, new_version)
    try:
        x0, y0, z0 = map(int, prev_version.split("."))
        x, y, z = map(int, new_version.split("."))
    except ValueError as e:
        print('format of version number is wrong', e)
        throw_error(prev_version, new_version)
    return prev_version, new_version


def check_version_in_release(prev_version, new_version):
    """Check version in RELEASE_branch."""
    x0, y0, z0 = map(int, prev_version.split("."))
    x, y, z = map(int, new_version.split("."))
    # x should never change, y should be even, y should not be 99 i.e
    # no major version change
    if (x != x0) or (y % 2 != 0) or (y!=y0) or (y == 99):
        throw_error(prev_version, new_version)
    # z should be incremented
    if not z - z0 >= 0:
        throw_error(prev_version, new_version)
    return


def check_version_in_master(prev_version, new_version):
    """Check version in master branch."""
    x0, y0, z0 = map(int, prev_version.split("."))
    x, y, z = map(int, new_version.split("."))
    # x should never change
    if x != x0:
        throw_error(prev_version, new_version)
    # y should be odd
    if y % 2 == 0:
        throw_error(prev_version, new_version)
    # y should be the same, and can be 99
    if (y != y0) and (y != 99):
        throw_error(prev_version, new_version)
    # z should be incremented and cannot be 99
    # to indicate major version change
    if not (z - z0 >= 0) and (y != 99):
        throw_error(prev_version, new_version)
    return

def check_version_bump(prev_version, new_version, refname):
    """Check the version bump for legality."""
    # Check format of version
    prev_version, new_version = check_version_format(prev_version, new_version)
    if "RELEASE" in refname:
        check_version_in_release(prev_version, new_version)

    if "master" in refname:
        check_version_in_master(prev_version, new_version)
    return 0


def prevent_bad_version_numbers(oldrev, newrev, refname):
    """Prevent bad version numbers in DESCRIPTION file.

    This function acts as the wrapper for all the helper functions.
    """
    if oldrev == ZERO_COMMIT:
        ## https://stackoverflow.com/questions/40883798/how-to-get-git-diff-of-the-first-commit
        ## 4b825dc642cb6eb9a060e54bf8d69288fbee4904 is the
        ## id of the "empty tree" in Git and it's always
        ## available in every repository.
        oldrev = "4b825dc642cb6eb9a060e54bf8d69288fbee4904"
    files_modified = git_diff_files(oldrev, newrev)
    for fname in files_modified:
        if "DESCRIPTION" in fname:
            diff = git_diff(oldrev, newrev, fname)
            prev_version, new_version = get_version_bump(diff)
            if (prev_version is None) and (new_version is None):
                continue
            check_version_bump(prev_version, new_version, refname)
    return
