#!/bin/bash

# directory with linux git repository
LINUX_DIR=~/code/zpp/linux/linux

if [ $LINUX_DIR == "" ]
then
    echo "Error: variable LINUX_DIR not set."
    exit
fi

if [ "$2" == "" ]
then
    echo "Usage: $0 <destination directory> <number of versions>"
    exit
fi

DESTINATION=`mkdir "$1" 2> /dev/null; cd "$1"; pwd`
VERSIONS=$2
CUR_DIR=`pwd`
COMMITS=40000

cd $LINUX_DIR

for i in `seq 1 $VERSIONS`
do
    git checkout master~$(( COMMITS*(VERSIONS-i)/(VERSIONS-1) )) 2> /dev/null
    FILES=`ls -A | egrep -v '^.git$'` 

    mkdir $DESTINATION/v$i
    cp -R $FILES $DESTINATION/v$i
done

git checkout master 2> /dev/null
cd $CUR_DIR
