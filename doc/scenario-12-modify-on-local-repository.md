# Scenario 12: Clone and modify on local repository

**Goal:** There are developers/users who do not contribute to Bioconductor, but would like to modify functions in the package to meet their needs.

## Steps:

1. Clone the package from the Bioconductor repository, use the **https** protocol

    ```
    git clone https://git@git.bioconductor.org/packages/<ExamplePackage>
    ```

1. Make changes which you need in the Bioconductor package. This is up to the developer/user to make whatever changes he wishes.

1. Rebuild and reinstall the package in your local machine,

    ```
    R CMD build ExamplePackage
    R CMD INSTALL ExamplePackage_version_number.tar.gz
    ```

1. The package with the changes should be available in your local R installation.
