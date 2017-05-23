# Scenario 8: New package workflow

**Goal**: You have developed a package in GitHub, following the _Bioconductor_ new package [Contributions README][] and other guidelines, and your package has been accepted! The accepted package has been added to the _Bioconductor_ git repository. Now what?

## Steps:

1. _Bioconductor_ needs to know your SSH 'public key'. _Bioconductor_ will use the first key in `https://github.com/<your-github-id>.keys`.

    Alternatively, send your SSH public key and package name to packages@bioconductor.org. Your key and appropriate permissions will be added to the _Bioconductor_ git server.

1. Your package is visible on the [_Bioconductor_ git server][].

    **SSH read/write access to developers:** `git@git.bioconductor.org`

    **HTTPS read only access to the world:** `https://git.bioconductor.org`

1. Conigure the "remotes" of your local git repository. You will need to push any future changes to your package to the _Bioconductor_ repository, and pull changes the _Bioconductor_ core team will make (e.g., bug fixes or bumping a version number for a new release). Add a remote to your machine's local git repository using:

    ```
    git remote add upstream git@git.bioconductor.org:packages/<YOUR-REPOSITORY-NAME>.git`
    ```

1. See other scenarios for working with _Bioconductor_ and GitHub repositories, in particular:

    - [Scenario 3][]: Fetch updates from the _Bioconductor_ core team.
    - [Scenario 2][]: Push local commits to _Bioconductor_ and GitHub.
    - [Scenario 10][]: Fix bugs in devel and release branches.

[Scenario 2]: scenario-2-push-to-gitub-gitbioc.md
[Scenario 3]: scenario-3-pull-from-gitbioc-push-github.md
[Scenario 10]: scenario-10-bug-fix-in-release-and-devel.md
[Contributions README]: https://github.com/Bioconductor/Contributions
[_Bioconductor_ git server]: https://git.bioconductor.org
