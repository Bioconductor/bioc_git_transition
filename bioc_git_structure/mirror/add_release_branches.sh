#!/bin/bash

set -eo pipefail
IFS=$'\n\t'

retry () {
 local n=0
 until [ $n -ge 5 ]
 do
   $@ && break  # substitute your command here
   echo "Retrying $@"
   n=$[$n+1]
   sleep 1
 done
}

if [[ -z $GITHUB_TOKEN ]]; then
  echo "Please set GITHUB_TOKEN to your Github API token before running!"
  exit 1
fi

set -u

svn_url="https://hedgehog.fhcrc.org/bioconductor"

branches=$1
shift

for project in $@; do
  pushd $project
  for branch in $branches; do
    nice_branch=$(echo $branch | awk -F_ '{print "release-" $2 "." $3}')
    branch_url=$svn_url/branches/$branch/madman/Rpacks/$project
    if svn list --depth empty $branch_url; then
      if [[ -z $(git branch --list $nice_branch) ]]; then
        git config --add svn-remote.$nice_branch.url $branch_url
        git config --add svn-remote.$nice_branch.fetch :refs/remotes/git-svn-$nice_branch
        retry git svn fetch $nice_branch
        git branch $nice_branch git-svn-$nice_branch
        git checkout $nice_branch
        retry git svn rebase
        retry git push origin $nice_branch
        git checkout master
      fi
        #git checkout $nice_branch
        #retry git svn rebase
        #retry git push origin $nice_branch
        #git checkout master
    fi
  done
  popd
done
