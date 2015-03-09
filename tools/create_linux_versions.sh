#!/bin/bash

# directory with linux git repository
LINUX_DIR=

if [ -z $LINUX_DIR ]
then
    echo "Error: variable LINUX_DIR not set."
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

DESTINATION=`mkdir -p "$1"; cd "$1"; pwd`
COMMITS=${3:-40000}

for i in `seq 1 $VERSIONS`
do
    git checkout master~$(( COMMITS*(VERSIONS-i)/(VERSIONS-1) )) 2> /dev/null
    FILES=`ls -A | egrep -v '^.git$'` 

    mkdir $DESTINATION/v$i
    cp -R $FILES $DESTINATION/v$i
done

git checkout master 2> /dev/null
