# Use the standard values for later login:
# username: root@localhost
# password: root

OTRS_VERSION="3.3.5"
OTRS_DIR=$INSTALL_DIR/otrs
OTRS_DATABASE="otrs"
OTRS_DATABASE_USER="otrs"
OTRS_DATABASE_PASSWORD="otrs"

if [ -d "$OTRS_DIR" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping OTRS installation: OTRS is allready installed."
    	return
	fi
fi

sudo rm -rf $OTRS_DIR*
sudo rm -rf $TMP_DIR/otrs*
sudo rm -f /etc/apache2/conf.d/otrs.conf

# remove old vhosts file
sudo rm -f /etc/apache2/sites-enabled/otrs.conf

download http://ftp.otrs.org/pub/otrs/otrs-$OTRS_VERSION.tar.gz otrs-$OTRS_VERSION.tar.gz
tar xfz $TMPDIR/otrs-$OTRS_VERSION.tar.gz -C $INSTALL_DIR --transform "s#^otrs-[0-9.]*#otrs#"

# Create User and Group
id -u otrs &>/dev/null || sudo useradd -r -d $OTRS_DIR -c 'OTRS user' otrs
id -u otrs &>/dev/null || sudo usermod -a -G www-data otrs

# setup apache and other config files
cd $OTRS_DIR/Kernel
cp Config.pm.dist Config.pm
cp Config/GenericAgent.pm.dist Config/GenericAgent.pm

sed -e "s#/opt/otrs#$OTRS_DIR#g" $OTRS_DIR/scripts/apache2-httpd.include.conf \
    | sudo tee /etc/apache2/sites-available/otrs.conf >/dev/null

sed -i -e "s#/opt/otrs#$OTRS_DIR#g" $OTRS_DIR/scripts/apache2-httpd.include.conf
sed -i -e "s#/opt/otrs#$OTRS_DIR#g" $OTRS_DIR/scripts/apache2-perl-startup.pl

sed -i -e 's#/opt/otrs#'$OTRS_DIR'#g' \
       -e 's#some-pass#'otrs'#g' \
	$OTRS_DIR/Kernel/Config.pm

# setup cronjobs
cd $OTRS_DIR/var/cron
for foo in *.dist; do cp $foo `basename $foo .dist`; done

# setup database
cd $OTRS_DIR/scripts/database
mysql -uroot -e "
    DROP DATABASE IF EXISTS $OTRS_DATABASE;
    CREATE DATABASE IF NOT EXISTS $OTRS_DATABASE;
    GRANT ALL PRIVILEGES ON "$OTRS_DATABASE".* TO '$OTRS_DATABASE_USER'@'localhost' IDENTIFIED BY '$OTRS_DATABASE_PASSWORD';
    FLUSH PRIVILEGES;"

mysql -uroot $OTRS_DATABASE < otrs-schema.mysql.sql
mysql -uroot $OTRS_DATABASE < otrs-initial_insert.mysql.sql
mysql -uroot $OTRS_DATABASE < otrs-schema-post.mysql.sql


# set permissions
cd $OTRS_DIR/bin/
#sudo ./otrs.SetPermissions.pl $OTRS_DIR --otrs-user=otrs --web-user=www-data --otrs-group=www-data --web-group=www-data
sudo ./otrs.SetPermissions.pl --otrs-user=otrs --web-user=www-data --otrs-group=otrs --web-group=www-data $OTRS_DIR
#sudo chown user:www-data $OTRS_DIR/ -R
#sudo chmod g+rw $OTRS_DIR/ -R
#sudo chown user:www-data $OTRS_DIR/ -R
#sudo chmod g+rw $OTRS_DIR/ -R


sudo a2ensite otrs.conf > /dev/null
sudo /etc/init.d/apache2 restart > /dev/null

sudo $OTRS_DIR/bin/Cron.sh start otrs

# Set init Script
sudo sed -e "s#/opt/otrs#$OTRS_DIR#g" $OTRS_DIR/scripts/otrs-scheduler-linux \
    | sudo tee /etc/init.d/otrs >/dev/null
sudo chmod a+x /etc/init.d/otrs

sudo chkconfig otrs --add

sudo /etc/init.d/otrs start

