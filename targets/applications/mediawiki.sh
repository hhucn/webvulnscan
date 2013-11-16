MEDIAWIKI_WIKI_NAME="WebvulnWiki"
MEDIAWIKI_SERVER="http://wvs.localhost"
MEDIAWIKI_DATABASE="db_mediawiki"
MEDIAWIKI_DATABASE_USER="usr_mediawiki"
MEDIAWIKI_DATABASE_PASSWORD="mediawiki"


wget http://download.wikimedia.org/mediawiki/1.21/mediawiki-1.21.2.tar.gz -nv -O $TMPDIR/mediawiki.tar.gz -c
tar xfz $TMPDIR/mediawiki.tar.gz -C $INSTALL_DIR --transform "s#^mediawiki-[0-9.]*#mediawiki#"

mysql -uroot -e \
	"DROP DATABASE IF EXISTS $MEDIAWIKI_DATABASE;
	CREATE DATABASE IF NOT EXISTS $MEDIAWIKI_DATABASE;
	GRANT ALL PRIVILEGES ON "$MEDIAWIKI_DATABASE".* TO '$MEDIAWIKI_DATABASE_USER'@'localhost' IDENTIFIED BY '$MEDIAWIKI_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"

mysql -u$MEDIAWIKI_DATABASE_USER -p$MEDIAWIKI_DATABASE_PASSWORD $MEDIAWIKI_DATABASE < $INSTALL_DIR/mediawiki/maintenance/tables.sql

cp $SCRIPTDIR/applications/mediawiki.conf $INSTALL_DIR/mediawiki/LocalSettings.php

#sudo chown -R www-data:www-data $INSTALL_DIR/mediawiki

sed -i -e 's#XXX_SITENAME_XXX#'$MEDIAWIKI_WIKI_NAME'#g' \
       -e 's#XXX_SCRIPTPATH_XXX#'mediawiki'#g' \
       -e 's#XXX_SERVER_XXX#'$MEDIAWIKI_SERVER'#g' \
       -e 's#XXX_DBNAME_XXX#'$MEDIAWIKI_DATABASE'#g' \
       -e 's#XXX_DBUSER_XXX#'$MEDIAWIKI_DATABASE_USER'#g' \
       -e 's#XXX_DBPASS_XXX#'$MEDIAWIKI_DATABASE_PASSWORD'#g' \
	$INSTALL_DIR/mediawiki/LocalSettings.php
