# Scenario 3: Get updates from Bioconductor and update Github

It is always a good idea to fetch updates from Bioconductor (remote `upstream`), to see if there were any changes made by your collaborators or the Bioconductor core team.

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
