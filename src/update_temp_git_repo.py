import os
import subprocess
import logging
from src.git_api.git_api import git_svn_rebase
from src.git_api.git_api import git_checkout
from src.git_api.git_api import git_svn_fetch
from src.git_api.git_api import git_reset
from local_svn_dump import Singleton


class UpdateGitRepository(object):
    """This class is used to update the packages inside temp_git_repo.

    This allows for updating only the master and most recent release
    to speed up the transition process.
    """
    __metaclass__ = Singleton

    def __init__(self, temp_git_repo, branch_list):
        self.temp_git_repo = temp_git_repo
        self. branch_list = branch_list

    def most_recent_release(self):
        """Get most recent release other than master."""
        return self.branch_list[-1]

    def most_recent_commit(self, cwd):
        """Get most recent commit in git repository."""
        x = subprocess.check_output(['git', 'log', '--format=%H', '-n', '1'],
                                    cwd=cwd)
        return x.strip()

    def update_temp_git_repo(self):
        """Create bare repos in the repository directory.

        This needs to be run from within the temp_git_repo directory.
        NOTE: Set `umask` environment variable to 0027 before making
            bare repositories for git.
        """
        for package in os.listdir(self.temp_git_repo):
            try:
                package_dir = os.path.join(self.temp_git_repo, package)
                # Rebase assumes that the branch is "master"
                git_svn_rebase(cwd=package_dir)
                recent_release = self.most_recent_release()
                # Fetch release updates
                git_svn_fetch(recent_release, cwd=package_dir)
                # Checkout release updates
                git_checkout(recent_release, cwd=package_dir)
                # Merge release updates WITHOUT edits to commit message
                subprocess.check_call['git', 'merge', '--no-edit'
                                      'git-svn-' + recent_release]
                merge_commit = self.most_recent_commit(cwd=package_dir)
                git_reset(merge_commit, cwd=package_dir)
                git_checkout('master', cwd=package_dir)
            except subprocess.CalledProcessError as e:
                logging.error("Error updating package: %s in release %s"
                              % (package, recent_release))
                logging.error(e)
                pass
            except OSError as e:
                logging.error("Error: %s, Package: %s" % (e, package))
                pass
        return
