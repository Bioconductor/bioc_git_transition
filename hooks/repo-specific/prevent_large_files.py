import subprocess
import sys
# Global variables used by pre-recieve hook

ZERO_COMMIT = "0000000000000000000000000000000000000000"
MAXSIZE = int(5000000)  # 5MB limit on file size
ERROR_MSG = """Error: file larger than %.0f Mb.

    File name: '%s'
    File size: %.1f Mb

Please see Biocondcutor guidelines
https://bioconductor.org/developers/package-guidelines/
"""

def prevent_large_files(oldrev, newrev, refname):
    """Pre-receive hook to check for large files."""

    # set oldrev properly if this is branch creation
    if oldrev == ZERO_COMMIT:
        if refname == "refs/heads/master":
            oldrev = subprocess.check_output(["git", "rev-list",
                                              "--max-parents=0",
                                              newrev]).strip()
        else:
            oldrev = "HEAD"

    list_files = subprocess.check_output(["git", "diff",
                                          "--name-only", "--diff-filter=ACMRT",
                                          oldrev + ".." + newrev])
    for fl in list_files.splitlines():

        size = subprocess.check_output(["git", "cat-file", "-s",
                                        newrev + ":" + fl])
        #  Check to see if for some reason we didn't get a size
        size = int(size.strip())
        if size:
            # Compare filesize to MAXSIZE
            mb = 1024.0 * 1024.0
            if size > MAXSIZE:
                print(ERROR_MSG  % (MAXSIZE / mb, fl, size / mb) )
                sys.exit(1)
    return
