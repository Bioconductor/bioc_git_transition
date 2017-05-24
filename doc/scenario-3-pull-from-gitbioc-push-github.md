# Scenario 3: Pull updates from _Bioconductor_ and push to GitHub

**Goal:** Your _Bioconductor_ repository has been updated by the core team. You want to fetch these commits from _Bioconductor_, merge them into your local repository, and push them to GitHub.

**NOTE:** It is always a good idea to fetch updates from _Bioconductor_  before making more changes. This will help prevent merge conflicts.

## Steps

These steps update the `master` branch.

1. Make sure you are on the appropriate branch.

    ```
    git checkout master
    ```

1. Fetch content from _Bioconductor_

    ```
    git fetch upstream
    ```

1. Merge upstream with the appropriate local branch

    ```
    git merge upstream/master
    ```

    If you have conflicts after the `merge` step, see [Scenario 5][].

1. Push changes to GitHub's (`origin`) `master` branch

     ```
     git push origin master
     ```

To pull updates to the current `RELEASE_X_Y` branch, replace `master` with `RELEASE_X_Y` in the lines above.

See [Scenario 9][] to sync your local repository with changes to both the _Bioconductor_ and Github repositories.

[Scenario 5]: scenario-5-resolve-conflicts.md
[Scenario 9]: scenario-9-sync-existing-github-gitbioc.md
