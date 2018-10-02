Git hooks for Bioconductor
=========================

This document describes the hooks on the Bioconductor git server.There
are two types of hooks on the Bioconductor git server,

1. Pre-receive hooks : These hooks intercept the push from the author
   of the package and show an error if their commit does not pass the
   "check" the hook performs. 
   
   There are three pre-recieve hooks on the system,
   
   1. Prevent Large files: This hook prevents large files from
          entering the git repository, where each file can have a max
          size of 5MB.
	   
   1. Prevent bad version numbers: This hook prevents bad version
          numbers according to the documentation given in
          http://bioconductor.org/developers/how-to/version-numbering/.
	   
   1. Prevent duplicate commits: This hook checks the last 50 commits
          to see if there are any duplicate commits.

1. Post-receive hooks: This hook takes the commit after it is accepted
   into the Bioconductor git server, and processes it for other needs.
   
   There is currently only one post-receive hook on the system,
   
   1. RSS feed: Once a commit is accepted into the system, the
          post-receive hook takes the commit information, eg: the
          message, the date and the author information, and publishes
          it to the GIT log on the Bioconductor website. It also makes
          builds the RSS file(xml format) for the feed.


The hooks are applied differently to both software and
workflow/data-experiment packages.

Hooks applied to Software packages:
	
* Prevent large files
		
* Prevent bad version numbers
	
* Prevent duplicate commits 
	
* RSS feed 	
	
Hooks applied to Workflow/Data-Experiment packages:

* Prevent bad version numbers

* Prevent duplicate commits 
		
* RSS feed
	
	
	
