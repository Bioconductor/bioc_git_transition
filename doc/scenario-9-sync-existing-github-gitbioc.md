# Scenario 9: Sync existing _Bioconductor_ and Github repositories

**Goal:** Ensure that your local, _Bioconductor_, and Github repositories are all in sync.

## Steps:

1. Fetch updates from all (_Bioconductor_ and Github) remotes.

    ```
    git fetch --all
    ```

1. Make sure you are on the master branch.

    ```
    git checkout master
    ```

1. Merge updates from the _Bioconductor_ (`upstream`) remote

    ```
    git merge upstream/master
    ```

    If you have conflicts after the `merge` step, see [Scenario 5][].

1. Merge updates from the Github (`origin`) remote

    ```
    git merge origin/master
    ```

1. Push to both _Bioconductor_  and GitHub repositories.

    ```
    git push upstream master
    git push origin master
    ```

1. Repeat for the release branch, replacing `master` with the name of the release branch, eg: `RELEASE_3_5`. Remember that only `master` and teh current release branh of _Bioconductor_ repositories can be updated.

[Scenario 5]: scenario-5-resolve-conflicts.md
