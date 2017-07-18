import subprocess
from src.helper.helper import get_branch_list


def release_to_manifest(release):
    manifest_file = ('bioc_' +
                     release.replace("RELEASE_", "").replace("_", ".") +
                     '.manifest')
    return manifest_file


def manifest_package_list(release, svn_root, package_path):
    """Get the package list from Bioconductor manifest file."""
    no_manifest_list = ['RELEASE_1_0',
                        'RELEASE_1_0_branch',
                        'RELEASE_1_4',
                        'RELEASE_1_4_branch',
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
