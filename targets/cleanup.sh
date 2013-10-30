#!/bin/bash

#####################################################################
###  Cleanup script to delete installed and configured stuff      ###
#####################################################################

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

#Import config files
. $SCRIPTDIR/global.cfg
. $SCRIPTDIR/applications/magento.cfg

clear
echo "Cleanup started..."

# Temp folder
echo "--- cleaning temp folder"
rm -rf $SCRIPT_TMP_FOLDER

# Magento installation and database
echo "--- deleting magento installation"
rm -rf $APACHE_DIR/$MAGENTO_INSTALL_FOLDER
SQL1="DELETE FROM mysql.user WHERE User='usr_magento';"
SQL2="DROP DATABASE db_magento;"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "${SQL1}${SQL2}" >/dev/null 2>&1

echo "Cleanup finished"
