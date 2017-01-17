#!/bin/bash

set -euo pipefail
IFS=$'\n\t'

branch=$1
shift

branch_point=$(find_branch_point.sh $branch)
if [[ -z $branch_point ]]; then
    base=$(echo $branch_point | cut -d\ -f2)
    echo $branch_point >> .git/info/grafts
    git filter-branch -- ${base}..$branch
    git push --all --force
else
    echo "No branch point found for $branch!"
fi
