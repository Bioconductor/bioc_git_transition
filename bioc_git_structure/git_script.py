from git import Repo
import os


def git_init_recursively(path):
    """Create git repository in all packages."""
    # print path to all subdirectories first.
    for package in os.listdir(path):
        if os.path.isdir(os.path.join(path,package)):
            pack_path = os.path.abspath(package)
            # Create git repository
            r = git.Repo.init(pack_path)
            # Create all bioconductor branches
            create_branches(path_path)
    return

def create_branches(git_repository):
    """ Create branches for all release versions in bioconductor."""
    assert not repo.bare  # Make sure that its a bare repo
    # Create a DEVEL branch
    git_repository.create_head("devel")

    # List of RELEASE branch names
    branch_names = ['1.5', '1.6', '1.7', '1.8', '1.9',
                    '2.0', '2.1', '2.2', '2.3', '2.4',
                    '2.5', '2.6', '2.7', '2.8', '2.9',
                    '2.10', '2.11', '2.12', '2.13', '2.14',
                    '3.0', '3.1', '3.2', '3.3', '3.4', '3.5']
    # Create RELEASE BRANCHES
    for version in branch_names:
        branch_name = "release" + "_" + version
        print("Creating a new branch for {0} in repo: {1}".format(branch_name,
              git_repository))
        # Create a new branch
        new_branch = git_repository.create_head(branch_name)
        print("New Branch: ", new_branch)
    return


def delete_all_branches(git_repository):
    """Delete all branches in repo."""
    for branch in git_repository.branches:
        if branch.name == "master":
            pass
        else:
            print branch.name
            branch.delete(git_repository, branch.name)
    return

if __name__ == '__main__':

    working_tree_dir = "/Users/niteshturaga/Documents/bioc_packs/"
    repo = Repo(working_tree_dir)
    # Assert repo not empty
    assert not repo.bare
    create_branches(repo)
