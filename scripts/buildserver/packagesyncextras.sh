#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

export BASE_DIR=/var/lib/pgsql/pgdg.$osshort.extras

export EXTRAS_RPM_DIR=$BASE_DIR/ALLRPMS
export EXTRAS_SRPM_DIR=$BASE_DIR/ALLSRPMS

# Create directories for binary and source RPMs. This directory will help us
# to create the repo files easily (though this can be done via ansible during initial installation:

mkdir -p $EXTRAS_RPM_DIR
mkdir -p $EXTRAS_SRPM_DIR

echo "${green}Syncing PostgreSQL extras RPMs for $os - $osarch${reset}"

# rsync binary and source RPMs to their own directories:

rsync --checksum -av --delete --stats $BASE_DIR/RPMS/$osarch/ $BASE_DIR/RPMS/noarch/ $EXTRAS_RPM_DIR
rsync --checksum -av --delete --stats $BASE_DIR/SRPMS/ $EXTRAS_SRPM_DIR

# Now, create repo for RPMs and SRPMS:

createrepo --changelog-limit=3 --workers=4 -d --update $EXTRAS_RPM_DIR
createrepo --changelog-limit=3 --workers=4 -d --update $EXTRAS_SRPM_DIR

echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $EXTRAS_RPM_DIR/repodata/repomd.xml
echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $EXTRAS_SRPM_DIR/repodata/repomd.xml

# Finally, perform the rsync:

rsync -ave ssh --delete $EXTRAS_RPM_DIR/ yumupload@yum.postgresql.org:yum/yum/common/pgdg-$osshort-extras/$osdistro/$os-$osarch
rsync -ave ssh --delete $EXTRAS_SRPM_DIR/ yumupload@yum.postgresql.org:yum/yum/srpms/common/pgdg-$osshort-extras/$osdistro/$os-$osarch

exit 0
