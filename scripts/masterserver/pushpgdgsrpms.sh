#!/bin/bash

# This scripts pushes source RPMS to yum.postgresql.org. 
# We first create repository related files, and then rsync them.
# You don't *need to* remove old versions everytime, yum will
# pick up the latest versions for users.

# This is the default root for the RPMs:
cd /media/disk/RPMS/srpms-web/

# If you want to push a specific version, use it like below:
#for i in `ls -d 9.1 9.0 8.4 8.3 8.2`
for i in `ls -d 9.2`
do
	cd $i
	for j in `ls -d redhat fedora`
#	for j in `ls -d redhat`
#	for j in `ls -d fedora`
	do
		cd $j
		for k in `ls -d *`
#		for k in `ls -d rhel-6-*`
# 		for k in `ls -d fedora-16* rhel-*`
#		for k in `ls -d fedora-16*`
		do
			cd $k
			echo "Working on $i - $j - $k"
			# Create / update repo files and web interface:
			createrepo -d . && repoview -u "http://yum.postgresql.org/srpms/$i/$j/$k/" -o repoview/ -t "PostgreSQL PGDG RPMs" .
			# rsync files to the relevant directory:
			rsync -ave ssh  --delete /media/disk/RPMS/srpms-web/$i/$j/$k  devrim@staging.pgrpms.org:/home/community/postgresqlrpms.org/public_html/srpms/$i/$j/
			cd ..
		done
		cd ..
	done
	cd ..
done

