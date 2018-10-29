"""
Usage:

    python detect_bad_version.py <directory with all packages>

"""

import os
import sys


def find_description(directory):
    description_files = []
    for f in os.listdir(directory):
        description_files.append(os.path.join(directory, f, "DESCRIPTION"))
    return description_files


def check_version(version):
    version_number = version.replace("Version :","").split(".")
    y = int(version_number[1])    
    correct = True
    ## Add rules here
    if y % 2 == 0:
        correct = False
    if y > 99:
        correct = False
    return correct


def read_description(DESCRIPTION_path):
    with open(DESCRIPTION_path) as f:
        txt = f.read()
    lines = txt.splitlines()
    version = [line for line in lines if line.startswith("Version")][0]
    package_name = DESCRIPTION_path.replace("/DESCRIPTION","").replace("packages/","")
    return (package_name, version)


def run(directory):
    descriptions = find_description(directory)
    for description in descriptions:    
        package_name, version = read_description(description)
        if not check_version(version):
            print(package_name, version)
    return


if __name__ == "__main__":
    print("Directory passed: ", sys.argv[1])
    run(str(sys.argv[1]))
