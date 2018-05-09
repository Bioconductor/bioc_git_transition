# INTEGRATION TEST


test_repo() {
    ## Create bare repo
    gittestpath=/tmp/test_bad_version_numbers.git
    hooks=/Users/ni41435_ca/Documents/bioc_git_transition/hooks/repo-specific
    gittestrepopath=/tmp/test_bad_version_numbers

    ## Clean up
    if [ -d "$gittestpath" ]; then
	rm -rf $gittestpath
    fi

    if [ -d "$gittestrepopath" ]; then
	rm -rf $gittestrepopath
    fi

    mkdir $gittestpath
    cd $gittestpath

    ## Make bare clone
    git init --bare

    ## Copy hooks
    cp $hooks/prevent_bad_version_numbers.py $hooks/prevent_duplicate_commits.py $hooks/prevent_large_files.py hooks/
    cp $hooks/pre-receive-hook hooks/pre-receive

    ## Make clone of bare repo
    cd /tmp
    git clone $gittestpath
}

## add tests here
###################################################################
## TEST 1: Check the files between multiple commits in the git diff

## Initiate test repo
test_repo
cd $gittestrepopath

## 1. Add DESCRIPTION file
cp /tmp/DESCRIPTION .
git add DESCRIPTION
git commit -m "Add DESCRIPTION file"

## 2. Add dummy file

touch dummy1
git add dummy1
git commit -m "Add dummy1 file"

## 2. Add dummy file 2

touch dummy2
git add dummy2
git commit -m "Add dummy2 file"

## Git push to test

git push

###################################################################

## Test 2: Check bad version bumps

## Initiate test repo
test_repo
cd $gittestrepopath

## 1. Add dummy file

touch dummy1
git add dummy1
git commit -m "Add dummy1 file"

## 2. Add DESCRIPTION file
cp /tmp/DESCRIPTION .
git add DESCRIPTION
git commit -m "Add DESCRIPTION file"

## 3. Add dummy file 2

touch dummy2
git add dummy2
git commit -m "Add dummy2 file"

## 4. Add dummy file 3

touch dummy3
git add dummy3
git commit -m "Add dummy2 file"

## Git push to test

git push
