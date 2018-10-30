"""
Usage:

    python detect_bad_version.py <directory with all packages> <even|odd>

    Passing 'even' as the second argument results in a success if the
    version is even. Packages with odd versions will be output.
"""

import os
import sys


def find_description(directory):
    description_files = []
    # Walk directories only; skip those without DESCRIPTION files
    for f in os.walk(directory).next()[1]:
        dfile = os.path.join(directory, f, "DESCRIPTION")
        if os.path.exists(dfile):
            description_files.append(dfile)
    return description_files


def check_version(version, parity):
    version_number = version.replace("Version :","").split(".")
    y = int(version_number[1]) 
    ## Add rules here
    if parity == "odd":
        if y % 2 == 0:
            return False
    elif parity == "even":
        if y % 2 != 0:
            return False

    if y > 99:
        return False
    else: 
        return True 


def read_description(DESCRIPTION_path):
    with open(DESCRIPTION_path) as f:
        txt = f.read()
    lines = txt.splitlines()
    version = [line for line in lines if line.startswith("Version")][0]
    package_name = DESCRIPTION_path.replace("/DESCRIPTION","").replace("packages/","")
    return (package_name, version)


def run(directory, parity):
    descriptions = find_description(directory)
    for description in descriptions: 
        package_name, version = read_description(description)
        if not check_version(version, parity):
            print(package_name, version)
    return


if __name__ == "__main__":
    print("Directory passed: ", sys.argv[1], sys.argv[2])
    run(str(sys.argv[1]), str(sys.argv[2]))
