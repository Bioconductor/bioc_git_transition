"""Bioconductor update SVN dump code.

Author: Nitesh Turaga

Usage:
    `python svn_dump_update.py`
"""

from src.local_svn_dump import LocalSvnDump
import logging as log
import ConfigParser
log.basicConfig(filename='svn_dump_update.log',
                format='%(asctime)s %(message)s',
                level=log.DEBUG)
log.debug("Bioconductor SVN Dump Log File: \n")


def svn_root_update(configfile):
    """Dump update needs to be run as git."""
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)

    bioc_git_repo = Config.get('GitBioconductor', 'bioc_git_repo')
    svn_root = Config.get('SVN', 'svn_root')
    remote_svn_server = Config.get('SVN', 'remote_svn_server')
    users_db = Config.get('SVN', 'users_db')
    update_file = Config.get('SVN', 'update_file')

    for s in Config.sections():
        for k, v in Config.items(s):
            log.info("%s: %s" % (k, v))

    dump = LocalSvnDump(svn_root, bioc_git_repo, users_db, remote_svn_server)
    dump.svn_get_revision()
    dump.svn_dump_update(update_file)
    dump.update_local_svn_dump(update_file)
    return


def svn_bioc_data_update(configfile):
    """Annotation data dump update."""
    Config = ConfigParser.ConfigParser()
    Config.read(configfile)

    bioc_data_git_repo = Config.get('Annotation', 'bioc_data_git_repo')
    svn_annotation_root = Config.get('Annotation', 'svn_annotation_root')
    remote_svn_data_server = Config.get('Annotation', 'remote_svn_data_server')
    data_users_db = Config.get('Annotation', 'data_users_db')
    update_file_data = Config.get('Annotation', 'updata_file_data')

    dump = LocalSvnDump(svn_annotation_root, bioc_data_git_repo,
                        data_users_db, remote_svn_data_server)
    dump.svn_get_revision()
    dump.svn_dump_update(update_file_data)
    dump.update_local_svn_dump(update_file_data)
    return


if __name__ == '__main__':
    svn_root_update("./settings.ini")
