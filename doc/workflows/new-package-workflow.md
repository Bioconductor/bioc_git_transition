# New package workflow

**Goal**: You are a developer who wants to contribute a new package to Bioconductor. You have been developing on GitHub (or another git based platform). How do you contribute your package to Bioconductor?

## Steps:

We use the package "BiocGenerics" as an example.

1. We assume that you have already finished developing you package according to the Bioconductor [Package Guidelines][].

1. If you do not have your package on GitHub, we highly recommend using it. You will be able to leverage features such as Pull requests, issue tracking, and many more social coding ideas which will make your Bioconductor package community happier. To use GitHub, please [Create a new GitHub account][].

1. The next step is to [Create a new GitHub repository][] with your package name.

1.  On your **local machine** initiate "git" in your package repository

    ```
    cd BiocGenerics
    git init
    ```

1. Once you have initialized the git repository on your local machine, add all the contents you need for the Bioconductor package,

    ```
    git add DESCRIPTION NAMESPACE NEWS R/* inst/* man/* tests/* vignettes/*
    ```

    You can also just do `git add *` if you wish to add everything in the package.

1. Commit all your new additions to your local git repository,

    ```
    git commit -m "New bioconductor package named BiocGenerics"
    ```

1.  Add a remote to your local git repository,

    `git remote add origin git@github.com:developer/BiocGenerics.git`

2.  To check that remotes are set up properly, run the command inside your local machine's clone.

    `git remote -v`

    which should produce the result

    ```
    origin  git@github.com:developer/BiocGenerics.git (fetch)
    origin  git@github.com:developer/BiocGenerics.git (push)
    ```

1. Push the new content to your GitHub repository, so it's visible to the world

    `git push -u origin master`

    **NOTE: Check your GitHub account, and make sure you are able to view all your files.**

1. Your next step is to notify the Bioconductor team, about the package you developed to contribute to Bioconductor. You can do this be adding an issue to the [Contributions Issues][] page. Please follow that [README.md][] file on the Contributions page for additional information.

1. After adding your package to the [Contributions Issues][] page, a member from the Bioconductor core team will be assigned to your package for review. Provided the review process goes as planned and your package is accepted, it will be added to the Bioconductor git server by the core team.

1. Once your package has been accepted to Bioconductor, you should be able to see it on the [Bioconductor git server][] which is available at:

    **ssh read/write access to developers:** `git@git.bioconductor.org`

    **https read only access to the world:** `https://git.bioconductor.org`

1. For developers/maintainers, you are required to send your ssh public key to `devteam-bioc@bioconductor.org` and you will be added to the server, and given access to your package.

1. The bioconductor core team will make changes on your package for bugs or bumping a version number for a new release. So it becomes essential that you add the Bioconductor repository as another remote to your machine's local git repository. You need to add a remote, using:

    `git remote add upstream git@git.bioconductor.org:packages/BiocGenerics.git`

1.  Fetch content from remote upstream,

    `git fetch upstream`

    **NOTE:** This step will fail if you don't have access as a developer to the Bioconductor repository.

1.  Merge upstream with origin's `master` branch,

    `git merge upstream/master`

1. Push changes to your GitHub (`origin`) repository's branch `master`,

    `git push origin`

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


[README.md]: https://github.com/Bioconductor/Contributions

[Contributions Issues]: https://github.com/Bioconductor/Contributions/issues

[Package Guidelines]: https://www.bioconductor.org/developers/package-guidelines/

[Create a new GitHub account]: https://help.github.com/articles/signing-up-for-a-new-github-account/

[Create a new GitHub repository]: https://help.github.com/articles/create-a-repo/
[Bioconductor git server]: https://git.bioconductor.org
