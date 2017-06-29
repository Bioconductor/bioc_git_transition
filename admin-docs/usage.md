# Usage

- Clone `git clone git@github.com:Bioconductor/bioc_git_transition`
- **IMPORTANT** Set SVN username / password set, e.g., readonly / readonly
- Folders will be created

    - `~/temp_packages`: git cloned from SVN; all commit histories added
    - `~/packages`: git bare repos get stored here

# SVN update

- Need local svn dump (e.g., `cp -r ~git/hedgehog.fhcrc.org ~/`)
- `git checkout svn_update`
- Update settings.ini

    ```
    [SVN]
    remote_svn_server: https://hedgehog.fhcrc.org/bioconductor
    svn_root: file:///hedgehog.fhcrc.org/bioconductor
    update_file: update.svn
    users_db: /home/mtmorgan/bioc_git_transition/users_db.txt
    transition_log:	/home/mtmorgan/bioc_git_transition/transition.log
    svn_dump_log: /home/mtmorgan/bioc_git_transition/svn_dump.log
    ```

- Start a tmux session (long-running job)
  - exit with `^B d`; `tmux a` to attach same session
- `~/bioc_git_transition$ python svn_dump_update.py &`

- Success
  - `svn_dump.log` concludes w/ 'Finished dump update'
  - Also: `$ svn info
      file:///home/mtmorgan/hedgehog.fhcrc.org/bioconductor/` revision
      should be current

# Clone to bare

- Update settings.ini

    ```
    [GitBioconductor]
    # This is the git-svn clone
    bioc_git_repo: /home/mtmorgan/temp_packages
    remote_url: packages/
    # This needs to change (Destination Dir)
    bare_git_repo: /home/mtmorgan/packages/
    ```

- Start a tmux session
- `python run_transition.py > run_transition.out 2> run_transition.err &`

# 'Production'

## Version bump

```
[GitEditBioconductor]
# Make changes and push to bare_git_repo
edit_repo: /home/mtmorgan/temp/edit_repo
server: git@git.bioconductor.org:
ssh_server: git@git.bioconductor.org/packages
https_server: https://git.bioconductor.org/packages
```
