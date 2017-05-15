# Scenario 4: Push updates to the release branch (RELEASE_X_Y)

**Goal:** A bug has been identified. A bug fix needs to be commited to the `RELEASE_X_Y` branch.

Developers have write access to the most recent release branch (currently, the `RELEASE_3_5` branch). Bug fixes (but not new features) should be commited to the current release, so that the bug fixes are made available to users.

**NOTE:** Best practice is to develop and test (including a full nightly build) the bug fix on the `master` branch, and to merge the bug fix from master to release. See [Scenario-10][].

**NOTE:** For developers who are used to the SVN way of development in _Bioconductor_, `devel` (svn) --> `master` (git).

## Steps:

1. Fetch and merge changes from the _Bioconductor_ and Github repositories following [Scenario 9][].

    ```
    git fetch --all
    git checkout RELEASE_3_5
    git merge upstream/RELEASE_3_5
    git merge origin/RELEASE_3_5
    ```

1. Make changes to source code as needed, and bump the version number in the DESCRIPTION file. Remember that release branch versions go from `x.y.z` to `x.y.z+1` (e.g., from `1.10.1` to `1.10.2`) where `y` is even in release.

1. Add and commit the files you made the changes to

    ```
    git add <file(s) that changed>
    git commit -m "My informative commit message"
    ```

1.  Push to both the _Bioconductor_ and GitHub repositories.

    ```
    git push origin RELEASE_3_5
    git push upstream RELEASE_3_5
    ```

[Scenario-10]: scenario-10-bug-fix-in-release-and-devel.md
