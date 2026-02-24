#!/usr/bin/bash

#########################################################
#							#
# Devrim Gündüz <devrim@gunduz.org> - 2026		#
#							#
#########################################################

# Include common values:
source ~/bin/global.sh

for signpackagelist in `find ~/rpmcommon/ ~/pgdg.extras ~/rpm1* -iname "*.rpm" | grep -v ALL`
do
	rpmsign --addsign $signpackagelist
done

exit 0
