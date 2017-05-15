# Scenario 3: Get updates from _Bioconductor_ and update GitHub

**Goal:** Your _Bioconductor_ repository has been updated by the core team. You want to fetch these commits from _Bioconductor_ (remote `upstream`), merge them into your local repository, and push them to GitHub.

**NOTE:** It is always a good idea to fetch updates from _Bioconductor_ as a precautionary measure before making more changes. This will help prevent merge conflicts.

## Steps

1. Make sure you are on the appropriate branch, depending on the location of the changes, either `upstream/master` or `upstream/RELEASE_X_Y`.

    ```
    git checkout master
    ## alternatively 'git checkout RELEASE_X_Y' for the release branch
    ```

2. Fetch content from _Bioconductor_

    ```
    git fetch upstream
    ```

3. Merge upstream with the appropriate local branch

    ```
    ## on branch `master`
    git merge upstream/master

    ## alternatively, on branch `RELEASE_X_Y`
    git merge upstream/RELEASE_X_Y
    ```

4. Push changes to GitHub's (`origin`) `master` branch

     ```
     git push origin
     ```
