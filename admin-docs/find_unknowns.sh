for pkg in /home/git/repositories/packages/*git;
do {
    cd $pkg
    unknown=`git log --all --oneline --committer="unknown"`
    latest=`git log --all --since="2017-08-15"`
    if [ ! -z "$unknown" ] && [ -z "$latest" ]; then
    	echo `basename $pkg`;
    fi
} done
