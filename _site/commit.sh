#!/bin/sh

#if [[ "$ret" -ne "0" ]]
#then
#   ifup eth0
#fi

dir=`dirname $0`

cd $dir

git add -A
git commit -a -m "commit"
git push origin master

cd -

