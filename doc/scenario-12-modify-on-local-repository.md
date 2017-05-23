# Scenario 12: Clone and modify a _Bioconductor_ repository for personal use

**Goal:** A user would like to modify functions in a package to meet their needs. There is no Github repository for the package.

## Steps:

1. Clone the package from the _Bioconductor_ repository. Use the **https** protocol

    ```
    git clone https://git@git.bioconductor.org/packages/<ExamplePackage>
    ```

1. Make changes which you need in the _Bioconductor_ package. This is up to the user to make whatever changes he wishes. Commit the changes to your local repository. A best practice might modify the changes in a new branch

     ```
     git checkout -b feature-my-feature
     ## modify
     git commit -a -m "feature: a new feature"
     ```

   and then merge the feature onto the branch corresponding to the release in use, e.g.,

    ```
    git checkout <RELEASE_X_Y>
    git merge feature-my-feature
    ```

1. Rebuild (to create the vignette and help pages) and reinstall the package in your local machine by running in the parent directory of _ExamplePackage_

    ```
    R CMD build ExamplePackage
    R CMD INSTALL ExamplePackage_<version.number>.tar.gz
    ```

1. The package with the changes should be available in your local _R_ installation.
