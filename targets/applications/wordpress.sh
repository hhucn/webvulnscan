WORDPRESS_INSTALL_DIR="wordpress"
WORDPRESS_DATABASE="db_wordpress"
WORDPRESS_DATABASE_PASSWORD="wordpress"
WORDPRESS_DATABASE_USER="usr_wordpress"
WORDPRESS_ADMIN_USER="wordpress"
WORDPRESS_ADMIN_PASSWORD="wordpress"

cd $INSTALL_DIR
sudo rm -rf $WORDPRESS_INSTALL_DIR

wget http://wordpress.org/latest.tar.gz -O $TMPDIR/wordpress.tar.gz -c
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

echo "#!/usr/bin/php
<?php
// php-script used from http://stackoverflow.com/users/1437818/broesph and then modified

function get_args(){
        \$args = array();
        for (\$i=1; \$i<count(\$_SERVER['argv']); \$i++){
                \$arg = \$_SERVER['argv'][\$i];
                if (\$arg{0} == '-' && \$arg{1} != '-'){
                        for (\$j=1; \$j < strlen(\$arg); \$j++){
                                \$key = \$arg{\$j};
                                \$value = \$_SERVER['argv'][\$i+1]{0} != '-' ? preg_replace(array('/^[\"\\']/', '/[\"\']$/'), '', \$_SERVER['argv'][++\$i]) : true;
                                \$args[\$key] = \$value;
                        }
                }
                else
                        \$args[] = \$arg;
        }

        return \$args;
}

// read commandline arguments
\$opt = get_args();

define( 'WP_INSTALLING', true );
 
require_once( dirname( dirname( __FILE__ ) ) . '/wp-load.php' );
require_once( dirname( __FILE__ ) . '/includes/upgrade.php' );
require_once(dirname(dirname(__FILE__)) . '/wp-includes/wp-db.php');

\$result = wp_install(\$opt[0], \$opt[1], \$opt[2], false, '', \$opt[3]);


" | sudo tee $INSTALL_DIR/$WORDPRESS_INSTALL_DIR/wp-admin/install.sh

sudo chmod a+x $INSTALL_DIR/$WORDPRESS_INSTALL_DIR/wp-admin/install.sh

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

