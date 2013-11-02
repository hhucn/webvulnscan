#!/bin/bash

#####################################################################
###  Cleanup script to delete installed and configured stuff      ###
#####################################################################

if ! [ `id -u` -eq 0 ]
then
	echo "This script requires superuser privileges."
	exit 1
fi

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Import config files
. $SCRIPTDIR/includes/global.cfg
. $SCRIPTDIR/applications/magento.cfg
. $SCRIPTDIR/applications/mediawiki.cfg

clear
echo "Cleanup started..."

# Temp folder
echo "--- cleaning temp folder"
rm -rf $SCRIPT_TMP_FOLDER;

# Magento installation and database
echo "--- deleting magento installation"
rm -rf $APACHE_DIR/$MAGENTO_INSTALL_FOLDER
SQL1="DELETE FROM mysql.user WHERE User='$MAGENTO_DATABASE_USER';"
SQL2="DROP DATABASE $MAGENTO_DATABASE;"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "${SQL1}${SQL2}" >/dev/null 2>&1

# WikiMedia installation and database
echo "--- deleting WikiMedia installation"
rm -rf $APACHE_DIR/$MEDIAWIKI_INSTALL_FOLDER
SQL1="DELETE FROM mysql.user WHERE User='$MEDIAWIKI_DATABASE_USER';"
SQL2="DROP DATABASE $MEDIAWIKI_DATABASE;"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "${SQL1}${SQL2}" >/dev/null 2>&1

echo "Cleanup finished"
