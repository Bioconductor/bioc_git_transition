import os
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


def append_development_url(package):
    """Extract `DevelopmentURL` from DESCRIPTION file."""
    description_file = os.path.join(package, 'DESCRIPTION')
    with open(description_file, 'r') as f:
        doc = f.read()
    doc_list = doc.split("\n")
    for i in xrange(len(doc_list)):
        if doc_list[i].startswith("URL:"):
            url = doc_list[i]
    url = url.replace("URL: ", "")
    print(url)
    if ("github" in url) and is_github_repo(url):
        # parse to see if valid github URL
        # Add url as Development URL
        development_url = "DevelopmentURL: " + url
        with open(description_file, "a") as f:
            f.write(development_url)
    else:
        print("This is not a valid URL")
    return


def append_development_url_in_all(edit_repo, push=False):
    """
    Append DevelopmentURL in all packages.

    If there is a github URL in the DESCRIPTION file,
    check if its valid, and append it as a new item,
    DevelopmentURL. Do this in all packages in the github
    edit repo, and push back to git server if `push=True`
    """
    for package in os.listdir(os.path.abspath(edit_repo)):
        append_development_url(package)
        # if push=True:
        #     git_push(package, branch)
    return
