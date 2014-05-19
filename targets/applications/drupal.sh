DRUPAL_DATABASE="db_drupal"
DRUPAL_DATABASE_USER="usr_drupal"
DRUPAL_DATABASE_PASSWORD="drupal"

# cleanup
sudo rm -rf $INSTALL_DIR/drupal

# download
wget http://ftp.drupal.org/files/projects/drupal-7.28.tar.gz -nv -O $TMPDIR/drupal.tar.gz -c
tar xfz $TMPDIR/drupal.tar.gz -C $INSTALL_DIR --transform "s#^drupal-[0-9.]*#drupal#"

# set permissions
sudo chmod 777 $INSTALL_DIR/drupal/sites/default


# copy and modify settings
sed -e "s#XXX_DRUPAL_DATABASE_XXX#$DRUPAL_DATABASE#g" \
    -e "s#XXX_DRUPAL_DATABASE_USER_XXX#$DRUPAL_DATABASE_USER#g" \
    -e "s#XXX_DRUPAL_DATABASE_PASSWORD_XXX#$DRUPAL_DATABASE_PASSWORD#g" \
    $SCRIPTDIR/applications/drupal.conf \
    | sudo tee $INSTALL_DIR/drupal/sites/default/settings.php >/dev/null

sudo chmod 777 $INSTALL_DIR/drupal/sites/default/settings.php


#setup database
mysql -uroot -e \
	"DROP DATABASE IF EXISTS $DRUPAL_DATABASE;
	CREATE DATABASE IF NOT EXISTS $DRUPAL_DATABASE;
	GRANT ALL PRIVILEGES ON "$DRUPAL_DATABASE".* TO '$DRUPAL_DATABASE_USER'@'localhost' IDENTIFIED BY '$DRUPAL_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"


curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/drupal/install.php?profile=standard&locale=en"
curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/drupal/install.php?profile=standard&locale=en&op=start&id=1" --data "site_name=webwvs&site_mail=a@b.com&account[name]=webwvsaccount[mail]=webwvsaccount[pass][pass1]=webwvsaccount[pass][pass2]=webwvs"
