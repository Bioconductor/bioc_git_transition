# Scenario 1: Create Github repository for existing Bioconductor repository

**Goal:** The SVN to git transition is all done and dusted. As a longterm SVN developer you don't have a Github repository of your package. You'd like to create a new Github repository, so that your user community can engage in the development of your package.

This scenario does NOT involve setting up a _fork_ or using an existing Github repository. See [scenario-9][] for details on that.

## Steps:

1.  [Create a new Github account][] if you don't have one.

1.  Set up remote access to Github via SSH or Https.  Please check [which-remote-url-should-i-use][] and [add your public key to your GitHub account][].

2.  [Create a new Github repository][] on your accoungt, with the name of the existing Bioconductor package that you have been previously developing in SVN.

    We use "BiocGenerics" as an example for this scenario.

    ![](images/create_repo.png)

    After pressing the 'Create repository' button, ignore the instructions that Github provides, and follow the rest of this document.

1.  On your local machine clone the empty repository from Github.

    Use `https` URL (replace `<developer>` with your Github username)

    ```
    git clone https://github.com/<developer>/BiocGenerics.git
    ```

    or `SSH` URL

    ```
    git clone git@github.com:<developer>/BiocGenerics.git
    ```

1.  Add remote to your cloned repository.

    Change the current working directory to your local repository cloned in previous step.

    ```
    cd BiocGenerics
    ```

    For Bioconductor repositories that you have read / write (ssh) access, use:

    ```
    git remote add upstream git@git.bioconductor.org:packages/BiocGenerics.git
    ```

    For read-only Bioconductor repositories, use:

    ```
    git remote add upstream https://git.bioconductor.org/packages/BiocGenerics.git
    ```

5.  Fetch content from remote upstream,

    ```
    git fetch upstream
    ```

6.  Merge upstream with origin's master branch,

    ```
    git merge upstream/master
    ```

    **NOTE:** If you have the error `fatal: refusing to merge unrelated histories`, then the repository cloned in step 4 was not empty. Either clone an empty repository, or see [scenario-9][].

7. Push changes to your origin master,

    ```
    git push origin master
    ```

    **NOTE:** Run the command `git config --global push.default matching` to always push local branches to the remote branch of the same name, allowing use of `git push origin` rather than `git push origin master`.

8.  (Optional) Add a branch to Github,

    ```
    ## Fetch all updates
    git fetch upstream

    ## Checkout new branch RELEASE_3_5, from upstream/RELEASE_3_5
    git checkout -b RELEASE_3_5 upstream/RELEASE_3_5

    ## Push updates to remote origin's new branch RELEASE_3_5
    git push -u origin RELEASE_3_5
    ```

9. Check your Github repository to confirm that the `master` (and optionally `RELEASE_3_5`) branches are present.

[Create a new Github account]: https://help.github.com/articles/signing-up-for-a-new-github-account/

[Create a new Github repository]: https://help.github.com/articles/create-a-repo/

[scenario-9]: scenario-9-sync-existing-github-gitbioc.md

[which-remote-url-should-i-use]: https://help.github.com/articles/which-remote-url-should-i-use/

 [add your public key to your GitHub account]: https://help.github.com/articles/connecting-to-github-with-ssh/
