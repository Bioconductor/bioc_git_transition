# Developer -- Add Bioconductor package to git.bioconductor.org

Bioconductor expects its developers to use a git-based version control system. This will allow the developers to easily interact with Bioconductor's private git server.

Bioconductor git server is available at:

1. `SSH` read/write access to developers: `git@git.bioconductor.org`

1. `HTTPS` read only access to the world: `https://git.bioconductor.org`


This document will explain a developers workflow using GitHub.

## Developer has a public GitHub repository

The developers will have a public GitHub repository where they can interact with their package community, accept pull requests, issues, and other GitHub collaboration features. As the developer actively develops they will have the repository cloned on their local machine. The GitHub repository is where the developer should be maintaining his code.

Eg:

```
git clone git@github.com:developer/<ExamplePackage>.git
```

The remotes on the package will be that of GitHub's, because it is the remote server being used by the developer. The developer can check if the remote is configured properly using,

```
git remote -v
```

This should show,

```
origin  git@github.com:developer/example_package.git (fetch)
origin  git@github.com:developer/example_package.git (push)
```

the remote shows that you can `fetch` and `push` to those remote locations, this remote location is called `origin`.

## Add remotes

Our goal is to add another remote location to the local repository, the Bioconductor private server.

```
git remote add upstream git@git.bioconductor.org:packages/example_package.git
```

To check if the remote has been added properly, we can check it using:

```
git remote -v
```

which should show,

```
origin  git@github.com:developer/example_package.git (fetch)
origin  git@github.com:developer/example_package.git (push)
upstream    git@git.bioconductor.org:packages/example_package.git (fetch)
upstream    git@git.bioconductor.org:packages/example_package.git (push)
```

NOTE: To be able to `fetch` and `push` to git@git.bioconductor.org, the developer should have ssh access. More about how to get ssh access on the [Contributions.md](https://github.com/Bioconductor/BiocContributions).


## Push to remote master and remote upstream

If a developer makes a change to his package, it is important that he push to BOTH his GitHub, and Bioconductor's git server. This is important if the developer wants the Bioconductor remote to be in sync.

First, push to the remote `origin` in the branch `master`:

```
git push origin master
```

Second, push to the remote `upstream` in the branch `master`:

```
git push upstream master
```

This will sync BOTH the developers GitHub repository and the Bioconductor servers repository.

## Pull from remote upstream and keep things in sync

One thing a developer has to do is get updates from any changes or commits made to the Bioconductor repository,

To get updates from the Bioconductor repository (i.e changes made by the core team)

```
git fetch --all
git merge upstream/master
```

To get updates from the GitHub repository (i.e changes made by your collaborators)

```
git merge origin/master
```
