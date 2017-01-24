#!/usr/bin/env python
"""Bioconductor Git script docstrings.

This module provides documentation as specified by the `Google Python
Style Guide`_. Docstrings may extend over multiple lines. Sections are created
with a section header and a colon followed by a block of indented text.

Author: Nitesh Turaga
Ideas taken from Jim Hester's code in Bioconductor/mirror

Usage:
    `python git_script.py`
"""

import os
import re
import subprocess
import pdb

def _get_pack_list(local_svn_dump):
    """Get list of packages on SVN."""
    result = subprocess.check_output(['svn', 'list', local_svn_dump])
    return [item.replace('/', '') for item in result.split()]


def svn_dump(local_svn_dump, packs):
    """
    Create git svn clone from SVN dump for each package.

    The SVN dump needs to be updated daily/nightly for the rest to
    work as planned.

    Parameters
    ----------
    local_svn_dump : List of Bioconductor packages
        List of Bioconductor packages obtained
        from _get_pack_list(local_svn_dump)

    Returns
    -------
    None
    """
    package_dir = os.path.join(local_svn_dump, 'trunk/madman/Rpacks/')
    for pack in packs:
        package_dump = os.path.join(package_dir, pack)
        subprocess.check_call(['git', 'svn', 'clone', package_dump])
        print("Finished git svn clone from local dump for package: ", pack)
    return


def git_add_remote(remote_path, path):
    """
    Add git remote to make the directory

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


def svn_get_revision(svn_path):
    """
    Summary line.

    # TODO: remove hardcoded packs and update to svn list from hedgehog

    """
    # Get revision number
    p = subprocess.Popen(["svn", "info", svn_path],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    revision = [line.split(":")[1].strip() for line in out.split("\n")
                if "Revision" in line]
    return int(revision[0])


def svn_dump_update(revision, remote_svn_server, local_svn_dump, update_file):
    """
    Summary line.

    Extended description of function.

    """
    # Get svn dump updates, from (revision + 1) till HEAD
    rev = "-r" + str(revision + 1) + ":HEAD"
    print("revision + 1: ", rev)
    f = open(update_file, 'w')
    proc = subprocess.Popen(['svnrdump', 'dump', remote_svn_server,
                            rev, '--incremental'], stdout=f,
                            stderr=subprocess.PIPE)
    ret_code = proc.wait()
    # Write dump update to file
    f.flush()
    f.close()
    print("Finshed dump to local file")
    return ret_code


# TODO: This doesn't work like expected
def update_local_svn_dump(local_svn_dump_location, update_file):
    """
    Summary line.
    """
    # Update svn dump
    # BUG HERE
    proc = subprocess.Popen(['svnadmin', 'load', local_svn_dump_location,
                             '<', update_file])
    out, err = proc.communicate()
    print("Finished dump update")
    return out


def _branch_exists(branch, working_directory):
    output = subprocess.check_output(['git', 'branch', '--list',
                                      branch], cwd=working_directory)
    return output != ''


def add_release_branches(local_svn_dump, git_repo):
    """Add release branches to each package.

    TODO Extended description of how this works.
    local_svn_dump = file:///home/nturaga/bioconductor-svn-mirror/

    remote_svn_server: 'https://hedgehog.fhcrc.org/bioconductor/'
    git_repo: '/home/nturaga/packages_local'
    """
    branch_url = os.path.join(local_svn_dump, "branches")
    # Get list of branches
    branch_list = [item.replace('/', '')
                   for item in
                   subprocess.check_output(['svn', 'list', branch_url]).split()
				   if "RELEASE" in item ]
    print("Branch list: ", branch_list)
    for branch in branch_list:
        # Special case to avoid badly named branches in SVN
        package_list_url = os.path.join(branch_url, branch, 'madman', 'Rpacks')
        # Get list of packages for EACH branch
        #package_list = subprocess.check_output(['svn', 'list', package_list_url]).split()
        package_list = _get_pack_list(package_list_url)
        import pdb; pdb.set_trace()
        for package in package_list:
            print("Package: ", package)
            bioc_git_package = os.path.join(git_repo, package)
            if package in os.listdir(git_repo):
                try:
                    pdb.set_trace()
                    print bioc_git_package
                    if not _branch_exists(branch, bioc_git_package):
			subprocess.check_call(['git', 'branch', branch], cwd=bioc_git_package)
                        print("Added branch {1} to package {2}".format(branch, bioc_git_package))
                except OSError as e:
                    print("Error: Package does not exist in repository, ",e)
                    pass
                except subprocess.CalledProcessError as e:
                    print("Branch: ", branch, "Package: ", package, "Error: ", e.output)
            else:
                print("Package ", package, "not in directory")
    return "Finished adding release branches"



def _svn_revision_branch_id(svn_url):
    """
    SVN stop on copy.
    """
    output = subprocess.check_output(['svn', 'log', '--stop-on-copy',
                                      '--verbose', svn_url])
    # parse output
    revision_id = re.findall('\(from [^:]+:([0-9]+)', output)[-1]
    return revision_id


def find_branch_points(from_revision, branch, package_dir):
    cmd1 = ['git', 'log', '--format=%H', branch]
    branch_root = subprocess.check_output(cmd1, cwd=package_dir).split()[-1]
    print("Branch root", branch_root)
    # Be careful, as there is an empty string at end of list
    commits = subprocess.check_output(['git', 'svn', 'log', '--oneline','--show-commit', 'master'],cwd=package_dir).split("\n")

    commits = [item for item in commits if len(item) != 0]

    for commit in commits:
        commit_info = commit.split(" | ")
        revision = commit_info[0].strip()
        sha1 = subprocess.check_output(['git', 'log', '-n', '1','--format=%H', commit_info[1].strip()],cwd=package_dir)
        if (int(revision[1:]) < int(from_revision[branch])):
            branch_point = (branch_root, sha1)
            return branch_point
    # TODO: make more meaningful message
    return None


def add_commit_history(local_svn_dump):
    """
    Add commit history.
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
        pdb.set_trace()
        packs = _get_pack_list(os.path.join(branch_url, branch, 'madman','Rpacks'))
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
                    subprocess.check_call(['git', 'filter-branch', '--', graft_range],cwd=cwd)
            except OSError as e:
                print("Package not found", package)
                print(e)
                pass
    return




def main():
    """Update SVN local dump and run gitify-bioconductor.

    Step 0: Create dump
    `svnadmin create bioconductor-svn-mirror`
    `svnrdump dump https://hedgehog.fhcrc.org/bioconductor |
                svnadmin load bioconductor-svn-mirror`

    This function runs the steps in order needed.
    Step 1: Define variables, and paths for SVN dump, remote_svn_repo,
            'git package local repo'.
    Step 2: Update SVN local dump
    Step 3: Add git remote path.
    Step 4: Add release branches to each package in 'git package local repo'
    """

    # Step 1
    local_svn_dump = 'file:///home/nturaga/bioconductor-svn-mirror/'
    local_svn_dump_location = "bioconductor-svn-mirror/"
    remote_svn_server = 'https://hedgehog.fhcrc.org/bioconductor'


    # Initial set up
    packs = _get_pack_list(local_svn_dump)
    # Create a local dump of SVN packages
    # svn_dump(packs)

    # Step 2
    revision = svn_get_revision(local_svn_dump)
    print revision
    update_file = "updt.svn"
#    svn_dump_update(revision, remote_svn_server, local_svn_dump, update_file)
    # TODO: BUG here
#    update_local_svn_dump(local_svn_dump_location, update_file)
    # Step 3: Add git remote branch, to make git package act as a server

    # Step 4: Add release branches to all   packages
    # Step 5:
    git_repo = "/home/nturaga/packages"
#    add_release_branches(local_svn_dump, git_repo)
    add_commit_history(local_svn_dump)

    return


if __name__ == '__main__':
    main()
