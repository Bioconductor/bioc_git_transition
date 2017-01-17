#!/bin/bash

set -eo pipefail
IFS=$'\n\t'

if [[ -z $GITHUB_TOKEN ]]; then
  echo "Please set GITHUB_TOKEN to your Github API token before running!"
  exit 1
fi

set -u

parse_last_revision() {
  grep '^r[0-9]' | tail -n 1 | awk '{ print $1 }'
}

svn_url="https://hedgehog.fhcrc.org/bioconductor/trunk/madman/Rpacks"

if [[ -s .last_revision ]]; then
  revision=$(cat .last_revision)

  head_revision=$(svn log -q -v -l 1 $svn_url | parse_last_revision)

  if [ "$revision" == "$head_revision" ]; then
    echo "No changes since last update"
    exit
  fi

  updated=$(svn log -q -v -$revision:HEAD $svn_url)

  # split records on '/', field 5 is the project directory, print only the
  # first time it is seen
  changed_directories=$(echo "$updated" | \
    awk -F"/" '$0 ~ "[AMR] /trunk/madman/Rpacks" && !a[$5]++ { print $5 }')

else
  changed_directories=$(svn list $svn_url | sed 's!/$!!')
  updated=$(svn log -l 1 -q -v $svn_url)
fi

last_revision=$(echo "$updated" | parse_last_revision)

if [[ ! -z $last_revision ]]; then
  echo $last_revision > .last_revision
fi

bioconductor_yaml="https://hedgehog.fhcrc.org/bioconductor/trunk/bioconductor.org/config.yaml"

devel_version=$(svn cat $bioconductor_yaml | \
    awk -F'"' '$0 ~ "^devel_version: " { print $2 }')

mainfest_packages=$(svn cat $svn_url/bioc_${devel_version}.manifest | \
    awk '$0 ~ "^Package: " { print $2 }')

API="https://api.github.com"
TOKEN_STRING="Authorization: token $GITHUB_TOKEN"

# found via curl -H $TOKEN_STRING $API/orgs/bioconductor/teams
#readonly_team_id=1389965
#\"team_id\":\"${readonly_team_id}\"

create_github_repo() {
  project=$1
  echo "Creating new Github Repository for $project"
  # https://developer.github.com/v3/repos/#create
  curl -H "$TOKEN_STRING" --request POST --data \
    "{
      \"name\":\"$project\",
      \"homepage\":\"http://bioconductor.org/packages/devel/bioc/html/${project}.html\",
      \"has_issues\":\"false\",
      \"has_wiki\":\"false\",
      \"has_downloads\":\"false\"
    }" \
  $API/orgs/bioconductor-mirror/repos
  echo "Pushing $project to Github"
  git svn rebase
  git remote add origin git@github.com:bioconductor-mirror/$project.git
  git push -u origin master
}

for project in $changed_directories; do
  if [[ -d $project ]]; then
    echo "Updating $project"
    pushd $project
      if ! $(git remote | grep -q -w origin) ; then
        # no remote set, so create a new repo and set the remote
        create_github_repo $project
      fi
      git svn rebase
      git push origin master
    popd
  else
    if $(echo $mainfest_packages | grep -q -w $project); then
      echo "$project is in manifest, cloning $project"
      git svn clone ${svn_url}/$project $project
      pushd $project
        #bfg --strip-blobs-bigger-than 100M
        create_github_repo $project
      popd
    fi
  fi
done
