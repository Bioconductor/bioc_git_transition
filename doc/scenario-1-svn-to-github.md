# Scenario 1: Create Github repository for existing Bioconductor repository

The SVN to git transition is all done and dusted. What should a developer do now?

## Steps:

1.  [Create a new Github account][] if you don't have one.

2.  [Create a new Github repository][] on your account, with the name of the existing Bioconductor repository you wish to clone.

    We use "BiocGenerics" as an example for this scenario.

3.  On your local machine clone the empty repository from Github

    `git clone git@github.com:developer/BiocGenerics.git`

4.  Add remote to your cloned repository,

    For Bioconductor repositories that you have read / write (ssh) access, use:

    `git remote add upstream git@git.bioconductor.org:packages/BiocGenerics.git`

    For read-only Bioconductor repositories, use:

    `git remote add upstream https://git.bioconductor.org/packages/BiocGenerics.git`

5.  Fetch content from remote upstream,

    `git fetch upstream`

6.  Merge upstream with origin's master branch,

    `git merge upstream/master`

7. Push changes to your origin master,

    `git push origin`

8.  (Optional) Add a branch to Github,

    ```
    # Fetch all updates
    git fetch upstream

    # Checkout new branch RELEASE_3_5, from upstream/RELEASE_3_5
    git checkout -b RELEASE_3_5 upstream/RELEASE_3_5

    # Push updates to remote origin's new branch RELEASE_3_5
    git push -u origin RELEASE_3_5
    ```

9. Check your Github repository to confirm that the `master` (and optionally `RELEASE_3_5`) branches are present.

[Create a new Github account]: https://help.github.com/articles/signing-up-for-a-new-github-account/

[Create a new Github repository]: https://help.github.com/articles/create-a-repo/
