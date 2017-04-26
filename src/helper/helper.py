import subprocess

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
