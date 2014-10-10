WORDPRESS_INSTALL_DIR="wordpress"
WORDPRESS_DATABASE="db_wordpress"
WORDPRESS_DATABASE_PASSWORD="wordpress"
WORDPRESS_DATABASE_USER="usr_wordpress"
WORDPRESS_ADMIN_USER="webwvs"
WORDPRESS_ADMIN_PASSWORD="webwvs12"

if isDone "$INSTALL_DIR/$WORDPRESS_INSTALL_DIR" "Wordpress" = true ; then
    return
fi

rm -rf $INSTALL_DIR/$WORDPRESS_INSTALL_DIR

download http://wordpress.org/latest.tar.gz wordpress.tar.gz 1
tar xfz $TMPDIR/wordpress.tar.gz -C $INSTALL_DIR

mysql -uroot -e "
    DROP DATABASE IF EXISTS $WORDPRESS_DATABASE;
    CREATE DATABASE IF NOT EXISTS $WORDPRESS_DATABASE;
    GRANT ALL PRIVILEGES ON "$WORDPRESS_DATABASE".* TO '$WORDPRESS_DATABASE_USER'@'localhost' IDENTIFIED BY '$WORDPRESS_DATABASE_PASSWORD';
    FLUSH PRIVILEGES;"

sed -e "s#database_name_here#$WORDPRESS_DATABASE#g" \
    -e "s#username_here#$WORDPRESS_DATABASE_USER#g" \
    -e "s#password_here#$WORDPRESS_DATABASE_PASSWORD#g" \
    $INSTALL_DIR/$WORDPRESS_INSTALL_DIR/wp-config-sample.php \
    | tee $INSTALL_DIR/$WORDPRESS_INSTALL_DIR/wp-config.php >/dev/null

cp $SCRIPTDIR/applications/wordpress_install.sh $INSTALL_DIR/$WORDPRESS_INSTALL_DIR/wp-admin/install.sh

chmod a+x $INSTALL_DIR/$WORDPRESS_INSTALL_DIR/wp-admin/install.sh

# customize path and disable caching
echo "
define('WP_SITEURL', 'http://wvs.localhost/wordpress');
define('WP_HOME', 'http://wvs.localhost/wordpress');
define('WP_CACHE', 'false');
" >> $INSTALL_DIR/$WORDPRESS_INSTALL_DIR/wp-config.php

# execute the wrapper script (to install wordpress)
$INSTALL_DIR/$WORDPRESS_INSTALL_DIR/wp-admin/install.sh WVS-Blog $WORDPRESS_ADMIN_USER wvs@example.com $WORDPRESS_ADMIN_PASSWORD

# cleanup
rm -rf $INSTALL_DIR/$WORDPRESS_INSTALL_DIR/wp-admin/install.sh

