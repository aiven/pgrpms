#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Make sure only postgres user can run this script:
if [ "$(id -u)" != "26" ]; then
	clear
	echo
	echo "${red}ERROR:${reset} This script must be run as postgres user" 1>&2
	echo
	exit 1
fi

# Color schemes
red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`

export os=rhel-9		# rhel-9, sles-15, fedora-40
export osarch=x86_64		# x86_64, aarch64, ppc64le
export osdistro=redhat		# fedora, redhat, suse
export git_os=EL-9		# EL-9, F-40, SLES-15
export osshort=rhel9		# Will be used for extras builds for now
export ossysupdates=rocky9	# centos8 rocky9 . Used for the sysupdates repo.
export extrasrepoenabled=1	# 1 or 0. Currently for RHEL 9, 8 and SLES 15

export GPG_TTY=$(tty)
export GPG_PASSWORD=foobar

declare -a pgStableBuilds=("16 15 14 13 12" )
declare -a pgTestBuilds=("17 16 15 14 13" )
declare -a pgBetaVersion=("17" )
declare -a pgAlphaVersion=("18" )

