OWNCLOUD_INSTALL_FOLDER="owncloud"
OWNCLOUD_SERVER="localhost"
OWNCLOUD_DATABASE="db_owncloud"
OWNCLOUD_DATABASE_USER="usr_owncloud"
OWNCLOUD_DATABASE_PASSWORD="owncloud"
OWNCLOUD_VERSION="5.0.13"
OWNCLOUD_ADMIN_USERNAME="admin"
OWNCLOUD_ADMIN_PASSWORD="admin"

rm -rf $APACHE_DIR/$OWNCLOUD_INSTALL_FOLDER

wget http://download.owncloud.org/community/owncloud-$OWNCLOUD_VERSION.tar.bz2 -O $TMPDIR/owncloud.tar.bz2 -c
tar xfj $TMPDIR/owncloud.tar.bz2 -C $APACHE_DIR

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
'directory' => '$APACHE_DIR/$OWNCLOUD_INSTALL_FOLDER',
'dbuser' => '$OWNCLOUD_DATABASE_USER',
'dbname' => '$OWNCLOUD_DATABASE',
'dbhost' => '$OWNCLOUD_SERVER',
'dbpass' => '$OWNCLOUD_DATABASE_PASSWORD',
);" > $APACHE_DIR/$OWNCLOUD_INSTALL_FOLDER/config/config.php

mkdir -p "$APACHE_DIR/$OWNCLOUD_INSTALL_FOLDER/data"

chown -R www-data:www-data $APACHE_DIR/$OWNCLOUD_INSTALL_FOLDER

cd $APACHE_DIR/$OWNCLOUD_INSTALL_FOLDER


# temporary patch the script so that we can simulate post-vars (for the initial setup)
cp index.php index.php.bk

#$INDEX_PATCH=" \<?php if (!isset($_SERVER['HTTP_HOST'])) { parse_str($argv[1], $_POST); } ?>";
INDEX_PATCH='<?php if (!isset($_SERVER["HTTP_HOST"])) { parse_str($argv[1], $_POST); } ?>';

sed -i "1s/^/$INDEX_PATCH\n/" index.php

#echo $INDEX_PATCH | cat - index.php > temp && mv temp index.php

#php -f index.php
