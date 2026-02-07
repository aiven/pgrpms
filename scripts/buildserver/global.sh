#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2026		#
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

export osmajorversion=10	# Major version: 10, 9, 15, 43
export os=rhel-${osmajorversion}		# rhel-9, sles-15, fedora-43
export osminversion=1		# Will be used to support multiple OS minor versions like SLES 15.7, RHEL 10.1
export osislatest=0		# Is this the latest minor version of the OS or not? 1 or 0
export osarch=x86_64		# x86_64, aarch64, ppc64le
export osdistro=redhat		# fedora, redhat, suse
export git_os=EL-${osmajorversion}		# EL-9, F-43, SLES-15
export extrasrepoenabled=1	# 1 or 0. Currently for RHEL and SLES.

export GPG_TTY=$(tty)
export GPG_PASSWORD=foobar

export AWS_PAGER=""
export awssrpmurl=s3://dnf-srpms.postgresql.org20250313103537584600000001		# s3://dnf-srpms.postgresql.org20250313103537584600000001 or s3://zypp-srpms.postgresql.org20250618120322107700000001
export awsdebuginfourl=s3://dnf-debuginfo.postgresql.org20250312201116649700000001	# s3://dnf-debuginfo.postgresql.org20250312201116649700000001 or s3://zypp-debuginfo.postgresql.org20250312201116651400000002

export CF_DEBUG_DISTRO_ID=XXXXXXXXXXXXXXXXXX
export CF_SRPM_DISTRO_ID=XXXXXXXXXXXXXXXXXX

declare -a pgStableBuilds=("18 17 16 15 14" )
declare -a pgTestBuilds=("18 17 16 15 14" )
declare -a pgBetaVersion=
declare -a pgAlphaVersion=19

# Common function to sign the package.
sign_package(){
	# Remove all files with .sig suffix. They are leftovers which appear
	# when signing process is not completed. Signing will be broken when
	# they exist.
	find ~/rpm* pgdg* -iname "*.sig" -print0 | xargs -0 /bin/rm -v -rf "{}"

	# Remove all buildreqs.nosrc packages:
	find ~/rpm* pgdg* -iname "*buildreqs.nosrc*" -print0 | xargs -0 /bin/rm -v -rf "{}"

	# Find the packages, and sign them. Using an expect script to automate signing process.
	# The first parameter refers to the location of the RPMs:
	for signpackagelist in `find ~/$1* -iname "*$signPackageName*$packageVersion*.rpm"`; do /usr/bin/expect ~/bin/signrpms.expect $signpackagelist; done
}
