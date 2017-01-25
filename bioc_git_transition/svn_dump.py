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


def get_pack_list(local_svn_dump):
    """Get list of packages on SVN."""
    package_dir = os.path.join(local_svn_dump, 'trunk/madman/Rpacks/')
    result = subprocess.check_output(['svn', 'list', package_dir])
    return [item.replace('/', '') for item in result.split()]


def svn_dump(local_svn_dump, packs, dump_location):
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
        subprocess.check_call(['git', 'svn', 'clone', package_dump],
                              cwd=dump_location)
        print("Finished git svn clone from local dump for package: ", pack)
    return


def svn_get_revision(local_svn_dump):
    """
    Summary line.

    # TODO: remove hardcoded packs and update to svn list from hedgehog

    """
    # Get revision number
    p = subprocess.Popen(["svn", "info", local_svn_dump],
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
    """Update Local SVN dump."""
    cmd = 'svnadmin load ' + local_svn_dump_location + ' < ' + os.path.abspath(update_file)
    subprocess.call(cmd, shell=True)
    print("Finished dump update")
    return
