# Configuration

## Table of Contents
- [Server Specs](#server)
- [Authentication and Authorization](#auth)
- [Public read-only access via http/s](#http)
    - [Smart http](#smarthttp)
    - [Dumb http](#dumbhttp)
- [Push / Pull access via SSH](#ssh)
    - [svn 'authz' to gitolite 'conf'](#sshgitolite)
    - [SSH locale](#sshlocale)

<a name="server"></a>
## Server Specs

Git is hosted at the AWS-based server, git.bioconductor.org. As of May 2017,
the EC2 instance has 2 vCPUs, 8 GB RAM and 500 GB disk space on the root drive.

<a name="auth"></a>
## Authentication and Authorization

The git repositories are located at /home/git/repositories and can be accessed
via http/s or ssh. Public read-only access is via http and push/pull access
is via ssh.

    Authentication: Verification of user identity with password or key; handled by http/s or ssh.
 
    Authoriziation: Determines which repositories a user can access; handled by gitolite. 

<a name="http"></a>
## Public read-only access via http/s

We are allowing unauthenticated access via http so all incoming http/s requests 
are treated as a single user. There are 2 options for public git access, 'git protocol' 
handled by git-daemon and 'smart http'. The current implementation is 'smart http'.

<a name="smarthttp"></a>
### Smart http

References:

- http://gitolite.com/gitolite/http/
- https://wiki.archlinux.org/index.php/Gitolite#Adding_http.28s.29_access_via_Apache_.28with_basic_authentication.29
- https://git-scm.com/docs/git-http-backend
- https://www.kernel.org/pub/software/scm/git/docs/git-http-backend.html

#### Overview:

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

#### Configure Apache2 for https as described here 

https://github.com/Bioconductor/AWS_management/blob/master/docs/Configure_Apache.md

#### Enable support for Common Gateway Interface (CGI)

Enable the CGI module:

    sudo a2enmod cgi

Modify the Apache config to enable CGI in the /home/git/bin directory:

    <Directory "/home/git/bin">
        Options +ExecCGI
        SetHandler cgi-script
        AllowOverride None
        Require       all granted
    </Directory>

Restart Apache:

    sudo service apache2 restart

#### Enable support for suEXEC 

The suEXEC feature provides users the ability to run Common Gateway Interface
(CGI) and Server Side Interface (SSI) programs under user IDs different from
the user ID of the calling web server. Normally, when a CGI or SSI program
executes, it runs as the same user who is running the web server. This
feature is not enabled by default.

References:
 
- https://httpd.apache.org/docs/2.4/suexec.html
- http://gitolite.com/gitolite/contrib/ssh-and-http/
- https://www.digitalocean.com/community/tutorials/how-to-use-suexec-in-apache-to-run-cgi-scripts-on-an-ubuntu-vps 

Install a modified suEXEC module that allows us to configure the directories
in which it operates.
 
    sudo apt-get install apache2-suexec-custom
    sudo a2enmod suexec

The ScriptAlias directive in the Apache config has (at least) two important
roles.  The first is to map between URLs and filesystem paths. This allows for
content which is not directly under the DocumentRoot to be served as part of
the web document tree. When a user enters the alias location in a browser the
script at the corresponding location will be executed.

The second role is in the git-http-backend script when *GIT_PROJECT_ROOT* 
and *PATH_INFO* variables are concatenated to specify the physical location
of the git repositories on the machine.

*PATH_INFO* is also used by gitolite to look up rules in the gitolite config
files. In packages.conf we specify repositories with a preceding 'packages/'
directory. This means *PATH_INFO* must include the 'packages/' prefix.
For this to happen we must set the alias in ScriptAlias to a location
above packages/; *PATH_INFO* can only 'see' directories below the alias in
ScriptAlias. Because *PATH_INFO* needs to have the 'packages/' prefix,
*GIT_PROJECT_ROOT* cannot.

Using IRanges as an example, we want the concatenated 
*GIT_PROJECT_ROOT/PATH_INFO* to look like this:

    /home/git/repositories/packages/IRanges.git/info/refs

Create a shell script named gitolite-suexec-wrapper.sh inside the
CGI-enabled directory. Point *GIT_PROJECT_ROOT* to the directory above
'packages/':

    #!/bin/bash
    #
    # Suexec wrapper for gitolite-shell
    #
 
    export GIT_PROJECT_ROOT="/home/git/repositories"
    export GITOLITE_HTTP_HOME="/home/git"
    exec ${GITOLITE_HTTP_HOME}/gitolite/src/gitolite-shell
 
Set permissions to 755 on the CGI-enabled /home/git/bin/ directory and 755 on
the /home/git/bin/gitolite-suexec-wrapper.sh wrapper. Both should be owned by
git. 

In the Apache config file, alias the root of git.bioconductor.org (i.e., '/')
to the CGI-enabled directory which now contains the suEXEC wrapper script.

    ScriptAlias / /home/git/bin/gitolite-suexec-wrapper.sh/

Add a line to the Apache config specifying which user should run the 
CGI scripts:
 
    SuexecUserGroup git git

When suEXEC was enabled, a /etc/apache2/suexec/www-data file was created. 
Modify the www-data file to point suEXEC root to the CGI-enabled directory:
 
    /home/git/bin/

#### Anonymous ('nobody') user

Apache passes an anonyomous user to gitolite who assigns the user name 'nobody'
in the gitolite.rc file. Confirm this line is uncommented:
 
    # rc variables used by various features
    HTTP_ANON_USER      =>  'nobody',

Give user 'nobody' read access to repositories in gitolite.conf or
packages.conf by specifying
 
    R = nobody
 
#### git-http-backend

This is the server-side implementation of git over http. It's a CGI program 
that serves the contents of a git repository to git clients. The script verifies 
the repos being accessed have magic file "git-daemon-export-ok" unless 
*GIT_HTTP_EXPORT_ALL* is set.

Add this line to the Apache config:
 
    SetEnv GIT_HTTP_EXPORT_ALL
 
Restart Apache:
 
    sudo service apache2 restart

<a name="dumbhttp"></a>
### Dumb http

(Keep for historical reference)

Because we do not authenticate users via http we could use the
out-of-the-box Apache configuration to limit what users can see.

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

<a name="ssh"></a>
## Push / pull access via SSH 

<a name="sshgitolite"></a>
### svn 'authz' to gitolite 'conf'

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

<a name="sshlocale"></a>
### SSH locale 

When a user ran 'git pull' with a non-C and non-US locale, the remote
server (i.e., git.bioconductor.org) issued a perl warning that 
setting the locale failed and the fallback locale ("en_US.UTF-8") would
be used. See this issue for full details:

https://github.com/Bioconductor/bioc_git_transition/issues/34

To prevent this, the git server was modified to prevent clients
from propagating their locale variables via SSH. 

There are 2 SSH config files, one is for clients connecting to the host 
(/etc/ssh/ssh_config) and another for the ssh daemon running on the host
(/etc/ssh/sshd_config). 

Modify the config file for the daemon, /etc/ssh/sshd_confg, by commenting out 
this line

    AcceptEnv LANG LC_*

then restart the service

    sudo service sshd restart
