# Scenario 9: Sync existing Github and Bioconductor repositories

**Goal:** Sync your Github repository and Bioconductor repository to the same commit. All the branches should be in sync.

## Steps:

*   Fetch all the updates from both remotes, Github and Bioconductor

    ```
    git fetch --all
    ```

*   Make sure you are on the master branch, if not, checkout master.
    ```
    git checkout master
    ```

*   Pull updates from your origin into your local machine.
    ```
    git pull
    ```

*   Merge updates into your `master` from Bioconductor (`upstream`) remote
    ```
    git merge upstream/master
    ```

*   Push to both Github and Bioconductor repositories, to have them in sync,

    ```
    git push origin master
    git push upstream master
    ```

If you want to update a release branch, simply replace `master` with name of the release branch, eg: `RELEASE_3_5`

*   (Optional) If you have conflicts after `pull` or `merge` step. Please take a look at the our manual on how to [Resolve Conflicts][].


[Resolve Conflicts]: scenario-5-resolve-conflicts.md
