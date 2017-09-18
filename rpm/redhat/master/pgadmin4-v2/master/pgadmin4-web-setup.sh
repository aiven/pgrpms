#!/bin/bash

#
# A basic shell script to setup pgadmin4 in server mode
#

# Run setup script first:
PYTHONSITELIB/pgadmin4-web/setup.py

if [ $? != 0 ]
then
	echo "Error setting up server mode. Please examine the output above"
	exit 1
fi

# Create and own log directories:
mkdir -m 700 /var/log/pgadmin
touch /var/log/pgadmin/pgadmin.log
chown apache: /var/log/pgadmin -R

exit 0

