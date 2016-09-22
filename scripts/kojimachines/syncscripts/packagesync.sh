#!/bin/bash

pgrelease=9.6
osdistro=redhat #options: fedora, redhat
os=rhel-7 # options: rhel-7, rhel-6, fedora-24, fedora-23
osarch=x86_64 # options: x86_64, i386
osdirarch=x86_64 # options: x86_64, i686, i386

RPM_DIR=/var/lib/pgsql/rpm/ALLRPMS
SRPM_DIR=/var/lib/pgsql/rpm/ALLSRPMS

# Create directories for binary and source RPMs. This directory will help us
# to create the repo files easily:
mkdir -p $RPM_DIR
mkdir -p $SRPM_DIR

# rsync binary and source RPMs to their own directories:

rsync -av --delete --stats /var/lib/pgsql/rpm/RPMS/$osdirarch/ /var/lib/pgsql/rpm/RPMS/noarch/ $RPM_DIR
rsync -av --delete --stats /var/lib/pgsql/rpm/SRPMS/ /var/lib/pgsql/rpm/ALLSRPMS

# Now, create repo for RPMs and SRPMS:

createrepo --changelog-limit=3 --workers=4 --max-delta-rpm-size=1073741824 --deltas --num-deltas=4 --oldpackagedirs=$RPM_DIR -g /usr/local/etc/postgresqldbserver-$pgrelease.xml -d --update $RPM_DIR && repoview -u "http://yum.postgresql.org/$pgrelease/$osdistro/$os-$osarch/" -o repoview/ -t "PostgreSQL PGDG $pgrelease RPMs" $RPM_DIR/
createrepo --changelog-limit=3 --workers=4 --max-delta-rpm-size=1073741824 --deltas --num-deltas=4 --oldpackagedirs=$SRPM_DIR -d --update $SRPM_DIR && repoview -u "http://yum.postgresql.org/srpms/$pgrelease/$osdistro/$os-$osarch/" -o repoview/ -t "PostgreSQL PGDG $pgrelease RPMs" $SRPM_DIR/

# Finally, perform the rsync:
rsync -ave ssh  --delete $RPM_DIR/  MASKED:/srv/yum/yum/$pgrelease/$osdistro/$os-$osarch
rsync -ave ssh  --delete $SRPM_DIR/  MASKED:/srv/yum/yum/srpms/$pgrelease/$osdistro/$os-$osarch

exit
