#!/bin/bash

if [ -z $LINUX_DIR ]
then
    echo "Variable LINUX_DIR is not set. You can fix it by adding line"
    echo ""
    echo "  export LINUX_DIR=<your linux git repository path>"
    echo ""
    echo "to ~/.bashrc or writing it in terminal."
    exit
fi

if [ -z $2 ]
then
    echo "Usage: $0 <destination directory> <number of versions> [<number of commits between master and the earliest version>]"
    exit
fi

VERSIONS=$2

if [ $VERSIONS -le 1 ]
then
    echo "Number of versions must be greater than or equal to 2."
    exit
fi

DESTINATION=$(readlink -m $1)
mkdir -p $DESTINATION

COMMITS=${3:-40000}

cd $LINUX_DIR

for i in `seq 1 $VERSIONS`
do
    git checkout master~$(( COMMITS*(VERSIONS-i)/(VERSIONS-1) )) &> /dev/null
    FILES=`ls -A | egrep -v '^.git$'` 

    mkdir $DESTINATION/v$i
    cp -R $FILES $DESTINATION/v$i
done
git checkout master &> /dev/null
