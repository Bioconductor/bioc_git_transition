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


def get_branch_list(branch_url):
    """Get list of branches."""
    branch_list = [item.replace('/', '')
                   for item in
                   subprocess.check_output(['svn', 'list', branch_url]).split()
                   if "RELEASE" in item]
    return branch_list


def git_add_remote(remote_path, path):
    """
    Add git remote to make the directory.

    Usage
    ---------
    cd /home/nturaga/packages
    python add_release_branches.py

    Parameters
    ----------
    path : Path to package
    """
    for pack in os.listdir(path):
        print(os.path.abspath(pack))
        if os.path.isdir(pack) and ".git" in os.listdir(os.path.abspath(pack)):
            remote = remote_path + pack
            print(remote)
            remote_add_cmd = ['git', 'remote', 'add', 'origin', remote]
            print(remote_add_cmd)
            # Run remote command
            proc = subprocess.Popen(remote_add_cmd, cwd=os.path.abspath(pack))
            out, err = proc.communicate()
            print("Added remote to ", os.path.abspath(pack))
    return


def _branch_exists(branch, working_directory):
    """Check if branch exists in git repo."""
    output = subprocess.check_output(['git', 'branch', '--list',
                                      branch], cwd=working_directory)
    return output != ''


def add_orphan_branch_points(branch, package_url, package_dir):
    """Add orphan branch."""
    # Configure remote svn url
    config_remote_url = ['git', 'config', '--add',
                         'svn-remote.' + branch + '.url', package_url]
    subprocess.check_call(config_remote_url, cwd=package_dir)
    # Configure remote svn 'fetch' url
    config_remote_fetch = ['git', 'config', '--add',
                           'svn-remote.' + branch + '.fetch',
                           ':refs/remotes/git-svn-' + branch]
    subprocess.check_call(config_remote_fetch, cwd=package_dir)
    # Fetch
    fetch = ['git', 'svn', 'fetch', 'git-svn-' + branch]
    subprocess.check_call(fetch, cwd=package_dir)
    # Checkout and change to branch
    checkout = ['git', 'checkout', '-b', branch, 'git-svn-' + branch]
    subprocess.check_call(checkout, cwd=package_dir)
    # Rebase
    subprocess.check_call(['git', 'svn', 'rebase'], cwd=package_dir)
    # Checkout master
    subprocess.check_call(['git', 'checkout', 'master'], cwd=package_dir)
    return


def add_release_branches(local_svn_dump, git_repo):
    """Add release branches to each package.

    TODO Extended description of how this works.
    local_svn_dump = file:///home/nturaga/bioconductor-svn-mirror/

    remote_svn_server: 'https://hedgehog.fhcrc.org/bioconductor/'
    git_repo: '/home/nturaga/packages_local'
    """
    # Get list of branches
    branch_url = os.path.join(local_svn_dump, "branches")
    branch_list = get_branch_list(local_svn_dump)

    print("Branch list: ", branch_list)

    for branch in branch_list:
        # Special case to avoid badly named branches in SVN
        package_list_url = os.path.join(branch_url, branch, 'madman', 'Rpacks')
        # Get list of packages for EACH branch
        package_list = sd.get_pack_list(package_list_url)
        for package in package_list:

            git_package_dir = os.path.join(git_repo, package)
            package_url = os.path.join(package_list_url, package)
            print("git_package_dir:\n %s, package_url:\n %s" %
                  (git_package_dir, package_url))
            if package in os.listdir(git_repo):
                try:
                    if not _branch_exists(branch, git_package_dir):
                        add_orphan_branch_points(branch, package_url,
                                                 git_package_dir)
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


def find_branch_points(from_revision, branch, package_dir):
    """Find branch points in the git revision history."""
    cmd1 = ['git', 'log', '--format=%H', branch]
    branch_root = subprocess.check_output(cmd1, cwd=package_dir).split()[-1]
    print("Branch root", branch_root)
    # Be careful, as there is an empty string at end of list
    commits = subprocess.check_output(['git', 'svn', 'log',
                                       '--oneline', '--show-commit', 'master'],
                                      cwd=package_dir).split("\n")

    commits = [item for item in commits if len(item) != 0]

    for commit in commits:
        commit_info = commit.split(" | ")
        revision = commit_info[0].strip()
        sha1 = subprocess.check_output(['git', 'log', '-n', '1',
                                        '--format=%H', commit_info[1].strip()],
                                       cwd=package_dir)
        if (int(revision[1:]) < int(from_revision[branch])):
            branch_point = (branch_root, sha1)
            return branch_point
    # TODO: make more meaningful message
    return None


def add_commit_history(local_svn_dump):
    """
    Add commit history by fixing branch points.

    Branch points found in the `find_branch_points` are written to the
    .git/info/grafts file. By calling git filter-branch the grafts
    are placed in the specific branch.
    """
    branch_url = os.path.join(local_svn_dump, "branches")
    # Get list of branches
    branch_list = [item.replace('/', '')
                   for item in
                   subprocess.check_output(['svn', 'list', branch_url]).split()
                   if 'RELEASE' in item]
    d = {}  # Dictionary
    for branch in branch_list:
        svn_branch_url = branch_url + "/" + branch
        revision = _svn_revision_branch_id(svn_branch_url)
        d[branch] = revision

    for branch in branch_list:
        packs = sd.get_pack_list(os.path.join(branch_url, branch,
                                              'madman', 'Rpacks'))
        for package in packs:
            cwd = os.path.join("/home/nturaga/packages", package)
            print("packge_dir: ", cwd)
            try:
                branch_point = find_branch_points(d, branch, cwd)
                if branch_point:
                    root, sha1 = branch_point
                    with open(os.path.join(cwd, ".git/info/grafts"), 'a') as f:
                        f.write(root + " " + sha1)
                    graft_range = root + ".." + branch
                    subprocess.check_call(['git', 'filter-branch',
                                           '--', graft_range], cwd=cwd)
            except OSError as e:
                print("Package not found", package)
                print(e)
                pass
    return
