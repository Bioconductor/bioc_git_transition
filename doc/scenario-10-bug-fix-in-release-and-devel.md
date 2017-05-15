# Scenario 10: Bug fix in `master` and  `release` branches

**Goal:** Maintainers will have to fix bugs from time to time, and make sure the patch is available both in the `master` branch (svn devel) and the current `release` branch.

## Steps:

1. Make sure to follow [Scenario-3][] to pull any potential changes in the code from the _Bioconductor_ core team. Do this for both the master and release branches.

    ```
    git fetch upstream
    git checkout <RELEASE_X_Y>
    git merge upstream/<RELEASE_X_Y>
    git checkout master
    git merge upstream/master
    ```

1. On your local machine, be sure that you are on the `master` branch.

    ```
    git checkout master
    ```

   Make the changes you need to fix your bug. Add the modified files to the commit. Remember to edit the DESCRIPTION file to update the version number.

    ```
    git add <files changed>
    # after version bump
    git add DESCRIPTION
    ```

   Commit the modified files. It is helpful to tag the commit as bug fix.

    ```
    git commit -m "bug fix: my bug fix"
    ```


1. (Alternative) If the changes are non-trivial, create a new branch where you can easily abandon any false starts. Merge the final version onto `master`

    ```
    git checkout master
    git checkout -b bugfix-my-bug
    ## add and commit to this branch. When the bug fix is complete...
    git checkout master
    git merge bugfix-my-bug
    ```

1. These changes are on your `master` branch. The changes need to be available in your `release` branch as well,

    ```
    git checkout <RELEASE_X_Y>
    git merge master
    ## FIXME: version bump in master not same as in release
    ```
1. Push your changes to both the Github and _Bioconductor_ `master` and `<RELEASE_X_Y>` branches. Make sure you are on the correct branch on your local machine.

   For the `master` branch,

    ```
    git checkout master
    git push upstream master
    git push origin master
    ```

   For the `release` branch,

    ```
    git checkout <RELEASE_X_Y>
    git push upstream <RELEASE_X_Y>
    git push origin <RELEASE_X_Y>
    ```

[Scenario-3]: scenario-3-pull-from-gitbioc-push-github.md
