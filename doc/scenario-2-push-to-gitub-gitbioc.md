# Scenario 2: Push to both Github and Bioconductor repositories

**Goal:** Push updates to both Github repository and Bioconductor repositories.

## Steps:

1. We assume you already have a Github repository with the right setup to push to Bioconductor's git server (git@git.bioconductor.org). If not please see FAQ's on how to get access and follow [Scenario-1][]. We use a clone of the BiocGenerics package in the following example.

2.  To check that remotes are set up properly, run the command inside your local machine's clone.

    ```
    git remote -v
    ```

    which should produce the result

    ```
    origin  git@github.com:developer/BiocGenerics.git (fetch)
    origin  git@github.com:developer/BiocGenerics.git (push)
    upstream    git@git.bioconductor.org:packages/BiocGenerics.git (fetch)
    upstream    git@git.bioconductor.org:packages/BiocGenerics.git (push)
    ```

3. Make and commit changes to `master` branch or the latest release branch (`RELEASE_X_Y`),

    ```
    git checkout master
    ## edit files, etc.
    git add <name of file changed>
    git commit -m "My informative commit message describing the change"
    ```

4. Push updates to Github's (`origin`) `master` branch

    ```
    git push origin master
    ```

    (use `RELEASE_X_Y` instead of `master` if you are committing to and updating the release branch, `git push origin RELEASE_X_Y`).

5.  Next, push updates to Bioconductor's (`upstream`) `master` branch

    ```
    git push upstream master
    ```

    (use `git push upstream RELEASE_X_Y` to push to Bioconductor's release branch).

6. Confirm changes, e.g., by visiting the Github web page for the repository.

(Optional)

It is always a good idea to fetch updates from remote origin and remote upstream, to see if there were any changes made by your collaborators or the Bioconductor core team. Before pushing changes please do [Scenario-3][].


[Scenario-1]: scenario-1-svn-to-github.md
[Scenario-3]: scenario-3-pull-from-gitbioc-push-github.md
