# Scenario 2: Push to both GitHub and _Bioconductor_ repositories

**Goal:** During everyday development, you commit changes to your local repository and wish to push these commits to both GitHub and _Bioconductor_ repositories.

**NOTE:** See [Scenario 3][] for best practices for getting updates from _Bioconductor_ and GitHub before committing local changes.

## Steps:

1. We assume you already have a GitHub repository with the right setup to push to _Bioconductor_'s git server (git@git.bioconductor.org). If not please see FAQ's on how to get access and follow [Scenario 1][]. We use a clone of the `BiocGenerics` package in the following example.

2.  To check that remotes are set up properly, run the command inside your local machine's clone.

    ```
    git remote -v
    ```

    which should produce the result (where <developer> is your GitHub username):

    ```
    origin  git@github.com:<developer>/BiocGenerics.git (fetch)
    origin  git@github.com:<developer>/BiocGenerics.git (push)
    upstream    git@git.bioconductor.org:packages/BiocGenerics.git (fetch)
    upstream    git@git.bioconductor.org:packages/BiocGenerics.git (push)
    ```

3. Make and commit changes to the `master` branch or the latest release branch (`RELEASE_X_Y`),

    ```
    git checkout master
    ## edit files, etc.
    git add <name of file changed>
    git commit -m "My informative commit message describing the change"
    ```

4. Push updates to GitHub's (`origin`) `master` branch

    ```
    git push origin master
    ```

    **Note**. Use `RELEASE_X_Y` instead of `master` if you are committing to and updating the release branch, `git push origin RELEASE_X_Y`.

5.  Next, push updates to _Bioconductor_'s (`upstream`) `master` branch

    ```
    git push upstream master
    ```

    (use `git push upstream RELEASE_X_Y` to push to _Bioconductor_'s release branch).

6. Confirm changes, e.g., by visiting the GitHub web page for the repository.




[Scenario 1]: scenario-1-svn-to-github.md
[Scenario 3]: scenario-3-pull-from-gitbioc-push-github.md
