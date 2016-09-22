#!/bin/bash

pgrelease=9.6
os=EL-7 #options: EL-7, EL-6, F-24, F-23
package=$1

if [ "$1" == "" ]
then
        echo "Please specify a package name as a parameter"
        echo "i.e. buildpackage.sh postgresql"
        echo
        exit 1
fi

if [ ! -x ~/git/pgrpms/rpm/redhat/$pgrelease/$package/$os ]
then
        echo "$package name is not valid package name or does not exist for $os"
        echo
        echo "Please specify a valid package name"
        exit 1
fi

echo
echo "Ok, building $package for $os"
sleep 1

cd ~/git/pgrpms/rpm/redhat/$pgrelease/$package/$os
time make build

cd
