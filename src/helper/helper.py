import subprocess
import os
import logging

def is_github_repo(url):
    """Check if it is a valid github repo.

    Returns True, or False.
    """
    cmd = ['git', 'ls-remote', url]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    out, err = proc.communicate()

    if err:
        print("This is not a valid github URL: \n %s" % err)
        return False
    print("Out: %s" % out)
    return True


def get_branch_list(svn_root):
    """Get list of branches.

    Input:
        svn_root path.
    Return:
        List of branches in the reverse order of releases, i.e,
        latest first.
    """
    branch_url = os.path.join(svn_root, "branches")
    branch_list = [item.replace('/', '')
                   for item in
                   subprocess.check_output(['svn', 'list', branch_url]).split()
                   if "RELEASE" in item]
    return branch_list


def setup_logger(logger_name, log_file):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(levelname)s : %(asctime)s : %(message)s')
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    l.setLevel(logging.DEBUG)
    l.addHandler(fileHandler)
    l.addHandler(streamHandler)

