#!/bin/bash

#################################
# Script to build packages in	#
# the PostgreSQL RPM repository.#
# https://yum.postgresql.org    #
#                               #
# Devrim Gunduz                 #
# devrim@gunduz.org             #
#################################


# OS version. Possible values are:
# EL-6 EL-7 EL-8 F-32 F-33 SLES-12 SLES-15, etc.
os=F-33

# Supported stable PostgreSQL versions:
declare -a pgStableBuilds=("15 14 13 12 11" )
# Supported "testing" versions
declare -a pgTestVersions=("15 14" )

#Color schemes
red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`

# if less than two arguments supplied, throw error:
	if [  $# -le 2 ]
	then
		echo
		echo "${red}ERROR:${reset} This script must be run with at least two parameters:"
		echo "       package name, package version"
		echo "       and optional: The actual package name to sign, and also the PostgreSQL version to build against"
		echo
	exit 1
	fi

# The name of the package in the git tree (pgpool-II-41, postgresql-14, etc)
packagename=$1
#  Package version (Version: field in the spec file)
packageVersion=$2
# Actual package name to sign (pgpool-II, postgis, etc).
signPackageName=$3
# The PostgreSQL version the package will be built. Leave empty for all
# PG versions.
buildVersion=$4


# Common function to sign the package.
sign_package(){
	# Remove all files with .sig suffix. They are leftovers  which appear
	# when signing process is not completed. Signing will be broken when
	# they exist.
	find ~/rpm* -iname "*.sig" -type -f -print0 | xargs -0 /bin/rm -v -rf "{}"

	# Find the packages, and sign them. In the future, a better approach would be getting
	# the version number from the spec file, so that we don't go over the older packages that
	# are already signed. This is not a problem for now, we just lose time. Older packages
	# won't be signed again anyway.
	# Using an expect script to automate signing process.
	for signpackagelist in `find ~/rpm* -iname "$signPackageName*$packageVersion*.rpm"`; do /usr/bin/expect ~/bin/signrpms.expect $signpackagelist; done
}


# Package builds. The packages can be in 2 places: Either in "common", or "non-common" directories.

# If the package is in common, then build it, sign it and exit safely:
if [ -x ~/git/pgrpms/rpm/redhat/master/common/$packagename/$os ]
then
echo "${green} Ok, this is a common package, and I am building $packagename for $os for common repo.${reset}"
sleep 1
       	cd ~/git/pgrpms/rpm/redhat/master/common/$packagename/$os
        time make commonbuild
        cd
	sign_package
	exit 0
fi

# If the package is in "non-common", then search the package for all of the values in the
# "pgStableBuilds" parameter (a.k.a. supported versions), and build them. After all of the
# packages are built, sign them:
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
				# Build targets in the Makefiles don't have dot in them, so:
				pgshortversion=`echo $packagepgbuildversion | tr -d . `

				time make build${pgshortversion}

				# DISABLED: This code is there for historical reasons. We already changed the way how testing repo works:
				# If that version is also the supported in the testing versions, then also build that one:
				#if [[ " ${pgTestVersions[@]} " =~ " ${packagepgbuildversion} " ]]
				#then
				#	time make build${packagepgbuildversion}testing
				#fi
			fi
		done
		sign_package
	fi

	# A specific version is not given, so build for all supported releases (for the package), and sign them:
	if [[ ! -z "$buildVersion" ]]
	then
		if [ -x ~/git/pgrpms/rpm/redhat/$buildVersion/$packagename/$os ]
	      		then
			cd ~/git/pgrpms/rpm/redhat/$buildVersion/$packagename/$os
			# Build targets in the Makefiles don't have dot in them, so:
			pgshortversion=`echo $buildVersion | tr -d . `

			time make build${pgshortversion}
			sign_package

			# DISABLED: This code is there for historical reasons. We already changed the way how testing repo works:
			# If that version is also the supported in the testing versions, then also build that one:
			#if [[ " ${pgTestVersions[@]} " =~ " ${buildVersion} " ]]
			#	then
			#	time make build${buildVersion}testing
			#fi
		fi
	fi
fi
