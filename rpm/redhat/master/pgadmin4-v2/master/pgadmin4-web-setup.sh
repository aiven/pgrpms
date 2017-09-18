#!/bin/bash

#
# A basic shell script to setup pgadmin4 in server mode
#

# Run setup script first:
PYTHONDIR PYTHONSITELIB/pgadmin4-web/setup.py

if [ $? != 0 ]
then
	echo "Error setting up server mode. Please examine the output above."
	exit 1
fi

# Own directories:
chown apache: /var/log/pgadmin /var/lib/pgadmin -R

exit 0

