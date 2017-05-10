# Scenario 3: Get updates from Bioconductor and update Github

**Goal:** Your Bioconductor repository has been updated by the core team. You want to fetch these commits from Bioconductor (remote `upstream`), merge them into your local repository, and push them to Github.

**NOTE:** It is always a good idea to fetch updates from Bioconductor as a precautionary measure before making more changes. This will help prevent conflicts.

## Steps

1. Make sure you are on the appropriate branch, if the change was made on `upstream/master` or `upstream/RELEASE_X_Y`.

    ```
    git checkout master
    ## alternatively 'git checkout RELEASE_X_Y' for the release branch
    ```

2. Fetch content from Bioconductor

    ```
    git fetch upstream
    ```

3. Merge upstream with your local branch, (it is this step, where you need to be sure you have the correct branch checked out)

    ```
    git merge upstream/master
    ```

4. Push changes to Github's (`origin`) `master` branch

     ```
     git push origin
     ```
