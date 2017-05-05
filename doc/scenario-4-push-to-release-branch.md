# Scenario 4: Push updates to release branch (RELEASE_X_Y)

Developers will have write access to only the most recent release, example, `RELEASE_3_5` if `RELEASE_3_6` is the current development cycle. Whatever updates developers make to their `master` branch will be captured in the latest development cycle.

NOTE: For developers who are used to the SVN way of development in Bioconductor, `devel` (svn) --> `master` (git).


## Steps:

1. Pull any changes from Github or other `origin` repository

    ```
    git pull
    ```

1. Fetch any updates from the Bioconductor `upstream` repository

   ```
   git fetch upstream
   ```

1. Checkout the branch. If the branch was not previously available on your local machine, use:

    ```
    git checkout -b RELEASE_3_5 upstream/RELEASE_3_5
    ```

    If the branch was already available, use:

    ```
    git checkout RELEASE_3_5
    git merge upstream/RELEASE_3_5
    ```

1. Make appropriate changes as needed, and bump the version number in the DESCRIPTION file.

1. Add and commit the files you made the changes to,  

    ```
    git add <file which changed>
    git commit -m "My informative commit message"
    ```

1.  Push to both the Bioconductor repository, and your own Github repository.

    ```
    git push origin RELEASE_3_5
    git push upstream RELEASE_3_5
    ```
