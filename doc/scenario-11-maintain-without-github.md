# Scenario 11: Maintaining your package on Bioconductor without a Github repo

**Goal:** Developer *without* or *does not want* a Github account or repository wants to maintain their package on Bioconductor.

## Steps:

### Clone and setup the package on your local machine.

1. Developer or maintainer of the Bioconductor package needs to make sure that they have correct `SSH` access rights to the Bioconductor repository hosted on our private git server. If this is not the case, please contact packages@bioconductor.org.

1. Clone package with `SSH` on your local machine,

    ```
    git clone git@git.bioconductor.org:packages/<ExamplePackage>
    ```

    **NOTE:** If you clone with `https` you will NOT get read+write access.

1. Once the package is cloned, there will only be a single remote. To see remote, use:

    ```
    git remote -v
    ```

    which will display,

    ```
    origin    git@git.bioconductor.org:packages/<ExamplePackage>.git (fetch)
    origin    git@git.bioconductor.org:packages/<ExamplePackage>.git (push)
    ```

    This indicates that your git repository has only one remote `origin`, which is the Bioconductor repository.

### How to make changes and maintain.

1. Before making changes to your package, make sure to `pull` changes or updates from the Bioconductor repository. This is needed to avoid conflicts.

    ```
    git pull
    ```

1. Make the required changes, then `add` and `commit` your changes to your `master` branch.

    ```
    git add <files changed>
    git commit -m "My informative commit message"
    ```

1. (Optional) If the changes need to be available on the `<RELEASE_X_Y>` branch, assuming that you have already made and committed your changes to the `master` branch

    First, checkout the branch `<RELEASE_X_Y>` using:

    ```
    git checkout -b <RELEASE_X_Y>
    ```

    Then, merge `master` into the `<RELEASE_X_Y>` branch

    ```
    git merge master
    ```
    A new commit message will show up after this step, with the message `Merge branch 'master' into <RELEASE_X_Y>`. It will be committed to `<RELEASE_X_Y>` branch when you save.

1. You have to push your commits to the Bioconductor repository to make them available to the user community.

    Push changes to the `master` branch using:

    ```
    git checkout master
    git push origin master
    ```

    Push changes to the `<RELEASE_X_Y>` branch using:

    ```
    git checkout <RELEASE_X_Y>
    git push origin <RELEASE_X_Y>
    ```
