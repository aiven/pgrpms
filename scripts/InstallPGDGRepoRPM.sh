#!/bin/bash

#########################################################
#							#
# Very simple bash script that detects OS, version and	#
# arch, and then asks for the PostgreSQL version, then	#
# creates .repo file for the PostgreSQL YUM repository 	#
# located at http://yum.PostgreSQL.org			#
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2015-2016		#
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
echo -n "${blue}(9.6,9.5,9.4, 9.3, 9.2, etc)${reset}: "

read pgversion

if [[ "$pgversion" =~ ^(9.6|9.5|9.4|9.3|9.2)$ ]]; then
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
# Oracle Linux: Not checked yet.

# CentOS/RHEL 6 and 7 (tested)
if [ "$lsb_distro_name" = "centos" ] || [ "$lsb_distro_name" = "redhatenterpriseserver" ] || [ "$lsb_distro_name" = "scientific" ]
then
	lsb_distro_url_first="redhat"
	lsb_distro_url_second="rhel"
	lsb_distro_url_third="centos"
fi

# Fedora

if [ "$lsb_distro_name" = "fedora" ]
then
	lsb_distro_url_first="fedora"
	lsb_distro_url_second="fedora"
	lsb_distro_url_third="fedora"
fi

# Give confirmation to the user about the platform:
echo "Installer will now create repository file for PostgreSQL $pgversion on ${green}$lsb_distro_name $lsb_distro_version${reset} for ${green}$distro_arch${reset} architecture"

echo "[pgdg$pgshortversion]
name=PostgreSQL $pgversion \$releasever - \$basearch
baseurl=https://download.postgresql.org/pub/repos/yum/$pgversion/$lsb_distro_url_first/$lsb_distro_url_second-\$releasever-\$basearch
enabled=1
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG-$pgshortversion

[pgdg$pgshortversion-source]
name=PostgreSQL $pgversion \$releasever - \$basearch - Source
failovermethod=priority
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/$pgversion/$lsb_distro_url_first/$lsb_distro_url_second-\$releasever-\$basearch
enabled=0
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG-$pgshortversion

[pgdg$pgshortversion-updates-testing]
name=PostgreSQL $pgversion \$releasever - \$basearch - Updates Testing
baseurl=https://download.postgresql.org/pub/repos/yum/testing/$pgversion/$lsb_distro_url_first/$lsb_distro_url_second-\$releasever-\$basearch
enabled=0
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG-$pgshortversion

[pgdg$pgshortversion-source-updates-testing]
name=PostgreSQL $pgversion \$releasever - \$basearch - Source Testing
failovermethod=priority
baseurl=https://download.postgresql.org/pub/repos/yum/srpms/testing/$pgversion/$lsb_distro_url_first/$lsb_distro_url_second-\$releasever-\$basearch
enabled=0
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-PGDG-$pgshortversion

" > /etc/yum.repos.d/pgdg-temp-$pgshortversion.repo

echo
echo "Temporary repository has been successfully configured."
echo "${red}Important:Please remove /etc/yum.repos.d/pgdg-temp-$pgshortversion.repo file after installing yum repo RPM manually.${reset}"
echo "Please visit http://yum.PostgreSQL.org/repopackages.php to install the repo RPM."
echo
echo "We are now ready to install PostgreSQL $pgversion."

read -r -p "Are you sure? [y/N] " response
case $response in
	[yY][eE][sS]|[yY])
	echo "Please wait while we are installing PostgreSQL $pgversion RPMs."
if [ "$lsb_distro_name" = "fedora" ]
then
	dnf -y groupinstall "PostgreSQL Database Server $pgversion PGDG"
else
	yum -y groupinstall "PostgreSQL Database Server $pgversion PGDG"
fi
	# Check whether the packages have been installed or not:
	if [ $? != 0 ]
	then
		echo
		echo "${red}There is an error installing PostgreSQL $pgversion. Please check the messages above.${reset}"
		echo "${red}Tip: PostgreSQL $pgversion may not be available for your platform.${reset}"
		exit 1
	fi
        ;;
    *)
	echo
	echo
	echo "You can later install PostgreSQL server by running"
	echo "${blue}yum groupinstall \"PostgreSQL Database Server $pgversion PGDG\"${reset}"
        ;;
esac
exit 0
