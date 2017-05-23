# _Bioconductor_ SVN to GIT transition

This package provides functionality to allow for SVN - Git transition for
the _Bioconductor_ Project.

## Goals

* Create a private git server with all Bioconductor packages, including commit
  history from each of the _RELEASE_ branches and the _devel_ branch.

## Setup

* To participate in the current testing cycle, communicate a single
  ssh public key to martin.morgan at roswellpark.org. Alternatively,
  provide a GitHub id and we'll use the first key in
  `https://github.com/<github_id>.keys`

## Usage: clone, push, pull, etc.

* **ALPHA testing**. Remember, repositories are *static* snapshots of
  svn; they are not current, changes commited here are *not*
  propagated to svn, and will *not* be retained.

* Clone a package for read-only access

        git clone https://git.bioconductor.org/packages/<package>.git

  or for read / write (appropriate permissions required)

        git clone git@git.bioconductor.org:packages/<package>

* See the branches available

        cd BiocGenerics
        git branch -a

* Checkout branch and see if the commit history is correct

        git checkout RELEASE_3_0
        git log

* Local commits

        ...
        git commit -m "alpha test" -a

* Push commits to writeable repositories (commits will be lost after
  testing phases are complete)

        git push

* (Non-core users): Fail to push changes on non-`master` or
  `RELEASE_3_4` branch.

        git checkout RELEASE_3_3
        ...
        git commit -m "alpha test" -a
        git push    # fail

## Usage: exploration

* Elementary browser interface available at

        https://git.bioconductor.org

* View R(ead) / W(rite) privileges

        ssh git@git.bioconductor.org info        # all packages
        ssh git@git.bioconductor.org info packages/BiocGenerics

## Status

- [x] ssh-based read-only access to all repositories
- [x] ssh-based read-write access to selected repositories
- [x] public read-only access to all repositories
- [ ] experiment-data packages

## Troubleshooting

### SSH

`ssh` may have to choose between multiple keys. Resolve this with an
entry in the plain-text `~/.ssh/config` file, where `identityfile`
disambiguates the key you'd like to use.

        host git-bioc
            user git
            hostname git.bioconductor.org
            port 22
            identityfile ~/.ssh/id_rsa

Use as `git clone git-bioc:packages/BiocGenerics`.
