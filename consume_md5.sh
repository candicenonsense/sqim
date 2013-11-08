#!/bin/sh

SRCDIR=$1;

for foo in `find $SRCDIR` ; do 
    echo $foo
    cat $foo | python ./consume_md5.py
done
