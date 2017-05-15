# Scenario 4: Push updates to release branch (RELEASE_X_Y)

**Goal:** A bug has been identified. A bug fix needs to be commited to the `RELEASE_X_Y` branch.

Developers can push commits to the `master` branch. These commits will be usied in the latest development builds, and will eventually become the  _next_ release branch. Developers also have write access to the most recent release branch (currently, the `RELEASE_3_5` branch). Bug fixes (but not new features) should be commited to the current release, so that they are made available to users.

**NOTE:** Best practice is to develop and test (including a full nightly build) the bug fix on the `master` branch, and to merge the bug fix from master to release. See [Scenario-10][].

**NOTE:** For developers who are used to the SVN way of development in _Bioconductor_, `devel` (svn) --> `master` (git).

## Steps:

1. Pull any changes from GitHub or other `origin` repository

    ```
    git pull
    ```

1. Fetch any updates from the _Bioconductor_ `upstream` repository

   ```
   git fetch upstream
   ```

1. Checkout the release branch. If the branch was not previously available on your local machine, use:

    ```
    git checkout -b RELEASE_3_5 upstream/RELEASE_3_5
    ```

    If the branch was already available, use:

    ```
    git checkout RELEASE_3_5
    git merge upstream/RELEASE_3_5
    ```

1. Make appropriate changes as needed, and bump the version number in the DESCRIPTION file.

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
