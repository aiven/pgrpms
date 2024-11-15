#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

for packageBuildVersion in ${pgStableBuilds[@]}
do
	echo "Checking PostgreSQL $packageBuildVersion"
	upload_status='curl -s -o /dev/null -w "%{http_code}" https://download.postgresql.org/pub/repos/yum/$packageBuildVersion/$osdistro/$os-$osarch/repodata'
	if [ $upload_status == "404" ]
	then
		echo "${red}ERROR:${reset} There is a problem with the PostgreSQL $packageBuildVersion status"
	fi
	echo
done
