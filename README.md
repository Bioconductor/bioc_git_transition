# _Bioconductor_ SVN to GIT transition

This package provides functionality to allow for SVN - Git transition for
the _Bioconductor_ Project.

Goals:
* Create a private git server with all Bioconductor packages, including commit
  history from each of the _RELEASE_ branches and also the _devel_ branch.

Usage:
* This is a smaller test set of packages so your choices
are limited to a `List of available packages` (refer below).

* Clone a package:

        git clone git@git.bioconductor.org:packages/<package_of_choice>

* See the branches available:

        cd BiocGenerics
        git branch -a

* Checkout branch and see if the commit history is correct (most important step):

        git checkout RELEASE_3_0
        git log
