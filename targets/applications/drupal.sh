DRUPAL_DATABASE="db_drupal"
DRUPAL_DATABASE_USER="usr_drupal"
DRUPAL_DATABASE_PASSWORD="drupal"

if [ -d "$INSTALL_DIR/drupal" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping Drupal installation: Drupal is already installed."
    	return
	fi
fi

DRUPAL_COOKIE=$(mktemp $TMPDIR/XXXXXX)

sudo rm -rf $INSTALL_DIR/drupal

# download
download http://ftp.drupal.org/files/projects/drupal-7.28.tar.gz drupal.tar.gz
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

curl -s -c $DRUPAL_COOKIE -b $DRUPAL_COOKIE --globoff "http://wvs.localhost/drupal/install.php?profile=standard&locale=en" > /dev/null
curl -s -c $DRUPAL_COOKIE -b $DRUPAL_COOKIE --globoff "http://wvs.localhost/drupal/install.php?profile=standard&locale=en&op=start&id=1" --data "site_name=webwvs&site_mail=a%40b.com&account[name]=webwvs[mail]=a%40b.com[pass][pass1]=webwvs12X%21[pass][pass2]=webwvs12X%21" > /dev/null
curl -s -c $DRUPAL_COOKIE -b $DRUPAL_COOKIE --globoff "http://wvs.localhost/drupal/install.php?profile=standard&locale=en&op=start&id=1" > /dev/null

curl -s -c $DRUPAL_COOKIE -b $DRUPAL_COOKIE --globoff "http://wvs.localhost/drupal/install.php?profile=standard&locale=en&op=start&id=1" > /dev/null

curl -s -c $DRUPAL_COOKIE -b $DRUPAL_COOKIE --globoff "http://wvs.localhost/drupal/install.php?profile=standard&locale=en" --data "site_name=webwvs&site_mail=a%40b.com&account%5Bname%5D=webwvs&account%5Bmail%5D=a%40b.com&account%5Bpass%5D%5Bpass1%5D=webwvs12X%21&account%5Bpass%5D%5Bpass2%5D=webwvs12X%21&site_default_country=&clean_url=1&date_default_timezone=Europe%2FParis&update_status_module%5B1%5D=1&update_status_module%5B2%5D=2&form_build_id=form-jN808jUDauYLotg-cjLwwO9PVsHkC81bGfPf21Isatw&form_id=install_configure_form&op=Save+and+continue" > /dev/null
