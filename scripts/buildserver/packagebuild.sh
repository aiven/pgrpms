#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

# Throw an error if less than two arguments are supplied:
	if [ $# -le 1 ]
	then
		echo
		echo "${red}ERROR:${reset} This script must be run with at least two parameters:"
		echo "       package name, package version"
		echo "       and optional: The actual package name to sign, and also the PostgreSQL version to build against"
		echo
	exit 1
	fi

# The name of the package in the git tree (pgpool-II-41, postgresql-16, etc)
packagename=$1
# Actual package name to sign (postgresql16, pgpool-II, postgis34, etc).
signPackageName=$2
# Optional: The PostgreSQL major version the package will be built against.
# Leave empty to build against all supported PostgreSQL versions.
buildVersion=$3

# Common function to sign the package.
sign_package(){
	# Remove all files with .sig suffix. They are leftovers which appear
	# when signing process is not completed. Signing will be broken when
	# they exist.
	find ~/rpm* -iname "*.sig" -print0 | xargs -0 /bin/rm -v -rf "{}"

	# Find the packages, and sign them. Using an expect script to automate signing process.
	# The first parameter refers to the location of the RPMs:
	for signpackagelist in `find ~/$1* -iname "*$signPackageName*$packageVersion*.rpm"`; do /usr/bin/expect ~/bin/signrpms.expect $signpackagelist; done
}

#################################
#	Build packages		#
#################################

# Packages can be in 3 places: Either in "common", "non-common" or "extras" directories.
# This script currently ignores "non-free" repo.

#################
# Common repo	#
#################

# If the package is in common, then build it, sign it and exit safely:
if [ -x ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os ]
then
echo "${green} Ok, this is a common package, and I am building $packagename for $git_os for common repo.${reset}"
sleep 1
	cd ~/git/pgrpms/rpm/redhat/main/common/$packagename/$git_os
	time make commonbuild
	# Get the package version after building the package so that we get the latest version:
	packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
	cd
	sign_package rpm
	exit 0
fi

#########################
#   Non-Common repo	#
#########################

# If the package is in "non-common", then search the package for all of the values in the
# "pgStableBuilds" parameter (a.k.a. supported versions), and build them. After all of the
# packages are built, sign them.

if [ -x ~/git/pgrpms/rpm/redhat/main/non-common/$packagename/$git_os ]
then
	# Build package against all PostgreSQL versions is 4th parameter is not given:
	if [ "${buildVersion}" == "" ]
	then
		:
	else
		if [[ "${pgStableBuilds[@]}" =~ "${buildVersion}" ]]
		then
			declare -a pgStableBuilds=("${buildVersion}")
		else
			echo "${red}ERROR:${reset} PostgreSQL version ${buildVersion} is not supported."
			exit 1
		fi
	fi

	for packageBuildVersion in ${pgStableBuilds[@]}
	do
		if [ -x ~/git/pgrpms/rpm/redhat/main/non-common/$packagename/$git_os ]
		then
			echo "Ok, building $packagename on $git_os against PostgreSQL $packageBuildVersion"
			sleep 1
			cd ~/git/pgrpms/rpm/redhat/$packageBuildVersion/$packagename/$git_os
			echo "time make build${packageBuildVersion}"
			time make build${packageBuildVersion}
			# Get the package version after building the package so that we get the latest version:
			packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
			cd
		sign_package rpm
		exit 0
		fi
	done
fi # End of non-common build

#################################
#	 Extras repo		#
#################################

# Build the package in the directly if it is in the "extras" repo.
if [ $extrasrepoenabled = 1 ]
then
# First make sure that extras repo is available for this platform:
	if [ -x ~/git/pgrpms/rpm/redhat/main/extras/$packagename/$git_os ]
	then
		echo "Ok, building $packagename on $osshort:"
		sleep 1
		cd ~/git/pgrpms/rpm/redhat/main/extras/$packagename/$git_os
		time make extrasbuild
		packageVersion=`rpmspec --define "pgmajorversion ${pgAlphaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
		cd
		sign_package pgdg
		exit 0
	fi
else
	echo "Extras repo is not enabled on this platform"
	exit 1
fi

#################################
#   Package is not available!	#
#################################

echo "Package does not exist in any of the repos"
exit 0
