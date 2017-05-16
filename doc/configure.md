# Server

Git is hosted at the AWS-based server, git.bioconductor.org. As of May 2017,
the EC2 instance has 2 vCPUs, 8 GB RAM and 500 GB disk space on the root drive.

# Authentication and Authorization

The git repositories are located at /home/git/repositories and can be accessed
via http/s or ssh.

    Authentication: Verification of user identify with a password or key; handled by http/s or ssh.
                
    Authoriziation: Determines which repositories can a use access; handled by gitolite. 

## Public read-only access via http/s

We are allowing unauthenticated access via http so all incoming http/s requests 
are treated as a single user. There are 2 options for public git access, 'git protocol' 
handled by git-daemon and 'smart http'. The current implementation is 'smart http'.

### Smart http

References:

- http://gitolite.com/gitolite/http/
- https://wiki.archlinux.org/index.php/Gitolite#Adding_http.28s.29_access_via_Apache_.28with_basic_authentication.29
- https://git-scm.com/docs/git-http-backend
- https://www.kernel.org/pub/software/scm/git/docs/git-http-backend.html

Overview:

apache -> gitolite -> git-http-backend

apache
- redirects incoming traffic to CGI-enabled location
- hands off to suEXEC
- suEXEC (as user git) runs CGI script that wraps gitolite executible

gitolite
- reads gitolite.rc
- checks user permissions in gitolite.conf and packages.conf
- hands off to git-http-backend

git-http-backend
- GET request (does repo exist)
- POST request (serve up the repo)

1) Configure Apache2 for https as described here 

https://github.com/Bioconductor/AWS_management/blob/master/docs/Configure_Apache_HOWTO.md

2) Enable support for Common Gateway Interface (CGI)

    ````
    sudo a2enmod cgi
    sudo service apache2 restart
    ````
    
    The Alias and ScriptAlias directives are used to map between URLs and
filesystem paths. This allows for content which is not directly under the
DocumentRoot to be served as part of the web document tree.  The ScriptAlias
directive has the additional effect of marking the target directory as
containing only CGI scripts.

- Apache2 config modifications:

    ````
    ScriptAlias /packages/ /home/git/bin/gitolite-suexec-wrapper.sh/
    <Directory "/home/git/bin">
        Options +ExecCGI
        SetHandler cgi-script
        AllowOverride None
        Require       all granted
    </Directory>
    ````
    
3) Enable support for suEXEC 

  Instructions collated from multiple sources: 
    https://httpd.apache.org/docs/2.4/suexec.html
    http://gitolite.com/gitolite/contrib/ssh-and-http/
    https://www.digitalocean.com/community/tutorials/how-to-use-suexec-in-apache-to-run-cgi-scripts-on-an-ubuntu-vps 

    The suEXEC feature provides users the ability to run Common Gateway Interface
  (CGI) and Server Side Interface (SSI) programs under user IDs different from
  the user ID of the calling web server. Normally, when a CGI or SSI program
  executes, it runs as the same user who is running the web server. This
  feature is not enabled by default.

- Install a modified suEXEC module that allows us to configure the directories
  in which it operates. Normally, this would not be configurable without
  recompiling from source. 
    ```
    sudo apt-get install apache2-suexec-custom
    sudo a2enmod suexec
    ```
    
- Add a line to the Apache2 config specifying which user should
  run the CGI scripts:
    ```
    SuexecUserGroup git git
    ```
    
- Modify /etc/apache2/suexec/www-data to point the suEXEC root to the 
  CGI-enabled directory specified in the Apache2 config file.
    ```
    /home/git/bin/
    ```
    
- Modify the gitolite-suexec-wrapper.sh:
    ```
    export GIT_PROJECT_ROOT="/home/git/repositories/packages"
    export GITOLITE_HTTP_HOME="/home/git"
    exec ${GITOLITE_HTTP_HOME}/gitolite/src/gitolite-shell
    ```
    
- Set permissions to 755 on both the CGI-enabled /home/git/bin/ directory
  and the suEXEC wrapper for the gitolite shell,
  /home/git/bin/gitolite-suexec-wrapper.sh. Both should be owned by git:git. 

- Restart Apache2:
    ```
    sudo service apache2 restart
    ```
    
- Add a whoami test script (test.cgi) to the CGI-enabled path in 
  ScriptAlias above. Confirm the git user is the one running 
  the script by pasting
    ```
    https://git.bioconductor.org/packages/test.cgi
    ```
    
  in a browser.

4) Anonymous ('nobody') user

- Apache passes an anonomous user to gitolite who assigns the user name
  'nobody' in the gitolite.rc file. Confirm this line is uncommented:
    ```
    # rc variables used by various features
    HTTP_ANON_USER      =>  'nobody',
    ```
    
- Give user 'nobody' read access to repositories in gitolite.conf or 
  packages.conf by specifying
    ```
    R = nobody
    ```
    
5) git-http-backend

  This is the server-side implementation of git over http. It's a CGI program 
that serves the contents of a git repository to git clients. The script verifies 
the repos being accessed have magic file "git-daemon-export-ok" unless 
GIT_HTTP_EXPORT_ALL is set.

- Add this line to the Apache2 config:
    ```
    SetEnv GIT_HTTP_EXPORT_ALL
    ```
    
### Non-gitolite (dumb) http configuration

(Keep for historical reference)

Because we do not authenticate users via http we could use the
out-of-the-box Apache2 configuration to limit what users can see.

- Configure Apache as described here https://github.com/Bioconductor/AWS_management/blob/master/docs/Configure_Apache.md.
- Add the git user, www-data, to the git group.
- All directories under /home/git/repositories should have the following permissions: 
  user: read, write, execute 
  group: read, execute 
  other: none 
- All files under /home/git/repositories should have the following permissions: 
  user: read, write 
  group: read 
  other: none 
- Testing: 
  -- Paste https://git.bioconductor.org/packages/ in a browser and confirm all packages are visible. 
  -- Download a package with `git clone https://git.bioconductor.org/packages/BiocGenerics.git`

## Push / pull access via ssh

# svn 'authz' to gitolite 'conf'

The gitolite configuration involves

- ssh key files need to be named after svn user accounts (the end user
  does not need to know about this)

- uncomment `'continuation-lines'` to allow for `\` continuation lines
  (aesthetically useful for @bioconductor-write0, for instance).

- The following repositories have svn permissions but do not exist in
  Nitesh's clone, so gitolite created empty repositories:
  AffyTiling.git Agi4x44PreProcess.git BeadExplorer.git
  COPDSexualDimorphism.git ChromoViz.git DASiR.git DAVIDQuery.git
  DNaseR.git EpiCluster.git GA4GHclient.git GGexplorer.git
  GeneGroupAnalysis.git GeneR.git GeneRfold.git GeneSpring.git
  GeneTS.git GeneticsBase.git GenoView.git HTSeqGenieBase.git
  MMDiff.git RMAGEML.git RMAPPER.git RNASeqGenie.git RTools4TB.git
  RWebServices.git Rintact.git Rolexa.git STROMA4.git SemSim.git
  Seqnames.git SomatiCA.git SpliceGraph.git TimerQuant.git
  arrayMagic.git arrayQCplot.git asmn.git basePLM.git bim.git
  biocDatasets.git cellHTS.git cosmo.git cosmoGUI.git cydar.git
  exonmap.git fbat.git flowFlowJo.git flowPhyto.git flowTime.git
  gene2pathway.git gmapR2.git goCluster.git hdf5.git iFlow.git
  inSilicoDb.git inSilicoMerging.git jmosaics.git maDB.git
  makePlatformDesign.git maskBad.git metaX.git mmgmos.git mtbls2.git
  neaGUI.git netReg.git pairseqsim.git pgUtils.git prism.git spade.git
  stam.git virtualArray.git wiggleplotr.git xcmsGUI.git xmapcore.git

