1. create github repo
2. add to git.bioc (Core team responsibility)
3. remotes

# Scenario 8: New package workflow

**Goal**: You have developed a package in Github, followed the Bioconductor new package [Contributions README][] and other guidelines, and your package has been accepted! The accepted package is added to the Bioconductor git repository. Now what?

## Steps:

1. Send your ssh public key to packages@bioconductor.org and you will be added to the server, and given access to your package.

1. Your package is visible on the [Bioconductor git server][] which is available at:

    **ssh read/write access to developers:** `git@git.bioconductor.org`

    **https read only access to the world:** `https://git.bioconductor.org`

1. You will need to push any future changes to your package to the Bioconductor repository, and pull changes the Bioconductor core team will make (e.g., bug fixes or bumping a version number for a new release). Add a remote to your machine's local git repository using:

    ```
    git remote add upstream git@git.bioconductor.org:packages/BiocGenerics.git`
    ```

1. See [Scenario-3][] for to how fetch updates from Bioconductor and push to Github.


[Scenario-3]: scenario-3-pull-from-gitbioc-push-github.md

[Contributions README]: https://github.com/Bioconductor/Contributions

[Bioconductor git server]: https://git.bioconductor.org
