 #!/bin/bash

### Configuration
MAGENTO_DATABASE="db_magento"
MAGENTO_DATABASE_USER="usr_magento"
MAGENTO_DATABASE_PASSWORD="magento"
MAGENTO_ADMIN_USERNAME="admin"
MAGENTO_ADMIN_PASSWORD="magento"
MAGENTO_URL="localhost/"
MAGENTO_VERSION="1.8.0.0"
MAGENTO_SAMPLEDATA_VERSION="1.6.1.0"

echo "Installing Magento with sample data"

# get Magento and sample data -- Using a private mirror during development to avoid extreme low speeds on magentocommerce
cd $SCRIPT_TMP_FOLDER
#wget http://www.magentocommerce.com/downloads/assets/1.8.0.0/magento-1.8.0.0.tar.gz 
#wget http://www.magentocommerce.com/downloads/assets/1.6.1.0/magento-sample-data-1.6.1.0.tar.gz 
wget http://www.vg-dev.de/magento/magento-$MAGENTO_VERSION.tar.gz -o /dev/null
wget http://www.vg-dev.de/magento/magento-sample-data-$MAGENTO_SAMPLEDATA_VERSION.tar.gz -o /dev/null

echo "--- extracting files..."
tar xfz magento-$MAGENTO_VERSION.tar.gz -C $APACHE_DIR > /dev/null
tar xfz magento-sample-data-$MAGENTO_SAMPLEDATA_VERSION.tar.gz > /dev/null

echo "--- creating database and user"
SQL1="CREATE DATABASE IF NOT EXISTS $MAGENTO_DATABASE;"
SQL2="GRANT ALL PRIVILEGES ON "$MAGENTO_DATABASE".* TO '$MAGENTO_DATABASE_USER'@'localhost' IDENTIFIED BY '$MAGENTO_DATABASE_PASSWORD';"
SQL3="FLUSH PRIVILEGES;"
mysql -uroot -p$MYSQL_ROOT_PASSWORD -e "${SQL1}${SQL2}${SQL3}"

echo "--- configuring apache2"


echo "--- importing sample data"
cd $SCRIPT_TMP_FOLDER/magento-sample-data-$MAGENTO_SAMPLEDATA_VERSION
mysql -h localhost -u$MAGENTO_DATABASE_USER -p$MAGENTO_DATABASE_PASSWORD $MAGENTO_DATABASE < magento_sample_data_for_$MAGENTO_SAMPLEDATA_VERSION.sql
sudo mv media/* $APACHE_DIR/magento/media


exit

echo "--- setting permissions"
cd $apacheDir/magento
chmod 550 mage
chmod 777 -R var/cache

echo "--- preparing installation"
# remove possible existing cache files (to prevent a ZEND exception during install)
rm -rf var/session var/cache
./mage mage-setup .
./mage config-set preferred_state stable
./mage install http://connect20.magentocommerce.com/community Mage_All_Latest --force
php -f shell/indexer.php reindexall

echo "--- installing magneto"
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
