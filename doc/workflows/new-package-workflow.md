# New package workflow

**Goal**: You are a developer who wants to contribute a new package to Bioconductor. You have been developing on GitHub (or another git based platform). How do you contribute your package to Bioconductor?

## Steps:

We use the package "BiocGenerics" as an example.

1. We assume that you have already finished developing you package according to the Bioconductor [Package Guidelines][], and its available on GitHub.

1. Your next step is to notify the Bioconductor team, about the package you developed for Bioconductor. You can do this be adding an issue to the [Contributions Issues][] page. Please follow that [README.md][] file on the Contributions page for additional information.

1. After adding your package to the [Contributions Issues][] page, a member from the Bioconductor core team will be assigned to your package for review. Provided the review process goes as planned and your package is accepted, it will be added to the Bioconductor git server by the core team.

1. Once your package has been accepted to Bioconductor, you should be able to see it on the [Bioconductor git server][] which is available at:

    **ssh read/write access to developers:** `git@git.bioconductor.org`

    **https read only access to the world:** `https://git.bioconductor.org`

1. For developers/maintainers, you are required to send your ssh public key to packages@bioconductor.org and you will be added to the server, and given access to your package.

1. The bioconductor core team will make changes on your package for bugs or bumping a version number for a new release. So it becomes essential that you add the Bioconductor repository as another remote to your machine's git repository. You need to add a remote, using:

    `git remote add upstream git@git.bioconductor.org:packages/BiocGenerics.git`

1.  Fetch content from remote upstream,

    `git fetch upstream`

    **NOTE:** This step will fail if you don't have access as a developer to the Bioconductor repository.

1.  Merge upstream with origin's `master` branch,

    `git merge upstream/master`

1. Push changes to your GitHub (`origin`) repository's branch `master`,

    `git push origin`

1. Check that your changes have been incorporated in the [nightly builds][] at Bioconductor.


Additional Resources:

[Create a new GitHub account][]

[Create a new GitHub repository][]



[Create a new GitHub account]: https://help.github.com/articles/signing-up-for-a-new-github-account/

[Create a new GitHub repository]: https://help.github.com/articles/create-a-repo/

[Bioconductor git server]: https://git.bioconductor.org

[nightly builds]: https://www.bioconductor.org/checkResults/

[README.md]: https://github.com/Bioconductor/Contributions

[Contributions Issues]: https://github.com/Bioconductor/Contributions/issues

[Package Guidelines]: https://www.bioconductor.org/developers/package-guidelines/


