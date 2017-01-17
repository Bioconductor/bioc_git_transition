#!/usr/bin/env python
###############################################################################
# By Nitesh Turaga
# Created: 2017 Jan 7th
# Last Modified: 2017 Jan 12th
# Title:clone.py
# Purpose: Git mirror from svn revision
###############################################################################

import os
import subprocess
from mirror import branch_exists

def svn_dump(packs):
	svn_local_dump ='file:///home/nturaga/bioconductor-svn-mirror/trunk/madman/Rpacks/'
	for pack in packs:
		cmd = 'git svn clone ' + svn_local_dump + pack
		os.system(cmd)
		print("Finished git svn clone from local dump for package: ",pack)
	return

def git_add_remote(path):
	remote_path = 'nturaga@git.bioconductor.org:/home/nturaga/packages_local/'
	for pack in os.listdir(path):
		if (os.path.isdir(pack) and (".git" in os.listdir(os.path.abspath(pack)))):
			remote = remote_path + pack
			remote_add_cmd = ['git', 'remote','add','origin',remote]
			# Run remote command
			p = subprocess.Popen(remote_add_cmd, cwd=os.path.abspath(pack))
    		print("Added remote to " , os.path.abspath(pack))

def svn_get_revision(svn_path):
	# Get revision number
	p = subprocess.Popen(["svn","info",svn_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	out, err = p.communicate()
	revision = [line.split(":")[1].strip() for line in out.split("\n") if "Revision" in line]
	return int(revision[0])

def svn_dump_update(revision, remote_svn_server, local_svn_dump, update_file):
	# Get svn dump updates, from (revision + 1) till HEAD
	rev = "-r" + str(revision+1) + ":HEAD"
	print("revision + 1: " , rev)
	f = open(update_file,'w')
	proc = subprocess.Popen(['svnrdump', 'dump', remote_svn_server, rev, '--incremental'],
						  stdout=f,
						  stderr=subprocess.PIPE)
	ret_code = proc.wait()
	# Write dump update to file
	f.flush()
	f.close()
	print("Finshed dump to local file")
	return ret_code


# TODO: This doesn't work like expected
def update_local_svn_dump(local_svn_dump_location, update_file):
	# Update svn dump
    # BUG HERE
  	proc = subprocess.Popen(['svnadmin', 'load', local_svn_dump_location, '<', update_file])
	out, err = proc.communicate()
	print("Finished dump update")
    return out


def _branch_exists(branch,working_directory):
    output = subprocess.check_output(['git', 'branch', '--list', branch],
             cwd=working_directory)
    return output != ''


def add_release_branches(remote_svn_server, git_repo):
    """Add release branches to each package.

    remote_svn_server: 'https://hedgehog.fhcrc.org/bioconductor/'
    git_repo: '/home/nturaga/packages_local'
    """
	branch_url = os.path.join(remote_svn_server, "branches")
    # Get list of branches
    branch_list = [item.replace("/","")
                    for item in subprocess.check_output(['svn', 'list', branch_url]).split()]
    for branch in branch_list:
        # Special case to avoid badly named branches in SVN
        if ("RELEASE" in branch) and ("_branch" not in branch):
            package_list_url = os.path.join(branch_url,branch, 'madman','Rpacks')
            # Get list of packages for EACH branch
            package_list = subprocess.check_output(['svn','list', package_list_url]).split()
            for package in package_list:
                try:
                    bioc_git_package = os.path.join(git_repo, package)
                    if branch_exists(branch_name, bioc_git_package):
                        # Add new branch in bioconductor package location
                        subprocess.check_call(['git','branch',branch_name], cwd=bioc_git_package)
                except subprocess.CalledProcessError as e:
                    print(e.output)
    return


def add_commit_history():
    """
    Add commit history.
    """
    return


def main():
    """Update SVN local dump and run gitify-bioconductor.

    This function runs the steps in order needed.
    Step 1: Define variables, and paths for SVN dump, remote_svn_repo,
            'git package local repo'.
    Step 2: Update SVN local dump
    Step 3: Add git remote path.
    Step 4: Add release branches to each package in 'git package local repo'
    """
    # TODO: Need to dynamically get list of packages
    with open('list_rpacks.txt') as f:
        packs = f.readlines()

    # Step 1
	local_svn_dump = 'file:///home/nturaga/bioconductor-svn-mirror/'
	local_svn_dump_loc = "bioconductor-svn-mirror/"
	remote_svn_server = 'https://hedgehog.fhcrc.org/bioconductor'

    # Step 2
    revision = svn_get_revision(local_svn_dump)
	print revision
	update_file = "updt.svn"
    svn_dump_update(revision, remote_svn_server, local_svn_dump, update_file)
    # TODO: BUG here
	update_local_svn_dump(local_svn_dump_loc, update_file)
    # Step 3: Add git remote branch, to make git package act as a server
    # Step 4: Add release branches to all packages
    # Step 5:

    return


if __name__ == '__main__':
    main()
