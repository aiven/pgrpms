#!/bin/bash

os=F-33

# Supported stable PostgreSQL versions:
declare -a pgStableBuilds=("13 12 11 10 9.6 9.5" )
# Supported "testing" versions
declare -a pgTestVersions=("13 12 11" )

packagename=$1
buildVersion=$2

if [ "$packagename" == "" ]
then
	echo "Please specify a package name as a parameter"
	echo "i.e. buildpackage.sh postgresql"
	echo
	exit 1
fi

if [ -x ~/git/pgrpms/rpm/redhat/master/common/$packagename/$os ]
then
echo "Ok, this is a common package, and I am building $packagename for $os for common repo"
sleep 1
       	cd ~/git/pgrpms/rpm/redhat/master/common/$packagename/$os
        time make commonbuild
        cd
	exit 0
fi

if [ -x ~/git/pgrpms/rpm/redhat/master/non-common/$packagename/$os ]
then
echo "Ok, building $packagename on $os against PostgreSQL versions(s)"
sleep 1
	# If there is no specific version specified, go on
	# and run build against each supported version.
	if [ "$buildVersion" == "" ]
	then
		# Extract PostgreSQL versions to packagepgbuildversion variable:
		for packagepgbuildversion in ${pgStableBuilds[@]}
		do
			#Now we need to make sure that the combination is supported:
			if [ -x ~/git/pgrpms/rpm/redhat/$packagepgbuildversion/$packagename/$os ]
	       		then
				cd ~/git/pgrpms/rpm/redhat/$packagepgbuildversion/$packagename/$os
				pgshortversion=`echo $packagepgbuildversion | tr -d . `
				time make build${pgshortversion}
				# If that version is also the supported in the testing versions, then also build that one:
				#if [[ " ${pgTestVersions[@]} " =~ " ${packagepgbuildversion} " ]]
				#then
				#	time make build${packagepgbuildversion}testing
				#fi
			fi
		done
	fi
	if [[ ! -z "$buildVersion" ]]
	then
		if [ -x ~/git/pgrpms/rpm/redhat/$buildVersion/$packagename/$os ]
	      		then
			cd ~/git/pgrpms/rpm/redhat/$buildVersion/$packagename/$os
			pgshortversion=`echo $buildVersion | tr -d . `
			time make build${pgshortversion}
			# If that version is also the supported in the testing versions, then also build that one:
			#if [[ " ${pgTestVersions[@]} " =~ " ${buildVersion} " ]]
			#	then
			#	time make build${buildVersion}testing
			#fi
		fi
	fi
fi
