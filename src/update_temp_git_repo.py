import os
import subprocess
import logging
from src.git_api.git_api import git_clone


def update_temp_git_repo(self):
    """Create bare repos in the repository directory.

    This needs to be run from within the temp_git_repo directory.
    NOTE: Set `umask` environment variable to 0027 before making
        bare repositories for git.
    """
    for package in os.listdir(os.path.abspath(self.temp_git_repo)):
        try:
            git_clone(os.path.join(self.temp_git_repo, package),
                      self.bare_git_repo, bare=True)
            # Git update server, so that info/refs is populated,
            # making the server "smart"
            cmd = ['git', 'update-server-info']
            subprocess.check_call(cmd,
                                  cwd=os.path.join(self.bare_git_repo,
                                                   package + ".git"))
        except subprocess.CalledProcessError as e:
            logging.error("Error creating bare repo: %s in package %s"
                      % (e, package))
            pass
        except OSError as e:
            logging.error("Error: %s, Package: %s" % (e, package))
            pass
    return

# cp -r /home/git/temp_packages/DelayedArray/ /tmp/.
# cd DelayedArray/
# git svn rebase
# git svn fetch RELEASE_3_5
# git checkout RELEASE_3_5
# git merge git-svn-RELEASE_3_5
# x = git log --format=%H | head -n 1
# git revert x
# git checkout master
