#!/bin/bash

# By: Martin Morgan
# Date: 19 October, 2016
# 
# Purpose: visit each directory and attempt to sync master with svn
# 
# Usage: mirror/update_all_repos.sh */

set -eo pipefail
IFS=$'\n\t'

if [[ -z $GITHUB_TOKEN ]]; then
  echo "Please set GITHUB_TOKEN to your Github API token before running!"
  exit 1
fi

set -u

basewd=`pwd`

for package in $@; do
    path="$basewd/$package"
    cd $path
    echo `pwd`
    git checkout master || continue
    git pull  || continue
    git svn rebase || {
        echo "fatal: git svn rebase"
        continue
    }
    git push -u origin master || continue
done

exit
