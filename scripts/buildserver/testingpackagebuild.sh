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

#################################
#	Build packages		#
#################################

	if [ -x ~/git/pgrpms/rpm/redhat/$pgBetaVersion/$packagename/$git_os ]
	then
		echo "Ok, building $packagename on $osshort:"
		sleep 1
		cd ~/git/pgrpms/rpm/redhat/$pgBetaVersion/$packagename/$git_os
		time make "build${pgBetaVersion}testing"
		packageVersion=`rpmspec --define "pgmajorversion ${pgBetaVersion}" -q --qf "%{name}: %{Version}\n" *.spec |head -n 1 | awk -F ': ' '{print $2}'`
		cd
		sign_package "rpm${pgBetaVersion}testing"
	exit 0
	fi

#################################
#   Package is not available!   #
#################################

echo "Package does not exist in PostgreSQL $pgBetaVersion"
exit 0
