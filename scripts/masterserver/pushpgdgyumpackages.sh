#!/bin/bash
# This scripts pushes binary RPMS to yum.postgresql.org. 
# We first create repository related files, and then rsync them.
# You don't *need to* remove old versions everytime, yum will
# pick up the latest versions for users.

# This is the default root for the RPMs:
cd /media/disk/RPMS

# If you want to push a specific version, use it like below:
for i in `ls -d 9.1`
#for i in `ls -d 9.2 9.1 9.0 8.4 8.3`
do
	cd $i
#	for j in `ls -d redhat`
	for j in `ls -d fedora`
#	for j in `ls -d redhat fedora`
	do
		cd $j
#		for k in `ls -d *`
		for k in `ls -d fedora-17-x*`
#		for k in `ls -d rhel-5-*`
#		for k in `ls -d fedora-16* rhel-*`
		do
			cd $k
			echo "--------------------------"
			echo "Working on $i - $j - $k"
			echo "--------------------------"
			# Create / update repo files and web interface:
			createrepo --checksum=sha -g /usr/local/etc/postgresqldbserver-$i.xml -d --update . && repoview -u "http://yum.postgresql.org/$i/$j/$k/" -o repoview/ -t "PostgreSQL PGDG RPMs" .
			# rsync files to the relevant directory:
			rsync -ave ssh  --delete /media/disk/RPMS/$i/$j/$k  devrim@www.gunduz.org:/home/community/postgresqlrpms.org/public_html/$i/$j/
			cd ..
		done
		cd ..
	done
	cd ..
done
