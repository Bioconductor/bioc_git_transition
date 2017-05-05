# Scenario 6: Abandon changes and start fresh

**Goal:** You want to start fresh after failing to resolve conflicts or some other issue. If you intend to go nuclear, please contact the bioc-devel@bioconductor.org mailing list.

# Going sub-nuclear:  Make a new branch

One way you can ignore your work, and make a new branch is by replacing your local and Github repository `master` branch with the Bioconductor `master` branch.

NOTE: This works only if you haven't pushed the change causing the issue to the Bioconductor repository.

## Steps:

1. Checkout a new branch called `master_backup` with tracking set to `upstream/master`.

    ```
    git checkout -b master_backup upstream/master
    ```

2. Then, rename the branches you currently have on your local machine.

    First, rename the `master` to `master_deprecated`, and finally, rename `master_backup` to `master`. This process is called the classic **Switcheroo**.

    ```
    git branch -m master master_deprecated
    git branch -m master_backup master
    ```

3. You will now have to `force push` the changes to your Github (`origin`) `master` branch.

    ```
    git push -f origin master
    ```

4. **(Optional)** If you have commits on your `master_deprecated` branch that you would like ported on to your new `master` branch. Git has a special feature called `cherry-pick`

    Take a look at which commit you want to cherry-pick on to the new master branch, using `git log master_deprecated`, copy the correct commit id, and use:

    ```
    git cherry-pick <commit id>
    ```

# Revert to a previous commit

If you find yourself in a place where you want to abandon the changes and go back to a previous commit id, you can always `revert`. Remember that, if you use `HEAD` as the commit id, that is the most recent **parent** commit of the current state of your local repository.

    ```
    git revert --hard <commit id>
    ```

    Example:
    ```
    git reset --hard e02e4d86812457fd9fdd43adae5761f5946fdfb3                                                        master
    HEAD is now at e02e4d8 version bump by bioc core
    ```

    You will then need to push the changes to both, Github and Bioconductor repositories, if you intend to make them permanent, using:

    ```
    git push -f origin
    git push -f upstream
    ```

# Go Nuclear - Delete your local copy and Github repo, because nothing is working.

**CAUTION: These instructions comes with many disadvantages. You have been warned.**

## Steps:

1. Delete your machines local repository, e.g., `rm -rf BiocGenerics`

2. Delete (or rename) your Github repository.

3. Start from [Scenario 1](scenario-1-svn-to-github.md). Make a new copy, and then [Scenario-3](scenario-3-pull-from-gitbioc-push-github.md)

## Costs of going nuclear:

(There will be a holocaust)

1. You will lose all your Github issues

2. You will lose your custom collaborator settings in Github.

3. You have to start from scratch and redo everything related to this transition.
