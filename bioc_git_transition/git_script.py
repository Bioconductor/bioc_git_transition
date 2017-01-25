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


def get_branch_list(svn_root):
    """Get list of branches."""
    branch_url = svn_root + "branches"
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


svn_root = "file:///home/nturaga/bioconductor-svn-mirror"
repo_dir = "/home/nturaga/packages"

# TODO: construct branch_url within this function (package_url)
def add_orphan_branch_points(svn_root, release, repo_dir, package):
    """Add orphan branch."""
    package_url = svn_root + '/branches/' + release + '/madman/Rpacks/' + package 
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


def add_release_branches(local_svn_dump, git_repo):
    """Add release branches to each package.

    TODO Extended description of how this works.
    local_svn_dump = file:///home/nturaga/bioconductor-svn-mirror/

    remote_svn_server: 'https://hedgehog.fhcrc.org/bioconductor/'
    git_repo: '/home/nturaga/packages_local'
    """
    # Get list of branches
    branch_url = os.path.join(local_svn_dump, "branches")
 	# TODO: Sort branch list based on the order of RELEASE
    branch_list = get_branch_list(local_svn_dump)
    print("Branch list: ", branch_list)

    for branch in branch_list:
        # Special case to avoid badly named branches in SVN
        package_list_url = os.path.join(branch_url, branch, 'madman', 'Rpacks')
        # Get list of packages for EACH branch
        print(package_list_url)
        package_list = sd.get_pack_list(package_list_url)
#        import pdb; pdb.set_trace()
        for package in package_list:

            git_package_dir = os.path.join(git_repo, package)
            package_url = os.path.join(package_list_url, package)
            print("git_package_dir:\n %s, package_url:\n %s" %
                  (git_package_dir, package_url))
            if package in os.listdir(git_repo):
                try:
                    print("in the try statement")
                    if not _branch_exists(branch, git_package_dir):
                        add_orphan_branch_points(svn_root, branch,repo_dir, package)
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

#add_release_branches(svn_root, "/home/nturaga/packages")

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
                                            '--format=%H', commit_info[1].strip()],
                                           cwd=package_dir)
			# Make tuple and strip sha's for whitespace
            branch_point = (branch_root.strip(), sha1.strip())
            return branch_point
    return None


def release_revision_dict(svn_root, branch_list):
    d = {}  # Dictionary
    branch_url = svn_root + "/branches"
    for release in branch_list:
        svn_branch_url = branch_url + "/" + release
        revision = _svn_revision_branch_id(svn_branch_url)
        d[release] = revision
    return d


branch_url = os.path.join(svn_root, "branches")
    # Get list of branches
branch_list = [item.replace('/', '')
               for item in
               subprocess.check_output(['svn', 'list', branch_url]).split()
               if 'RELEASE' in item]
d = release_revision_dict(svn_root, branch_list)
for k,v in d.iteritems():
    print k, v


def graft(repo_dir, package, release, d):
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
    
graft("/home/nturaga", "Biostrings", "RELEASE_3_4", d)
graft("/home/nturaga", "Biostrings", "RELEASE_3_3", d)
graft("/home/nturaga", "Biostrings", "RELEASE_3_2", d)


def add_commit_history(local_svn_dump, repo_dir):
    """
    Add commit history by fixing b.

    .git/info/grafts file. By calling git filter-branch the grafts
    are placed in the specific branch.
    """
    # Get list of branches
    branch_list = get_branch_list(local_svn_dump)
    d = release_revision_dict(local_svn_dump, branch_list)
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
    cmd = ['git', 'clone', '--bare', os.path.join(repo_dir,package)]
    subprocess.check_call(cmd, cwd=destination_dir)
    return

bare_repo("/home/nturaga", "packages_dest", "Biostrings")

def create_bare_repos(repo_dir, destination_dir):
    for package in os.listdir(os.path.abspath(repo_dir)):
        try:
            bare_repo(repo_dir, destination_dir, package)
        except CalledProcessError as e:
            print("Package: %s, Error creating bare repository: %s" % (package, e))
            pass
        except OSError as e:
            print("Package: %s, Error: %s" % (package, e))
            pass
    return

 
