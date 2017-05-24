# Update Release branch

## Steps:

1.  Developers/Maintainers make changes to the current release branch. You will need to add a branch to GitHub, to be able to push these changes.

    ```
    # Fetch all updates
    git fetch upstream

    # Checkout new branch RELEASE_3_5, from upstream/RELEASE_3_5
    git checkout -b RELEASE_3_5 upstream/RELEASE_3_5

    # Push updates to remote origin's new branch RELEASE_3_5
    git push -u origin RELEASE_3_5
    ```

1. Check your GitHub repository to confirm that the `master` (and optionally `RELEASE_3_5`) branches are present.

