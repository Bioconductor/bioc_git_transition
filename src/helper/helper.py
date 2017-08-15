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


def release_to_manifest(release):
    no_manifest_list = ['RELEASE_1_0', 'RELEASE_1_0_branch',
                        'RELEASE_1_4', 'RELEASE_1_4_branch',
                        'RELEASE_1_5']
    if release in no_manifest_list:
        return
    manifest_file = ('bioc_' +
                     release.replace("RELEASE_", "").replace("_", ".") +
                     '.manifest')
    return manifest_file


def manifest_package_list(release, svn_root, package_path):
    """Get the package list from Bioconductor manifest file."""
    no_manifest_list = ['RELEASE_1_0', 'RELEASE_1_0_branch',
                        'RELEASE_1_4', 'RELEASE_1_4_branch',
                        'RELEASE_1_5']
    # Return empty if there is not release
    if release in no_manifest_list:
        return
    manifest = (svn_root + "/" + "branches" + "/" + release +
                package_path + "/" +
                release_to_manifest(release))

    cmd = ['svn', 'cat', manifest]
    out = subprocess.check_output(cmd)
    doc = out.split("\n")
    package_list = [line.replace("Package: ", "").strip()
                    for line in doc if line.startswith("Package")]
    return package_list


def populate_manifest_dictionary(svn_root, package_path):
    """Populate dictionary with manifest package list."""
    manifest_dictionary = {}
    branch_list = get_branch_list(svn_root)
    for release in branch_list:
        package_list = manifest_package_list(release, svn_root,
                                             package_path)
        manifest_dictionary[release] = package_list
    return manifest_dictionary


def get_union(svn_root, package_path, manifest_dictionary):
    """Get a union of RELEASE_3_5 and RELEASE_3_6 manifest_files."""
    # Get package list from RELEASE_3_5
    release_3_5 = manifest_dictionary["RELEASE_3_5"]
    # Get package list for RELEASE_3_6
    manifest = (svn_root + "/" + "trunk" + package_path + "/"
                + release_to_manifest("RELEASE_3_6"))
    cmd = ['svn', 'cat', manifest]
    out = subprocess.check_output(cmd)
    doc = out.split("\n")
    release_3_6 = [line.replace("Package: ", "").strip()
                   for line in doc if line.startswith("Package")]
    return list(set(release_3_5 + release_3_6))


def union_of_data_manifest():
    svn_root = "file:///home/git/bioc-data.hedgehog.fhcrc.org/"
    release_3_5 = (svn_root + "branches/" +
                   "RELEASE_3_5/experiment/pkgs/" +
                   "bioc-data-experiment.3.5.manifest")
    trunk = (svn_root +
             "trunk/experiment/pkgs/" +
             "bioc-data-experiment.3.6.manifest")

    def get_list(manifest):
        cmd = ['svn', 'cat', manifest]
        out = subprocess.check_output(cmd)
        out = out.replace("## Blank lines between all entries\nPackage:", "")
        package_list = [item.strip() for item in out.split("\nPackage:")]
        return package_list
    release_3_6 = get_list(trunk)
    release_3_5 = get_list(release_3_5)
    return list(set(release_3_6 + release_3_5))


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
