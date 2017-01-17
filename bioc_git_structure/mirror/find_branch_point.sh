#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

branch_sha1 () {
  local branch=$1
  local from=${2:-master}

  local branch_root=$(git log --format='%H' $branch | tail -n 1)

  local svn_url=$(git config svn-remote.${branch}.url)

  local from_revision=$(svn log --stop-on-copy --verbose "$svn_url" | perl -ne 'if (/from [^:]+:([0-9]+)/) { print $1,"\n" }')

  for commit in $(git svn log --oneline --show-commit $from); do
    local commit_info=($(echo $commit | perl -ne 'print join("\t", split /[ |]+/)'))
    local revision=${commit_info[0]}
    local sha1=$(git log -n 1 --format='%H' ${commit_info[1]})
    if [[ ${revision:1} -lt $from_revision ]]; then
      echo $branch_root $sha1
      return 0
    fi
  done
  return 1
}

echo $(branch_sha1 $1)
