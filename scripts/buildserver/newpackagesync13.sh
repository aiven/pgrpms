#!/bin/bash

pgrelease=13
osdistro=fedora
os=fedora-33
osarch=x86_64
osdirarch=x86_64

RPM_DIR=/var/lib/pgsql/rpm13/ALLRPMS
DEBUG_RPM_DIR=/var/lib/pgsql/rpm13/ALLDEBUGRPMS
SRPM_DIR=/var/lib/pgsql/rpm13/ALLSRPMS

export GPG_TTY=$(tty)
export GPG_PASSWORD=blahblah

# Create directories for binary and source RPMs. This directory will help us
# to create the repo files easily:
mkdir -p $RPM_DIR
mkdir -p $SRPM_DIR
mkdir -p $DEBUG_RPM_DIR

#Rem ove older binaries
#rm $(repomanage --old --keep=2 /var/lib/pgsql/rpm13/RPMS/$osdirarch/) -f
#rm $(repomanage --old --keep=2 /var/lib/pgsql/rpm13/RPMS/noarch/) -f
#rm $(repomanage --old --keep=2 /var/lib/pgsql/rpm13/SRPMS/) -f

# rsync binary and source RPMs to their own directories:

rsync -av --delete --stats /var/lib/pgsql/rpm13/RPMS/$osdirarch/ /var/lib/pgsql/rpm13/RPMS/noarch/ $RPM_DIR
rsync -av --delete --stats /var/lib/pgsql/rpm13/SRPMS/ /var/lib/pgsql/rpm13/ALLSRPMS

# Move debuginfo and debugsource packages to a separate directory.
# First clean the old ones, and then copy existing ones:
rm -rf $DEBUG_RPM_DIR/*
mv $RPM_DIR/*debuginfo* $RPM_DIR/*debugsource* $DEBUG_RPM_DIR/

# Now, create repo for RPMs and SRPMS:

createrepo --changelog-limit=3 --workers=4 --oldpackagedirs=$RPM_DIR -g /usr/local/etc/postgresqldbserver-$pgrelease.xml -d --update $RPM_DIR && repoview -u "https://download.postgresql.org/pub/repos/yum//$pgrelease/$osdistro/$os-$osarch/" -o repoview/ -t "PostgreSQL PGDG $pgrelease Updates RPMs" $RPM_DIR/
createrepo --changelog-limit=3 --workers=4 --oldpackagedirs=$DEBUG_RPM_DIR -g /usr/local/etc/postgresqldbserver-$pgrelease.xml -d --update $DEBUG_RPM_DIR
createrepo --changelog-limit=3 --workers=4 --oldpackagedirs=$SRPM_DIR -d --update $SRPM_DIR && repoview -u "https://download.postgresql.org/pub/repos/yum/srpms//$pgrelease/$osdistro/$os-$osarch/" -o repoview/ -t "PostgreSQL PGDG $pgrelease Updates RPMs" $SRPM_DIR/

echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign  --batch --yes --passphrase-fd 0 $COMMON_RPM_DIR/repodata/repomd.xml
echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --export $GPG_KEY_ID > $COMMON_SRPM_DIR/repodata/repomd.xml.key

# Finally, perform the rsync:
rsync -ave ssh --delete $RPM_DIR/ foo@foo:foo//$pgrelease/$osdistro/$os-$osarch
rsync -ave ssh --delete $DEBUG_RPM_DIR/ foo@foo:foo//debug/$pgrelease/$osdistro/$os-$osarch
rsync -ave ssh --delete $SRPM_DIR/ foo@foo:foo/srpms//$pgrelease/$osdistro/$os-$osarch

exit
