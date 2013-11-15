MAGENTO_DATABASE="db_magento"
MAGENTO_DATABASE_USER="usr_magento"
MAGENTO_DATABASE_PASSWORD="magento"
MAGENTO_ADMIN_USERNAME="admin"
MAGENTO_ADMIN_PASSWORD="magento123"
MAGENTO_URL="wvs.localhost/magento/"
MAGENTO_VERSION="1.8.0.0"
MAGENTO_SAMPLEDATA_VERSION="1.6.1.0"

rm -rf $INSTALL_DIR/magento

wget http://www.magentocommerce.com/downloads/assets/$MAGENTO_VERSION/magento-$MAGENTO_VERSION.tar.gz -O $TMPDIR/magento.tar.gz -c
tar xfz $TMPDIR/magento.tar.gz -C $INSTALL_DIR

wget http://www.magentocommerce.com/downloads/assets/$MAGENTO_SAMPLEDATA_VERSION/magento-sample-data-$MAGENTO_SAMPLEDATA_VERSION.tar.gz -O $TMPDIR/magento-sample-data.tar.gz -c
tar xfz $TMPDIR/magento-sample-data.tar.gz -C $INSTALL_DIR/magento/media/

mysql -uroot -e "
    DROP DATABASE IF EXISTS $MAGENTO_DATABASE;
    CREATE DATABASE IF NOT EXISTS $MAGENTO_DATABASE;
    GRANT ALL PRIVILEGES ON "$MAGENTO_DATABASE".* TO '$MAGENTO_DATABASE_USER'@'localhost' IDENTIFIED BY '$MAGENTO_DATABASE_PASSWORD';
    FLUSH PRIVILEGES;"

mysql -u$MAGENTO_DATABASE_USER -p$MAGENTO_DATABASE_PASSWORD $MAGENTO_DATABASE < $INSTALL_DIR/magento/media/magento-sample-data-$MAGENTO_SAMPLEDATA_VERSION/magento_sample_data_for_$MAGENTO_SAMPLEDATA_VERSION.sql

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
