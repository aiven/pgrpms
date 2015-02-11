#!/bin/bash

#########################################################
#							#
# Very simple bash script that detects OS, version and	#
# arch, and then asks for the PostgreSQL version, then	#
# install the repo RPM for the user of the PostgreSQL 	#
# YUM repository located at http://yum.PostgreSQL.org	#
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2015		#
#							#
#########################################################

clear
echo

#Color schemes
red=`tput setaf 1`
green=`tput setaf 2`
blue=`tput setaf 4`
reset=`tput sgr0`

# Check whether lsb_release exists or not:

if [ ! -f /usr/bin/lsb_release ]
then
	echo
	echo "${red}ERROR:${reset} lsb_release command does not exist. Please install it with"
	echo
	echo "${blue}	yum -y install redhat-lsb-core"
	echo
	echo "${red}Exiting...${reset}"
	echo
	exit 1
fi

# Some introductory message (TODO: more should be added)
echo "${green}This script only installs the PostgreSQL repository RPM for the official"
echo "PostgreSQL repository located at http://yum.PostgreSQL.org . "
echo ""
echo "Please follow the procedures for installing PostgreSQL server after"
echo "installing the repository RPM.${reset}"
echo

# Make sure only root can run this script:
if [ "$(id -u)" != "0" ]; then
	echo
	echo "${red}ERROR:${reset} This script must be run as root" 1>&2
	echo
	exit 1
fi

# Gather some information from the OS: OS name, version and arch:
lsb_distro_name=`lsb_release -i -s`
lsb_distro_version=`lsb_release -r -s`
distro_arch=`uname -m`

# We need the lowercase version of the distro name:
lsb_distro_name=`echo $lsb_distro_name | awk '{print tolower($0)}'`

#Ask for which PostgreSQL version is needed"
echo "Please enter the ${red}major${reset} PostgreSQL version that you want to install:"
echo -n "${blue}(9.4, 9.3, 9.2, etc)${reset}: "

read pgversion

if [[ "$pgversion" =~ ^(9.4|9.3|9.2|9.1|9.0)$ ]]; then
	echo
	echo "${green}$pgversion is currently supported, will continue...${reset}"
	echo
else
	echo
	echo "${red}ERROR:${blue} $pgversion${red} is not supported or not a PostgreSQL major version"
	echo "Exiting.${reset}"
	echo
	exit
fi

# We also need a dotless version of pgversion variable:
pgshortversion=`echo $pgversion | tr -d . `

# We need to check the distro name, and make some changes in the URL for some of them.
# CentOS 6: We need to change first occurence of centos to redhat, 2nd to rhel:
# CentOS 7: CentOS 7 includes an extra string (1406), so we need to omit that.
# Fedora: No need to change.
# RHEL 7: RedHatEnterpriseServer
# RHEL 6: Not checked yet.
# SL: Not checked yet.
# Oracle Linux: Not checked yet.

# CentOS 6,7 and RHEL 7
if [ "$lsb_distro_name" = "centos" ]
then
	lsb_distro_url_first="redhat"
	lsb_distro_url_second="rhel"
	lsb_distro_url_third="centos"
fi

# RHEL 7
if [ "$lsb_distro_name" = "redhatenterpriseserver" ]
then
	lsb_distro_url_first="redhat"
	lsb_distro_url_second="rhel"
	lsb_distro_url_third="redhat"
fi

# SL 6
if [ "$lsb_distro_name" = "scientific" ]
then
	lsb_distro_url_first="redhat"
	lsb_distro_url_second="rhel"
	lsb_distro_url_third="redhat"
fi

if [ "$lsb_distro_name" = "fedora" ]
then
	lsb_distro_url_first="fedora"
	lsb_distro_url_second="fedora"
	lsb_distro_url_third="fedora"
fi

# RHEL 7.0:
if [ "$lsb_distro_version" = "7.0.1406" ]
then
	lsb_distro_version="7.0"
fi

# Give confirmation to the user about the platform:
echo "Installer will now install the repository RPM for ${green}$lsb_distro_name $lsb_distro_version${reset} for ${green}$distro_arch${reset} architecture"

# Install the repository RPM
echo "Please stand by while installing the repository RPM. It may take a while."
echo
yum --quiet -y install http://yum.postgresql.org/$pgversion/$lsb_distro_url_first/$lsb_distro_url_second-$lsb_distro_version-$distro_arch/pgdg-$lsb_distro_url_third$pgshortversion-$pgversion-latest.noarch.rpm

# Check whether the repo RPM has been installed or not:
if [ $? != 0 ]
then
	# Throw error messages:
	echo
	echo "${red}Error installing the repository RPM. See the message above for details."
	echo "This distro/arch may not be supported for PostgreSQL $pgversion${reset}"
	exit 1
fi

# RPM has been installed successfully.
echo
echo "Repository RPM successfully installed. You can now install PostgreSQL server by running"
echo "${blue}yum groupinstall \"PostgreSQL Database Server $pgversion PGDG\"${reset}"

read -r -p "Are you sure? [y/N] " response
case $response in
	[yY][eE][sS]|[yY])
	echo "Please wait while we are installing PostgreSQL $pgversion RPMs."
	yum -y groupinstall "PostgreSQL Database Server $pgversion PGDG"
        ;;
    *)
	echo
	echo
	echo "You can later install PostgreSQL server by running"
	echo "${blue}yum groupinstall \"PostgreSQL Database Server $pgversion PGDG\"${reset}"
        ;;
esac
exit 0
