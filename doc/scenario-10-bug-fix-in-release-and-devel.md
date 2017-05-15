# Scenario 10: Bug fix in `release` and  `master` branch

**Goal:** Maintainers will have to fix bugs from time to time, and make sure the patch is available both in the `master` branch( svn `devel`) and the current `release` branch.

## Steps:

1. Make sure to follow [Scenario-3][] to pull any potential changes in the code from the Bioconductor core team.

2. Once you have done that, on your local machine, make the changes you need to fix your bug. It is helpful to tag the commit as bug fix, and then update the version number.

3. On your local machine,

    ```
    git add <files changed>
    # after version bump
    git add DESCRIPTION
    ```

    After adding the files which changed,

    ```
    git commit -m "bug fix and version bump"
    ```

4. The assumption is that you are making these changes on your `master` branch. Once the changes have been committed, you need to make sure these changes are available in your `release` branch as well,

    ```
    git checkout <RELEASE_X_Y>
    git merge master
    ## FIXME: version bump in master not same as in release
    ```
5. Then, make sure you push your changes to both the Github and Bioconductor, `master` and `<RELEASE_X_Y>` branches. Make sure you are on the correct branch on your local machine,

    For the `master` branch,

    ```
    git checkout master
    git push upstream master
    git push origin master
    ```

    then, for the `release` branch,

    ```
    git checkout <RELEASE_X_Y>
    git push upstream <RELEASE_X_Y>
    git push origin <RELEASE_X_Y>
    ```

[Scenario-3]: scenario-3-pull-from-gitbioc-push-github.md
