MAGENTO_DATABASE="db_magento"
MAGENTO_DATABASE_USER="usr_magento"
MAGENTO_DATABASE_PASSWORD="magento"
MAGENTO_ADMIN_USERNAME="admin"
MAGENTO_ADMIN_PASSWORD="magento123"
MAGENTO_URL="wvs.localhost/magento"
MAGENTO_VERSION="1.9.0.1"
MAGENTO_SAMPLEDATA_VERSION="1.9.0.0"


if [ -d "$INSTALL_DIR/magento" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping Magento installation: Magento is already installed."
    	return
	fi
fi

sudo rm -rf $INSTALL_DIR/magento

download http://www.magentocommerce.com/downloads/assets/$MAGENTO_VERSION/magento-$MAGENTO_VERSION.tar.gz magento.tar.gz
tar xfz $TMPDIR/magento.tar.gz -C $INSTALL_DIR

download http://www.magentocommerce.com/downloads/assets/$MAGENTO_SAMPLEDATA_VERSION/magento-sample-data-$MAGENTO_SAMPLEDATA_VERSION.tar.gz magento-sample-data.tar.gz
tar xfz $TMPDIR/magento-sample-data.tar.gz -C $TMPDIR
rsync -av $TMPDIR/magento-sample-data-$MAGENTO_SAMPLEDATA_VERSION/media $INSTALL_DIR/magento/media/
rsync -av $TMPDIR/magento-sample-data-$MAGENTO_SAMPLEDATA_VERSION/skin $INSTALL_DIR/magento/skin/

mysql -uroot -e "
    DROP DATABASE IF EXISTS $MAGENTO_DATABASE;
    CREATE DATABASE IF NOT EXISTS $MAGENTO_DATABASE;
    GRANT ALL PRIVILEGES ON "$MAGENTO_DATABASE".* TO '$MAGENTO_DATABASE_USER'@'localhost' IDENTIFIED BY '$MAGENTO_DATABASE_PASSWORD';
    FLUSH PRIVILEGES;"

mysql -u$MAGENTO_DATABASE_USER -p$MAGENTO_DATABASE_PASSWORD $MAGENTO_DATABASE < $TMPDIR/magento-sample-data-$MAGENTO_SAMPLEDATA_VERSION/magento_sample_data_for_$MAGENTO_SAMPLEDATA_VERSION.sql

sudo chmod a+x $INSTALL_DIR/magento/mage

cd $INSTALL_DIR/magento
./mage mage-setup .
./mage config-set preferred_state stable
./mage install http://connect20.magentocommerce.com/community Mage_All_Latest --force

php -f install.php -- \
    --license_agreement_accepted "yes" \
    --locale "de_DE" \
    --timezone "Europe/Berlin" \
    --default_currency "EUR" \
    --db_host "localhost" \
    --db_name "$MAGENTO_DATABASE" \
    --db_user "$MAGENTO_DATABASE_USER" \
    --db_pass "$MAGENTO_DATABASE_PASSWORD" \
    --url "$MAGENTO_URL" \
    --use_rewrites "yes" \
    --use_secure "no" \
    --secure_base_url "" \
    --use_secure_admin "no" \
    --admin_firstname "Webvulnscan" \
    --admin_lastname "Test" \
    --admin_email "test@example.com" \
    --admin_username "$MAGENTO_ADMIN_USERNAME" \
    --admin_password "$MAGENTO_ADMIN_PASSWORD"

sudo chown www-data:www-data $INSTALL_DIR/magento/ -R
