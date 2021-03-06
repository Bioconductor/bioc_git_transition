# Frequently asked questions

1. I'm a developer for Bioconductor, my package `ExamplePackage` is on the new server https://git.bioconductor.org. What do I do next?

    Take a look at [Scenario 1: Create GitHub repository for existing Bioconductor repository][]. This will give you the information needed.

2. I have a GitHub repository already set up for my bioconductor package at `www.github.com/<developer>/<ExamplePackage>` , how do I link my repository in GitHub and https://git.bioconductor.org ?

    Take a look at [Scenario 1: Create GitHub repository for existing Bioconductor repository][]. Step 4 gives you information on how to add the remote and link both GitHub and Bioconductor repositories.

3. I'm unable to `push` or `merge`  my updates from my GitHub repository to my bioconductor package on `git@git.bioconductor.org` , how do I go about this?

    If you are unable to `push` or `merge` to either your GitHub account or Bioconductor repository, it means you do not have the correct access rights. If you are a developer for Bioconductor, you will need to submit your SSH public key to https://goo.gl/forms/eg36vcBkIUjfZfLe2.

    You should also make sure to check that your public key is set up correctly on GitHub. Follow [Adding a new SSH key to your GitHub account][].

4. I'm not sure how to fetch the updates from `git.bioconductor.org` with regards to my package, how do I do this?

    Take a look at [Scenario 3: Get updates from Bioconductor and update GitHub][]. This will give you the information needed.

5. I'm just a package user, do I need to do any of this?

    As a package user, you do not need any of these **developer** related documentation. Although, it is a good primer if you want to be a contributor to Bioconductor.

    You can also open [Pull requests][], and [issues][] on the Bioconductor packages you use, **if** they have a GitHub repository.

6. I'm new to git and GitHub, where should I learn?

    There are many resources where you can learn about git and GitHub.

    * [git-and-github-learning-resources][]
    * [git-scm][]
    * [Guides][]

7. SVN was working well for me, why do we have to move?

    We believe that git, and social coding are the way forward for open source projects. They enable participation from a larger audience. Switching from SVN allows us to better manage the packages being contributed to Bioconductor.

8. I'm a Bioconductor package maintainer, but I don't have access to the Bioconductor server where my packages are being maintained. How do I gain access?

    Please submit your ssh public key or github ID to https://goo.gl/forms/eg36vcBkIUjfZfLe2. Your key will be added to your our server and you will get read+ write access to your package.

    All developers of Bioconductor packages are required to do this, if they don't already have access. Please identify which packages you need read/write access to in the email.

9. What is the relationship between the `origin` and `upstream` remote?

    In `git` lingo **origin** is just the default name for a remote from which a repository was originally cloned. It might equally have been called by another name. We recommend that **origin** be set to the developers GitHub repository.

    Similarly, **upstream** is the name for a remote which is hosted on the Bioconductor server.

    It is important that all the changes/updates you have on your **origin** are equal to **upstream**, in other words, you want these two remotes to be in sync.

    Follow [Scenario 9: Sync existing GitHub and Bioconductor repositories][] for details on how to achieve this.

    Image explaining GitHub and Bioconductor relationship for a developer

    ![](images/github-bioc-relationship.png)

10. Can I have more than one upstream remote, if yes, is this recommended?

    You can have as many remotes as you please. But you can have only one remote with the name **upstream**. We recommend having the remote `origin` set to GitHub, and `upstream` set to the Bioconductor git server to avoid confusion.

11. Common names used in the scenario's

    `developer`: This should be your GitHub username, eg: mine is `nturaga`.

    `BiocGenerics`: This is being used as an example to demonstrate git commands.

    `ExamplePackage`: This is being used a place holder for a package name.

    SVN `trunk` and git `master` branch are now the development branches.

13. I'm a Bioconductor developer only on the Bioconductor server. I do not have/want a GitHub account. What should I do?

    You do not have to get a Github account if you do not want one. But it is a really good idea,
    to maintain your package publicly and interact with the community via the social coding features
    available in Github.

    We highlight this in [Scenario-11: Maintain-without-github][]


## More questions?

If you have additional questions which are not answered here already, please send an email to bioc-devel@bioconductor.org.

## Helpful links:

[Scenario 1: Create GitHub repository for existing Bioconductor repository](scenario-1-svn-to-github.md)

[Scenario 2: Push to both GitHub and Bioconductor repositories](scenario-2-push-to-gitub-gitbioc.md)

[Scenario 3: Get updates from Bioconductor and update GitHub](scenario-3-pull-from-gitbioc-push-github.md)

[Scenario 4: Push updates to release branch (RELEASE_X_Y)](scenario-1-svn-to-github.md)

[Scenario 5: Resolve conflicts](scenario-5-resolve-conflicts.md)

[Scenario 6: Abandon changes and start fresh](scenario-6-abandon-changes.md)

[Scenario 7: Add collaborators and leverage GitHub features](scenario-7-add-collaborators.md)

[Scenario 8: New package workflow](scenario-8-new-package-workflow.md)

[Scenario 9: Sync existing GitHub and Bioconductor repositories](scenario-9-sync-existing-github-gitbioc.md)

[Adding a new SSH key to your GitHub account](https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/)

[Create a pull request on GitHub](https://help.github.com/articles/creating-a-pull-request/)

[Create an issue on GitHub](https://help.github.com/articles/creating-an-issue/)

[Git and GitHub learning resources](https://help.github.com/articles/git-and-github-learning-resources/)

[git-scm manual](https://git-scm.com/)

[GitHub Guides](https://guides.github.com/)

********

[Scenario 1: Create GitHub repository for existing Bioconductor repository]: scenario-1-svn-to-github.md

[Scenario 2: Push to both GitHub and Bioconductor repositories]: scenario-2-push-to-github-gitbioc.md

[Scenario 3: Get updates from Bioconductor and update GitHub]: scenario-3-pull-from-gitbioc-push-github.md

[Scenario 4: Push updates to release branch (RELEASE_X_Y)]: scenario-1-svn-to-github.md

[Scenario 5: Resolve conflicts]: scenario-5-resolve-conflicts.md

[Scenario 6: Abandon changes and start fresh]: scenario-6-abandon-changes.md

[Scenario 7: Add collaborators and leverage GitHub features]: scenario-7-add-collaborators.md

[Scenario 8: New package workflow]: scenario-8-new-package-workflow.md

[Scenario 9: Sync existing GitHub and Bioconductor repositories]: scenario-9-sync-existing-github-gitbioc.md

[Scenario-11: Maintain-without-github]: scenario-11-maintain-without-github.md

[Adding a new SSH key to your GitHub account]: https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/

[Pull requests]: https://help.github.com/articles/creating-a-pull-request/

[issues]: https://help.github.com/articles/creating-an-issue/

[git-and-github-learning-resources]: https://help.github.com/articles/git-and-github-learning-resources/

[git-scm]: https://git-scm.com/

[Guides]: https://guides.github.com/
