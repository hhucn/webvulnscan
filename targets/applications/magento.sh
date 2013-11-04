MAGENTO_DATABASE="db_magento"
MAGENTO_DATABASE_USER="usr_magento"
MAGENTO_DATABASE_PASSWORD="magento"
MAGENTO_ADMIN_USERNAME="admin"
MAGENTO_ADMIN_PASSWORD="magento123"
MAGENTO_URL="localhost/magento/"
MAGENTO_VERSION="1.8.0.0"
MAGENTO_SAMPLEDATA_VERSION="1.6.1.0"

# get Magento and sample data -- Using a private mirror during development to avoid extreme low speeds on magentocommerce
wget http://www.magentocommerce.com/downloads/assets/$MAGENTO_VERSION/magento-$MAGENTO_VERSION.tar.gz -O $TMPDIR/magento.tar.gz -c
tar xfz $TMPDIR/magento.tar.gz -C $APACHE_DIR

wget http://www.magentocommerce.com/downloads/assets/$MAGENTO_SAMPLEDATA_VERSION/magento-sample-data-$MAGENTO_SAMPLEDATA_VERSION.tar.gz -O $TMPDIR/magento-sample-data.tar.gz
tar xfz $TMPDIR/magento-sample-data.tar.gz -C $APACHE_DIR/magento/media/

mysql -uroot -e "
    CREATE DATABASE IF NOT EXISTS $MAGENTO_DATABASE;
    GRANT ALL PRIVILEGES ON "$MAGENTO_DATABASE".* TO '$MAGENTO_DATABASE_USER'@'localhost' IDENTIFIED BY '$MAGENTO_DATABASE_PASSWORD';
    FLUSH PRIVILEGES;"

mysql -u$MAGENTO_DATABASE_USER -p$MAGENTO_DATABASE_PASSWORD $MAGENTO_DATABASE < $APACHE_DIR/magento/media/magento-sample-data-$MAGENTO_SAMPLEDATA_VERSION/magento_sample_data_for_$MAGENTO_SAMPLEDATA_VERSION.sql
chown -R www-data:www-data $APACHE_DIR/magento
chmod a+x $APACHE_DIR/magento/mage

cd $APACHE_DIR/magento
./mage mage-setup .
./mage config-set preferred_state stable
./mage install http://connect20.magentocommerce.com/community Mage_All_Latest --force
cd -

# set apache user as owner for cache folder - if it exists
if [ -d "var/cache" ]; then
	chown -R www-data:www-data var/cache
fi

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
    --admin_password "$MAGENTO_ADMIN_PASSWORD" > /dev/null
