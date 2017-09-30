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

echo "We can now configure the Apache Web server for you. This will create the pgAdmin4 conf file under /etc/httpd/conf.d/. Do you wish to continue?"
select pgayn in "Yes" "No"; do
    case $pgayn in
        Yes )
	echo
	cp /etc/httpd/conf.d/pgadmin4-v2.conf.sample /etc/httpd/conf.d/pgadmin4-v2.conf
	echo "pgAdmin4-v2 Apache config file is created as /etc/httpd/conf.d/pgadmin4-v2.conf"
	break;;
        No ) exit;;
    esac
done

httpd_status=`ps cax | grep httpd`
if [ $? -eq 0 ]; then
	echo "Apache web server is running. Reload is required for pgAdmin4 installation to complete. Would you like to continue?"
select pgahtyn in "Yes" "No"; do
    case $pgahtyn in
        Yes )
	echo
	systemctl reload httpd
	if [ $? != 0 ]
	then
		echo "Error reloading httpd. Please check systemd logs"
	else
		echo "Apache successfully reloaded. You can now start using pgAdmin4 in web mode"
	fi
        break;;
        No ) exit;;
    esac
 done
else
	echo "Apache web server is not running. We can start the web server for you to finish pgAdmin4 installation. Would you like to continue?"
select pgahtyn in "Yes" "No"; do
    case $pgahtyn in
        Yes )
	echo
	systemctl restart httpd
	if [ $? != 0 ]
	then
		echo "Error starting httpd. Please check systemd logs"
	else
		echo "Apache successfully started. You can now start using pgAdmin4 in web mode"
	fi
        break;;
        No ) exit;;
    esac
 done
fi

exit 0
