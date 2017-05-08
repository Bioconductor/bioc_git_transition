# Scenario 7: Add collaborators and leverage Github features


## Maintaining Collaborators on github

1. [Adding a new collaborator][]

2. [Removing collaborator][]

## Pull requests on Github

1. [Merging a pull request][]

## Push to Bioconductor repository

Once you have accepted pull requests from your package community on Github, you can push these changes to Bioconductor.

1. Make sure that you are on the branch to which the changes were applied, for example `master`.

   ```
   git checkout master
   ```

1. Pull the Github changes to your local repository.

    ```
    git pull
    ```

1. Push your local repository to the upstream Bioconductor repository.

    ```
    git push upstream master
    ```
    
If you want to update a release branch, simply replace `master` with name of the release branch, e.g.: `RELEASE_3_5`.

[Adding a new collaborator]: https://help.github.com/articles/inviting-collaborators-to-a-personal-repository/

[Removing collaborator]: https://help.github.com/articles/removing-a-collaborator-from-a-personal-repository/

[Merging a pull request]: https://help.github.com/articles/merging-a-pull-request/
