#!/usr/bin/bash

#################################################
#						#
# Devrim Gündüz <devrim@gunduz.org> - 2024	#
#						#
#################################################

source ~/bin/global.sh

~/bin/s3indexbuilder.py $awssrpmurl srpms/ --cfdistribution $CF_SRPM_DISTRO_ID
~/bin/s3indexbuilder.py $awsdebuginfourl debug/ --cfdistribution $CF_DEBUG_DISTRO_ID

aws cloudfront create-invalidation --distribution-id $CF_SRPM_DISTRO_ID --path /srpms
aws cloudfront create-invalidation --distribution-id $CF_DEBUG_DISTRO_ID --path /debug
