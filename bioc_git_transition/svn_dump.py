#!/usr/bin/env python

"""Bioconductor make SVN dump and update.

This module provides functions to create an SVN dump and
update the SVN dump before making the git transition.

Author: Nitesh Turaga

Usage:
    `python svn_dump.py`
"""
import os
import subprocess
import logging as log


# TODO: THERE IS A BUG HERE
def get_pack_list(path):
    """Get list of packages on SVN."""
    # if 'trunk/madman/Rpacks' not in path:
    # path = os.path.join(path, 'trunk/madman/Rpacks/')
    result = subprocess.check_output(['svn', 'list', path])
    return [item.replace('/', '') for item in result.split()]


def manifest_package_list(svn_root, manifest_file):
    """Get the package list from Bioconductor manifest file."""
    manifest = os.path.join(svn_root, "trunk", "madman", "Rpacks",
                            manifest_file)
    cmd = ['svn', 'cat', manifest]
    out = subprocess.check_output(cmd)
    # with open(manifest, 'r') as f:
    doc = out.split("\n")
    package_list = [line.replace("Package: ", "").strip()
                    for line in doc if line.startswith("Package")]
    return package_list


def svn_dump(svn_root, packs, svn_root_dir):
    """
    Create git svn clone from SVN dump for each package.

    The SVN dump needs to be updated daily/nightly for the rest to
    work as planned.

    Parameters
    ----------
    svn_root : List of Bioconductor packages
        List of Bioconductor packages obtained
        from _get_pack_list(svn_root)

    Returns
    -------
    None
    """
    package_dir = os.path.join(svn_root, 'trunk/madman/Rpacks/')
    for pack in packs:
        package_dump = os.path.join(package_dir, pack)
        cmd = ['git', 'svn', 'clone', '--authors-file=user_db.txt',
               package_dump]
        subprocess.check_call(cmd, cwd=svn_root_dir)
        # TODO: git svn clone
        # --rewrite-root=https://hedgehog.fhcrc.org/bioconductor/trunk/madman/Rpacks/BiocInstaller
        # --authors-file=users_and_user_db.txt file:///home/nturaga/bioconductor-svn-mirror/trunk/madman/Rpacks/BiocInstaller
        log.debug("Finished git-svn clone for package: %s" % pack)
    return


def svn_get_revision(svn_root):
    """
    Summary line.

    # TODO: remove hardcoded packs and update to svn list from hedgehog

    """
    # Get revision number
    p = subprocess.Popen(["svn", "info", svn_root],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    revision = [line.split(":")[1].strip() for line in out.split("\n")
                if "Revision" in line]
    return int(revision[0])


def svn_dump_update(revision, remote_svn_server, update_file):
    """
    Summary line.

    Extended description of function.

    """
    # Get svn dump updates, from (revision + 1) till HEAD
    rev = "-r" + str(revision + 1) + ":HEAD"
    f = open(update_file, 'w')
    proc = subprocess.Popen(['svnrdump', 'dump', remote_svn_server,
                            rev, '--incremental'], stdout=f,
                            stderr=subprocess.PIPE)
    ret_code = proc.wait()
    # Write dump update to file
    f.flush()
    f.close()
    log.debug("Finshed dump to local file: %s" % update_file)
    return ret_code


# TODO: This doesn't work like expected
def update_local_svn_dump(svn_root_dir, update_file):
    """Update Local SVN dump."""
    cmd = ('svnadmin load ' + svn_root_dir + ' < '
                            + os.path.abspath(update_file))
    subprocess.call(cmd, shell=True)
    log.debug("Finished dump update")
    return
