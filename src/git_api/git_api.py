"""Git API.

This module provides functions for working with the Bioconductor
`git` repository. It gives the required Git API to work it the
bioconductor git server.

Author: Nitesh Turaga
"""
import subprocess
import ntpath
import os


def git_remote_add(name, remote_url, cwd):
    """Git remote add."""
    cmd = ['git', 'remote', 'add', name, remote_url]
    subprocess.check_call(cmd, cwd=cwd)
    return


def git_remote_rename(package_dir, orignal_name, new_name):
    """Git remote rename."""
    cmd = ['git', 'remote', 'rename', orignal_name, new_name]
    subprocess.check_call(cmd, cwd=package_dir)
    return


def git_remote_remove(name, cwd):
    """Git remote remove."""
    cmd = ['git', 'remote', 'remove', name]
    subprocess.check_call(cmd, cwd=cwd)
    return


def git_branch_exists(branch, cwd):
    """Check if branch exists in git repo."""
    output = subprocess.check_output(['git', 'branch', '--list',
                                      branch], cwd=cwd)
    return output != ''


def git_filter_branch(graft_range, cwd):
    """Git filter branch, for a specified graft range."""
    cmd = ['git', 'filter-branch', '--force', '--', graft_range]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, cwd=cwd)
    out, err = proc.communicate()
    return


def git_svn_rebase(cwd):
    """Git svn rebase a package."""
    cmd = ['git', 'svn', 'rebase']
    subprocess.check_call(cmd, cwd=cwd)
    return


def git_svn_fetch(branch, cwd):
    """Git svn fetch branch."""
    cmd = ['git', 'svn', 'fetch', branch]
    subprocess.check_call(cmd, cwd=cwd)
    return


def git_checkout(branch, cwd, new=False):
    """Git checkout branch.

    new=True, this option specifies that branch is `new` and
              needs to be created.
    new=False, this option specifies that branch is present.
    """
    if new:
        cmd = ['git', 'checkout', '-b', branch]
    else:
        cmd = ['git', 'checkout', branch]
    subprocess.check_call(cmd, cwd=cwd)
    return


def path_leaf(path):
    """Get leaf node of the path."""
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def git_clone(repository, directory, bare=True):
    """Make a clone of a git repository.

    Package will be cloned in `directory`, and if `bare=True`
    are bare repository is created, else a regular clone.
    git clone --bare packages/Biostrings temp/Biostrings.git
    """
    destination = os.path.join(directory, path_leaf(repository))
    destination = destination + ".git"
    if bare:
        cmd = ['git', 'clone', '--bare', repository, destination]
    else:
        destination = destination.replace(".git", "")
        cmd = ['git', 'clone', repository, destination]
    subprocess.check_call(cmd)
    return destination


def git_lfs_track(path, cwd):
    """Track files in git lfs."""
    cmd = ['git', 'lfs', 'track', path]
    subprocess.check_call(cmd, cwd=cwd)
    return


def git_add(path, cwd):
    """Add files to git."""
    cmd = ['git', 'add', path]
    subprocess.check_call(cmd, cwd=cwd)
    return


def git_commit(message, cwd):
    """Commit files to git server."""
    cmd = ['git', 'commit', '-m', message]
    subprocess.check_call(cmd, cwd=cwd)
    return

def git_mv(old, new, cwd):
    cmd = ['git', 'mv', old, new]
    subprocess.check_call(cmd, cwd=cwd)
    return

def git_rm(regex, cwd):
    cmd = ['git', 'rm', regex]
    subprocess.check_call(cmd, cwd=cwd)
    return
