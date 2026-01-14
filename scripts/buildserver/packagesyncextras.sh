#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2024		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

if [ $extrasrepoenabled != 1 ]
then
	echo "Extras repo is not enabled on this platform"
	exit 1
fi

export BASE_DIR=/var/lib/pgsql/pgdg.$osshort.extras

export EXTRAS_RPM_DIR=$BASE_DIR/ALLRPMS
export EXTRAS_SRPM_DIR=$BASE_DIR/ALLSRPMS
export EXTRAS_DEBUG_RPM_DIR=$BASE_DIR/ALLDEBUGRPMS

# Create directories for binary and source RPMs. This directory will help us
# to create the repo files easily (though this can be done via ansible during initial installation:

mkdir -p $EXTRAS_RPM_DIR
mkdir -p $EXTRAS_SRPM_DIR
mkdir -p $EXTRAS_DEBUG_RPM_DIR

echo "${green}Syncing PostgreSQL extras RPMs for $os - $osarch${reset}"

# rsync binary and source RPMs to their own directories:

rsync --checksum -av --delete --stats $BASE_DIR/RPMS/$osarch/ $BASE_DIR/RPMS/noarch/ $EXTRAS_RPM_DIR
rsync --checksum -av --delete --stats $BASE_DIR/SRPMS/ $EXTRAS_SRPM_DIR

# Move debuginfo and debugsource packages to a separate directory.
# First clean the old ones, and then copy existing ones:
rm -rf $EXTRAS_DEBUG_RPM_DIR/*
mv $EXTRAS_RPM_DIR/*debuginfo* $EXTRAS_RPM_DIR/*debugsource* $EXTRAS_DEBUG_RPM_DIR/

# Now, create repo for RPMs and SRPMS:

createrepo --changelog-limit=3 --workers=4 -d --update $EXTRAS_RPM_DIR
createrepo --changelog-limit=3 --workers=4 -d --update $EXTRAS_SRPM_DIR
createrepo --changelog-limit=3 --workers=4 -d --update $EXTRAS_DEBUG_RPM_DIR

echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $EXTRAS_RPM_DIR/repodata/repomd.xml
echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $EXTRAS_SRPM_DIR/repodata/repomd.xml
echo $GPG_PASSWORD | /usr/bin/gpg2 -a --pinentry-mode loopback --detach-sign --batch --yes --passphrase-fd 0 $EXTRAS_DEBUG_RPM_DIR/repodata/repomd.xml

# We currently pull packages from yonada, so skip the next line:
# rsync -ave ssh --delete $EXTRAS_RPM_DIR/ yumupload@yum.postgresql.org:yum/yum/extras/$osdistro/$os.$osminversion-$osarch

# Sync SRPMs to S3 bucket:
aws s3 sync $EXTRAS_SRPM_DIR $awssrpmurl/srpms/extras/$osdistro/$os.$osminversion-$osarch --exclude "*.html" --exclude "repodata"
aws s3 sync --delete $EXTRAS_SRPM_DIR/repodata/ $awssrpmurl/srpms/extras/$osdistro/$os.$osminversion-$osarch/repodata/ --exclude "*.html"
aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/extras/$osdistro/$os.$osminversion-$osarch/repodata/*

# Sync debug* RPMs to S3 bucket:
aws s3 sync $EXTRAS_DEBUG_RPM_DIR $awsdebuginfourl/debug/extras/$osdistro/$os.$osminversion-$osarch/ --exclude "*.html"
aws s3 sync --delete $EXTRAS_DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/debug/extras/$osdistro/$os.$osminversion-$osarch/repodata/ --exclude "*.html"
aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug/extras/$osdistro/$os.$osminversion-$osarch/repodata/*

# S3 does not allow symlinks, so we have to sync the packages once again to the OS major version directory if this is the latest version of the OS:
if [ "$osislatest" == 1 ]
then
	aws s3 sync $EXTRAS_SRPM_DIR $awssrpmurl/srpms/extras/$osdistro/$os-$osarch --exclude "*.html" --exclude "repodata"
	aws s3 sync --delete $EXTRAS_SRPM_DIR/repodata/ $awssrpmurl/srpms/extras/$osdistro/$os-$osarch/repodata/ --exclude "*.html"

	aws s3 sync $EXTRAS_DEBUG_RPM_DIR $awsdebuginfourl/debug/extras/$osdistro/$os-$osarch/ --exclude "*.html"
	aws s3 sync --delete $EXTRAS_DEBUG_RPM_DIR/repodata/ $awsdebuginfourl/debug/extras/$osdistro/$os-$osarch/repodata/ --exclude "*.html"
	# Invalidate the caches:
	aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms/extras/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*
	aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug/extras/$packageSyncVersion/$osdistro/$os-$osarch/repodata/*
fi
exit 0
