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
from git_api import git_remote_add
from git_api import git_filter_branch
from git_api import git_branch_exists
from git_api import git_svn_rebase
from git_api import git_checkout
from git_api import git_svn_fetch
from git_api import git_clone
# Logging configuration
import logging as log

svn_root = 'file:///home/nturaga/bioconductor-svn-mirror/'
svn_root_dir = "bioconductor-svn-mirror/"
remote_svn_server = 'https://hedgehog.fhcrc.org/bioconductor'
bioc_git_repo = "/home/nturaga/packages"
update_file = "updt.svn"
remote_url = "ubuntu@git.bioconductor.org:/packages/"


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
    #  from distutils.version import LooseVersion
    # branch_list = sorted(branch_list, key=LooseVersion)
    # return branch_list.reverse()
    return branch_list


def get_pack_list(path):
    """Get list of packages on SVN."""
    result = subprocess.check_output(['svn', 'list', path])
    return [item.replace('/', '') for item in result.split()]


def add_remote(bioc_git_repo, remote_url):
    """Add git remote to make the directory.

    Usage: cd /home/nturaga/packages and run function.
    """
    for package in os.listdir(bioc_git_repo):
        if ((os.path.isdir(package)) and
                (".git" in os.listdir(os.path.abspath(package)))):
            remote = remote_url + package
            # Run remote command
            git_remote_add('origin', remote, os.path.abspath(package))
            log.info("Added remote to package: %s" % package)
    return


def add_orphan_branch_points(svn_root, release, bioc_git_repo, package):
    """Add orphan branch.

    Configure the remote and fetch urls for git-svn. Then, fetch from the
    svn remote repository. Checkout from the release branch, and rebase it to
    the fetched commits. Checkout master at the end.
    """
    branch_url = os.path.join(svn_root, "branches")
    package_url = os.path.join(branch_url, release, 'madman',
                               'Rpacks', package)
    package_dir = os.path.join(bioc_git_repo, package)
    # TODO: add git config to git_api
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
    git_svn_fetch(release, cwd=package_dir)
    # Checkout and change to branch
    checkout = ['git', 'checkout', '-b', release, 'git-svn-' + release]
    subprocess.check_call(checkout, cwd=package_dir)
    # Rebase
    git_svn_rebase(cwd=package_dir)
    # Checkout master
    git_checkout('master', cwd=package_dir, new=False)
    return


def add_release_branches(svn_root, bioc_git_repo):
    """Add release branches to each package.

    TODO: Extended description of how this works.
    svn_root = file:///home/nturaga/bioconductor-svn-mirror/
    bioc_git_repo: '/home/nturaga/packages_local'
    """
    # Get list of branches
    branch_url = os.path.join(svn_root, "branches")
    # TODO: Sort branch list based on the order of RELEASE
    branch_list = get_branch_list(svn_root)
    for branch in branch_list:
        # Special case to avoid badly named branches in SVN
        package_list_url = os.path.join(branch_url, branch, 'madman', 'Rpacks')
        # Get list of packages for EACH branch
        package_list = get_pack_list(package_list_url)
        for package in package_list:

            git_package_dir = os.path.join(bioc_git_repo, package)
            package_url = os.path.join(package_list_url, package)
            log.info("git_package_dir:\n %s, package_url:\n %s" %
                     (git_package_dir, package_url))
            if package in os.listdir(bioc_git_repo):
                try:
                    log.info("Adding release branches to package: %s"
                             % package)
                    if not git_branch_exists(branch, git_package_dir):
                        add_orphan_branch_points(svn_root, branch,
                                                 bioc_git_repo, package)
                        log.info("Orphan branch added: %s" % git_package_dir)
                except OSError as e:
                    log.error("Error: Package missing in repository")
                    log.error(e)
                    pass
                except subprocess.CalledProcessError as e:
                    log.error("Branch: %s, Package: %s, Error: %s"
                              % (branch, package, e.output))
            else:
                log.warning("Package %s not in directory" % package)
    return "Finished adding release branches"


def _svn_revision_branch_id(svn_url):
    """SVN stop on copy."""
    output = subprocess.check_output(['svn', 'log', '--stop-on-copy',
                                      '--verbose', svn_url])
    # parse output
    revision_id = re.findall('\(from [^:]+:([0-9]+)', output)[-1]
    return revision_id


def find_branch_points(from_revision, bioc_git_repo, package, release):
    """Find branch points in the git revision history."""
    package_dir = os.path.join(bioc_git_repo, package)
    cmd1 = ['git', 'log', '--format=%H', release]
    branch_root = subprocess.check_output(cmd1, cwd=package_dir).split()[-1]
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


def graft(bioc_git_repo, package, release, d):
    """Write graft file in each pacakage, connecting the branches.

    The graft file contains the parent commit_id and the orphan-branch
    commit_id. It connects the two by adding the commit history.
    """
    cwd = os.path.join(bioc_git_repo, package)
    log.info("Graft package directory: %s" % cwd)
    branch_point = find_branch_points(d, bioc_git_repo, package, release)
    if branch_point:
        offspring_sha1, parent_sha1 = branch_point
        with open(os.path.join(cwd, ".git/info/grafts"), 'a') as f:
            f.write(offspring_sha1 + " " + parent_sha1 + "\n")
        graft_range = parent_sha1 + ".." + release
        git_filter_branch(graft_range, cwd=cwd)
    return


def add_commit_history(svn_root, bioc_git_repo):
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
        packs = get_pack_list(os.path.join(branch_url, release,
                                           'madman', 'Rpacks'))
        for package in packs:
            try:
                graft(bioc_git_repo, package, release, d)
            except OSError as e:
                log.error("Package not found: %s" % package)
                log.error(e)
                pass
    return


def create_bare_repos(bioc_git_repo, destination_dir):
    """Create bare repos in the repository directory.

    This needs to be run from within the bioc_git_repo directory.
    """
    for package in os.listdir(os.path.abspath(bioc_git_repo)):
        try:
            git_clone(os.path.join(bioc_git_repo, package), destination_dir,
                      bare=True)
        except subprocess.CalledProcessError as e:
            log.error("Package: %s, Error creating bare repository: %s" % (
                      package, e))
            pass
        except OSError as e:
            log.error("Package: %s, Error: %s" % (package, e))
            pass
    return
