OWNCLOUD_INSTALL_DIR="owncloud"
OWNCLOUD_SERVER="localhost"
OWNCLOUD_DATABASE="owncloud"
OWNCLOUD_DATABASE_USER="owncloud"
OWNCLOUD_DATABASE_PASSWORD="owncloud"
OWNCLOUD_VERSION="7.0.0"
OWNCLOUD_ADMIN_USERNAME="webwvs"
OWNCLOUD_ADMIN_PASSWORD="webwvs12"

# to install Version 6.0.0a uncomment this line
# OWNCLOUD_VERSION="6.0.0a"

if isDone "$INSTALL_DIR/$OWNCLOUD_INSTALL_DIR" "ownCloud" = true ; then
    return
fi

sudo rm -rf $INSTALL_DIR/$OWNCLOUD_INSTALL_DIR

download http://download.owncloud.org/community/owncloud-$OWNCLOUD_VERSION.tar.bz2 owncloud.tar.bz2
tar xfj $TMPDIR/owncloud.tar.bz2 -C $INSTALL_DIR

mysql -uroot -e \
	"DROP DATABASE IF EXISTS $OWNCLOUD_DATABASE;
	CREATE DATABASE IF NOT EXISTS $OWNCLOUD_DATABASE;
	GRANT ALL PRIVILEGES ON "$OWNCLOUD_DATABASE".* TO '$OWNCLOUD_DATABASE_USER'@'localhost' IDENTIFIED BY '$OWNCLOUD_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"

echo -n "
<?php
\$AUTOCONFIG = array (
'installed' => false,
'dbtype' => 'mysql',
'dbtableprefix' => '',
'adminlogin' => '$OWNCLOUD_ADMIN_USERNAME',
'adminpass' => '$OWNCLOUD_ADMIN_PASSWORD',
'directory' => '$INSTALL_DIR/$OWNCLOUD_INSTALL_DIR',
'dbuser' => '$OWNCLOUD_DATABASE_USER',
'dbname' => '$OWNCLOUD_DATABASE',
'dbhost' => '$OWNCLOUD_SERVER',
'dbpass' => '$OWNCLOUD_DATABASE_PASSWORD',
);" > $INSTALL_DIR/$OWNCLOUD_INSTALL_DIR/config/config.php

mkdir -p "$INSTALL_DIR/$OWNCLOUD_INSTALL_DIR/data"

cd $INSTALL_DIR/$OWNCLOUD_INSTALL_DIR

sudo chown -R www-data:www-data $INSTALL_DIR/$OWNCLOUD_INSTALL_DIR

# The install-dir needs to be encoded
INSTALL_DIR_ENC=$(echo $INSTALL_DIR"%2F"$OWNCLOUD_INSTALL_DIR | sed -e 's/\//%2F/g')
OWNCLOUD_DATA_DIR=$INSTALL_DIR"/"$OWNCLOUD_INSTALL_DIR"/data"

curl --data "install=true&adminpass=$OWNCLOUD_ADMIN_PASSWORD&adminpass-clone=$OWNCLOUD_ADMIN_PASSWORD&adminlogin=$OWNCLOUD_ADMIN_USERNAME&directory=$OWNCLOUD_DATA_DIR&dbuser=$OWNCLOUD_DATABASE_USER&dbtype=mysql&dbpass=$OWNCLOUD_DATABASE_PASSWORD&dbpass-clone=$OWNCLOUD_DATABASE_PASSWORD&dbname=$OWNCLOUD_DATABASE&dbhost=$OWNCLOUD_SERVER" "http://wvs.localhost/$OWNCLOUD_INSTALL_DIR/index.php/"

