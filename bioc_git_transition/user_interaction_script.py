#!/usr/bin/env python

"""Bioconductor Git user interaction script docstrings.

This module provides functions for working with the Bioconductor
`git` repository. This module gives the bioconductor core team,
to interact with the GIT server, and work with package authors.

Author: Nitesh Turaga
"""
import os
import subprocess
from clone_new_package import clone
from git_script import git_remote_add
import logging as log


# TODO: Edit destination dir
edit_repo = "/home/nturaga/clones"
SERVER = 'ubuntu@git.bioconductor.org:'


def git_checkout(branch, cwd, new=False):
    """Git checkout branch.

    new=False, this option specifies if branch is already created or not.
    """
    if new:
        cmd = ['git', 'checkout', '-b', branch]
    else:
        cmd = ['git', 'checkout', branch]
    subprocess.check_call(cmd, cwd=cwd)
    return


def extract_developmentURL(package):
    """Extract DevelopmentURL from DESCRIPTION file."""
    description = os.path.join(package, 'DESCRIPTION')
    with open(description, 'r') as f:
        doc = f.read()
    doc_list = doc.split("\n")
    for i in xrange(len(doc_list)):
        if doc_list[i].startswith("DevelopmentURL:"):
            url = doc_list[i]
    url = url.replace("DevelopmentURL:", "")
    url = url.strip()
    return url


# TODO: Edit the package url as the remote repo changes
def edit_repo(repo_dir, edit_repo, package):
    """
    Clone a package from repo_dir to make changes.

    Use this function to set up a clone of an existing bioconductor-git
    package, to make changes and push back to the git-server.
    """
    log.info("Set up a clone of package: %s, to push changes to repo_dir")
    package_url = SERVER + repo_dir + "/" + package
    clone(edit_repo, package_url, bare=False)
    developmentURL = extract_developmentURL(os.path.join(edit_repo, package))
    git_remote_add('upstream', developmentURL,
                   cwd=os.path.join(edit_repo, package))
    return


# 1385  git remote add upstream https://github.com/Bioconductor/spbtest3.git
# 1386  git remote -v
# 1387  git pull -Xtheirs --no-edit upstream master

def clone_all_edit_repo(repo_dir):
    """Clone all packages in git server to a location,
        where contents may be edited.
    """
    for package in os.listdir(repo_dir):
        edit_repo(repo_dir, package)
    return


def daily_fetch_branch(edit_repo, package, branch):
    """Daily fetch from github repo.

    ## git checkout branch-1
    ## git pull upstream branch-1:branch-1
    ## git push origin branch-1
    """
    path = os.path.join(edit_repo, package)
    git_checkout(branch, cwd=path, new=False)
    # Git pull into a branch of the edit_repp
    cmd = ['git', 'pull', '-Xtheirs', '--no-edit', 'upstream',
           branch + ":" + branch]
    p = subprocess.Popen(cmd, cwd=path, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    if ("CONFLICT" in out):
        log.error("Merge conflict in the package: %s" % package)
        log.error(out)
    else:  # Git push
        cmd = ['git', 'push', 'origin', branch]
        subprocess.check_call(cmd, cwd=path)
    return


def daily_fetch(edit_repo, branch):
    """Daily fetch  needs to be run by the build system on
        the branch being updated e.g `master` or `RELEASE_3_4`
    """
    for package in os.listdir(edit_repo):
        daily_fetch_branch(edit_repo, package, branch)
    return


def version_bump(edit_repo, package, release=False):
    """Bump package version.

    release=False, assumes that version bump is not for a new
                   release branch.
    """
    description_file = os.path.join(edit_repo, package, 'DESCRIPTION')
    with open(description_file, 'r') as f:
        doc = f.read()
    doc_list = doc.split("\n")
    for i in xrange(len(doc_list)):
        if doc_list[i].startswith("Version:"):
            version = doc_list[i]
            index = i
    x, y, z = version.split("Version: ")[1].split(".")
    if release:
        # Special case
        if int(y) == 99:
            x = int(x) + 1
            y = 0
        else:
            y = int(y) + 1
        z = 0
    else:
        z = int(z) + 1
    version = str(x) + "." + str(y) + "." + str(z)
    doc_list[index] = "Version: " + version
    with open(description_file, "w") as f:
        f.write("\n".join(doc_list))
    log.info("Package: %s updated version to: %s" % (package, version))
    return


def commit_message(msg, package):
    """Add a commit message to package during, bioc release."""
    cmd = ['git', 'commit', '-m', msg]
    subprocess.check_call(cmd, cwd=package)
    return


def release_branch(edit_repo, package, new_release):
    """Create new release branch, make git call."""
    package_dir = os.path.join(edit_repo, package)
    # checkout master
    git_checkout(branch="master", cwd=package_dir, new=False)
    # on master, version bump, release = False
    version_bump(package, release=False)
    commit_message("bump x.y.z versions to even 'y' prior to creation of "
                   + new_release, package_dir)

    # IN THE BRANCH, version bump release=True
    git_checkout(branch=new_release, cwd=package_dir, new=True)
    version_bump(package, release=True)
    # commit messsage in branch
    commit_message(msg="Creating branch for BioC " + new_release,
                   package=package_dir)

    # checkout master
    git_checkout(branch="master", cwd=package_dir, new=False)
    # version bump release=True
    version_bump(package, release=True)
    # Commit message
    commit_message("bump x.y.z versions to odd 'y' after creation of "
                   + new_release, package_dir)
    log.info("New branch created for package %s" % package)
    return


def create_new_release_branch(new_release, edit_repo):
    """Create a new RELEASE from master.

    This function is used to create a new release version,
    from the 'master' branch going forward.
    Usage: create_new_release_branch('RELEASE_3_7', '/packages/')
    """
    for package in os.listdir(os.path.abspath(edit_repo)):
        # Create a new release branch
        release_branch(new_release, package)
        # TODO: Push new release branch
        cmd = ['git', 'push', '-u', 'origin', new_release]
        subprocess.check_call(cmd, cwd=os.path.join(edit_repo, package))
    return
