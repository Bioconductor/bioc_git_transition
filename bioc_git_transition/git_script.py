#!/usr/bin/env python

"""Bioconductor Git script docstrings.

This module provides functions for working with the Bioconductor
`git` repository. Once the SVN dump takes place, we add remote branches,
and commit history to each branch as needed.

Author: Nitesh Turaga
Ideas taken from Jim Hester's code in Bioconductor/mirror
"""

import os
import re
import subprocess
import svn_dump as sd
from distutils.version import LooseVersion


def get_branch_list(svn_root):
    """Get list of branches.
    Input:
        svn_root path.
    Return:
        List of branches in the reverse order of releases, i.e, latest first.
    """
    branch_url = svn_root + "branches"
    branch_list = [item.replace('/', '')
                   for item in
                   subprocess.check_output(['svn', 'list', branch_url]).split()
                   if "RELEASE" in item]
    # Reverse branch list based on RELEASE version number
    branch_list = sorted(branch_list, key=LooseVersion)
    return branch_list.revers()


def git_remote_add(name, remote_url, cwd):
    """Git remote add."""
    cmd = ['git', 'remote', 'add', name, remote_url]
    subprocess.check_call(cmd, cwd=cwd)
    return


def add_remote(remote_url, repo_dir):
    """Add git remote to make the directory.

    Usage: cd /home/nturaga/packages and run function.
    """
    for package in os.listdir(repo_dir):
        if ((os.path.isdir(package)) and
                (".git" in os.listdir(os.path.abspath(package)))):
            remote = remote_url + package
            # Run remote command
            git_remote_add('origin', remote, os.path.abspath(package))
            print("Added remote to package: %s" % package)
    return


def _branch_exists(branch, working_directory):
    """Check if branch exists in git repo."""
    output = subprocess.check_output(['git', 'branch', '--list',
                                      branch], cwd=working_directory)
    return output != ''


# TODO: construct branch_url within this function (package_url)
def add_orphan_branch_points(svn_root, release, repo_dir, package):
    """Add orphan branch.

    Configure the remote and fetch urls for git-svn. Then, fetch from the
    svn remote repository. Checkout from the release branch, and rebase it to
    the fetched commits. Checkout master at the end.
    """
    package_url = os.path.join(svn_root, 'branches', release, 'madman',
                               'Rpacks', package)
    # package_url = (svn_root + '/branches/' + release +
    #    '/madman/Rpacks/' + package)
    package_dir = os.path.join(repo_dir, package)
    print(package_url)
    # Configure remote svn url
    config_remote_url = ['git', 'config', '--add',
                         'svn-remote.' + release + '.url', package_url]
    subprocess.check_call(config_remote_url, cwd=package_dir)
    #  remote svn 'fetch' url
    config_remote_fetch = ['git', 'config', '--add',
                           'svn-remote.' + release + '.fetch',
                           ':refs/remotes/git-svn-' + release]
    subprocess.check_call(config_remote_fetch, cwd=package_dir)
    # Fetch
    fetch = ['git', 'svn', 'fetch', release]
    subprocess.check_call(fetch, cwd=package_dir)
    # Checkout and change to branch
    checkout = ['git', 'checkout', '-b', release, 'git-svn-' + release]
    subprocess.check_call(checkout, cwd=package_dir)
    # Rebase
    subprocess.check_call(['git', 'svn', 'rebase'], cwd=package_dir)
    # Checkout master
    subprocess.check_call(['git', 'checkout', 'master'], cwd=package_dir)
    return


def add_release_branches(svn_root, repo_dir):
    """Add release branches to each package.

    TODO: Extended description of how this works.
    svn_root = file:///home/nturaga/bioconductor-svn-mirror/
    repo_dir: '/home/nturaga/packages_local'
    """
    # Get list of branches
    branch_url = os.path.join(svn_root, "branches")
    # TODO: Sort branch list based on the order of RELEASE
    branch_list = get_branch_list(svn_root)
    print("Branch list: ", branch_list)

    for branch in branch_list:
        # Special case to avoid badly named branches in SVN
        package_list_url = os.path.join(branch_url, branch, 'madman', 'Rpacks')
        # Get list of packages for EACH branch
        print(package_list_url)
        package_list = sd.get_pack_list(package_list_url)
#        import pdb; pdb.set_trace()
        for package in package_list:

            git_package_dir = os.path.join(repo_dir, package)
            package_url = os.path.join(package_list_url, package)
            print("git_package_dir:\n %s, package_url:\n %s" %
                  (git_package_dir, package_url))
            if package in os.listdir(repo_dir):
                try:
                    print("in the try statement")
                    if not _branch_exists(branch, git_package_dir):
                        add_orphan_branch_points(svn_root, branch,
                                                 repo_dir, package)
                        print("Added orphan branch in %s " % git_package_dir)
                except OSError as e:
                    print("Error: Package does not exist in repository, ", e)
                    pass
                except subprocess.CalledProcessError as e:
                    print("Branch: %s, Package: %s, Error: %s" %
                          branch, package, e.output)
            else:
                print("Package %s not in directory" % package)
    return "Finished adding release branches"


def _svn_revision_branch_id(svn_url):
    """SVN stop on copy."""
    output = subprocess.check_output(['svn', 'log', '--stop-on-copy',
                                      '--verbose', svn_url])
    # parse output
    revision_id = re.findall('\(from [^:]+:([0-9]+)', output)[-1]
    return revision_id


def find_branch_points(from_revision, repo_dir, package, release):
    """Find branch points in the git revision history."""
    package_dir = os.path.join(repo_dir, package)
    cmd1 = ['git', 'log', '--format=%H', release]
    branch_root = subprocess.check_output(cmd1, cwd=package_dir).split()[-1]
    print("Branch root", branch_root)
    # Be careful, as there is an empty string at end of list
    commits = subprocess.check_output(['git', 'svn', 'log',
                                       '--oneline', '--show-commit', 'master'],
                                      cwd=package_dir).split("\n")
    # Remove new line char artifact
    commits = [item for item in commits if len(item) != 0]

    for commit in commits:
        commit_info = commit.split(" | ")
        revision = commit_info[0].strip()
        if (int(revision[1:]) <= int(from_revision[release])):
            sha1 = subprocess.check_output(['git', 'log', '-n', '1',
                                            '--format=%H',
                                            commit_info[1].strip()],
                                           cwd=package_dir)
            # Make tuple and strip sha's for whitespace
            branch_point = (branch_root.strip(), sha1.strip())
            return branch_point
    return None


def release_revision_dict(svn_root, branch_list):
    """Make a dictionary with key = svn_release and value = revision_id."""
    d = {}  # Dictionary
    branch_url = svn_root + "/branches"
    for release in branch_list:
        svn_branch_url = branch_url + "/" + release
        revision = _svn_revision_branch_id(svn_branch_url)
        d[release] = revision
    return d


def graft(repo_dir, package, release, d):
    """Write graft file in each pacakage, connecting the branches.

    The graft file contains the parent commit_id and the orphan-branch
    commit_id. It connects the two by adding the commit history.
    """
    cwd = os.path.join(repo_dir, package)
    print("packge_dir: ", cwd)
    branch_point = find_branch_points(d, repo_dir, package, release)
    if branch_point:
        offspring_sha1, parent_sha1 = branch_point
        with open(os.path.join(cwd, ".git/info/grafts"), 'a') as f:
            f.write(offspring_sha1 + " " + parent_sha1 + "\n")
        graft_range = parent_sha1 + ".." + release
        subprocess.check_call(['git', 'filter-branch', '--force',
                               '--', graft_range], cwd=cwd)
    return


def add_commit_history(svn_root, repo_dir):
    """
    Add commit history by fixing b.

    .git/info/grafts file. By calling git filter-branch the grafts
    are placed in the specific branch.
    """
    # Get list of branches
    branch_list = get_branch_list(svn_root)
    d = release_revision_dict(svn_root, branch_list)
    branch_url = svn_root + "branches"
    for release in branch_list:
        packs = sd.get_pack_list(os.path.join(branch_url, release,
                                              'madman', 'Rpacks'))
        for package in packs:
            try:
                graft(repo_dir, package, release, d)
            except OSError as e:
                print("Package not found", package)
                print(e)
                pass
    return


def bare_repo(repo_dir, destination_dir, package):
    """Make a bare git repo."""
    cmd = ['git', 'clone', '--bare', os.path.join(repo_dir, package)]
    subprocess.check_call(cmd, cwd=destination_dir)
    return


def create_bare_repos(repo_dir, destination_dir):
    """Create bare repos in the repository directory."""
    for package in os.listdir(os.path.abspath(repo_dir)):
        try:
            bare_repo(repo_dir, destination_dir, package)
        except subprocess.CalledProcessError as e:
            print("Package: %s, Error creating bare repository: %s" % (
                  package, e))
            pass
        except OSError as e:
            print("Package: %s, Error: %s" % (package, e))
            pass
    return
