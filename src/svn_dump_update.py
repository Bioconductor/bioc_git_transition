"""Bioconductor update SVN dump code.

Author: Nitesh Turaga

Usage:
    `python svn_dump_update.py`
"""

from src.local_svn_dump import LocalSvnDump
import logging
import ConfigParser


def svn_root_update(configfile):
    """Dump update needs to be run as git."""
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)

    temp_git_repo = Config.get('Software', 'temp_git_repo')
    svn_root = Config.get('SVN', 'svn_root')
    remote_svn_server = Config.get('SVN', 'remote_svn_server')
    users_db = Config.get('SVN', 'users_db')
    update_file = Config.get('SVN', 'update_file')
    package_path = Config.get('Software', 'package_path')

    logging.debug("Bioconductor SVN Dump Log File: \n")

    dump = LocalSvnDump(svn_root, temp_git_repo,
                        users_db, remote_svn_server, package_path)
    dump.svn_get_revision()
    dump.svn_dump_update(update_file)
    dump.update_local_svn_dump(update_file)
    del dump
    return


def svn_experiment_root_update(configfile):
    """Dump update needs to be run as git."""
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)

    temp_git_repo = Config.get('ExperimentData', 'temp_git_repo')
    svn_root = Config.get('ExperimentData', 'svn_root')
    remote_svn_server = Config.get('ExperimentData', 'remote_svn_server')
    users_db = Config.get('SVN', 'users_db')
    update_file = Config.get('ExperimentData', 'update_file')
    package_path = Config.get('ExperimentData', 'package_path')

    logging.debug("Bioconductor SVN Dump Log File: \n")

    dump = LocalSvnDump(svn_root, temp_git_repo, users_db,
                        remote_svn_server, package_path)
    dump.svn_get_revision()
    dump.svn_dump_update(update_file)
    dump.update_local_svn_dump(update_file)
    del dump
    return
