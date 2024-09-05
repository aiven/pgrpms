#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

export COMMON_RPM_DIR=/var/lib/pgsql/rpmcommon/ALLRPMS
export COMMON_SRPM_DIR=/var/lib/pgsql/rpmcommon/ALLSRPMS
export COMMON_DEBUG_RPM_DIR=/var/lib/pgsql/rpmcommon/ALLDEBUGRPMS

# Create directories for binary and source RPMs. This directory will help us
# to create the repo files easily (though this can be done via ansible during initial installation:

mkdir -p $COMMON_RPM_DIR
mkdir -p $COMMON_SRPM_DIR
mkdir -p $COMMON_DEBUG_RPM_DIR

echo "${green}Syncing PostgreSQL common RPMs for $os - $osarch${reset}"

# rsync binary and source RPMs to their own directories:

rsync --checksum -av --delete --stats /var/lib/pgsql/rpmcommon/RPMS/$osarch/ /var/lib/pgsql/rpmcommon/RPMS/noarch/ $COMMON_RPM_DIR
rsync --checksum -av --delete --stats /var/lib/pgsql/rpmcommon/SRPMS/ $COMMON_SRPM_DIR

# Move debuginfo and debugsource packages to a separate directory.
# First clean the old ones, and then copy existing ones:
rm -rf $COMMON_DEBUG_RPM_DIR/*
mv $COMMON_RPM_DIR/*debuginfo* $COMMON_RPM_DIR/*debugsource* $COMMON_DEBUG_RPM_DIR/

# Now, create repo for RPMs and SRPMS:

createrepo --changelog-limit=3 --workers=4 -d --update $COMMON_RPM_DIR
createrepo --changelog-limit=3 --workers=4 -d --update $COMMON_SRPM_DIR
createrepo --changelog-limit=3 --workers=4 -d --update $COMMON_DEBUG_RPM_DIR

echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $COMMON_RPM_DIR/repodata/repomd.xml
echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $COMMON_SRPM_DIR/repodata/repomd.xml
echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $COMMON_DEBUG_RPM_DIR/repodata/repomd.xml

# Finally, perform the rsync:

rsync --checksum -ave ssh --delete $COMMON_RPM_DIR/ yumupload@yum.postgresql.org:yum/yum/common/$osdistro/$os-$osarch
rsync --checksum -ave ssh --delete $COMMON_SRPM_DIR/ yumupload@yum.postgresql.org:yum/yum/srpms/common/$osdistro/$os-$osarch
aws s3 sync $COMMON_DEBUG_RPM_DIR s3://dnf-debuginfo.postgresql.org/debug/common/$osdistro/$os-$osarch/
aws cloudfront create-invalidation --distribution-id E3CHUBIN4OQV1C --path /debug/common/$osdistro/$os-$osarch/repodata/*

exit 0
