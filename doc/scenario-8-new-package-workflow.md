1. create github repo
2. add to git.bioc (Core team responsibility)
3. remotes

# Scenario 8: New package workflow

**Goal**: You have developed a package in GitHub, followed the _Bioconductor_ new package [Contributions README][] and other guidelines, and your package has been accepted! The accepted package is added to the _Bioconductor_ git repository. Now what?

## Steps:

1. Send your SSH public key to packages@bioconductor.org and you will be added to the server, and given access to your package.

1. Your package is visible on the [_Bioconductor_ git server][] which is available at:

    **SSH read/write access to developers:** `git@git.bioconductor.org`

    **HTTPS read only access to the world:** `https://git.bioconductor.org`

1. You will need to push any future changes to your package to the _Bioconductor_ repository, and pull changes the _Bioconductor_ core team will make (e.g., bug fixes or bumping a version number for a new release). Add a remote to your machine's local git repository using:

    ```
    git remote add upstream git@git.bioconductor.org:packages/BiocGenerics.git`
    ```

1. See [Scenario 3][] for to how fetch updates from _Bioconductor_ and push to GitHub.


[Scenario 3]: scenario-3-pull-from-gitbioc-push-github.md
[Contributions README]: https://github.com/Bioconductor/Contributions
[_Bioconductor_ git server]: https://git.bioconductor.org
