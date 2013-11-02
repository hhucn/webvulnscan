
#####################################################################
###  Media Wiki install script                                    ###
###  To modify the installation parameters check mediawiki.cfg    ###
#####################################################################

# Import configuration file
. $SCRIPTDIR/applications/mediawiki.cfg

echo "Installing MediaWiki"

cd $SCRIPT_TMP_FOLDER
wget http://download.wikimedia.org/mediawiki/$MEDIAWIKI_VERSION_SHORT/mediawiki-$MEDIAWIKI_VERSION_LONG.tar.gz -o /dev/null

print "--- extracting files..."
tar xfz mediawiki-$MEDIAWIKI_VERSION_LONG.tar.gz -C $APACHE_DIR > /dev/null

cd $APACHE_DIR
mv mediawiki-$MEDIAWIKI_VERSION_LONG $MEDIAWIKI_INSTALL_FOLDER

print "--- creating database and user"
SQL1="CREATE DATABASE IF NOT EXISTS $MEDIAWIKI_DATABASE;"
SQL2="GRANT ALL PRIVILEGES ON "$MEDIAWIKI_DATABASE".* TO '$MEDIAWIKI_DATABASE_USER'@'localhost' IDENTIFIED BY '$MEDIAWIKI_DATABASE_PASSWORD';"
SQL3="FLUSH PRIVILEGES;"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "${SQL1}${SQL2}${SQL3}"

