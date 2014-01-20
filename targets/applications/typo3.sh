
#TYPO3_VERSION="6.0.4"
TYPO3_DATABASE="db_typo3"
TYPO3_DATABASE_USER="usr_typo3"
TYPO3_DATABASE_PASSWORD="typo3"
TYPO3_INSTALL_PASSWORD="typo3"
TYPO3_ADMIN_PASSWORD="typo3"

sudo rm -rf $INSTALL_DIR/typo3
sudo rm -rf $TMP_DIR/typo3*

wget http://get.typo3.org/introduction -O $TMPDIR/typo3.tar.gz -c
tar xfz $TMPDIR/typo3.tar.gz -C $INSTALL_DIR
mv -f $INSTALL_DIR/introduction* $INSTALL_DIR/typo3

#cd $INSTALL_DIR/dummy-*
#rm -rf index.php typo3_src t3lib typo3
#mv * $INSTALL_DIR/typo3
#rm -rf $INSTALL_DIR/dummy*

cd $INSTALL_DIR/typo3
touch typo3conf/ENABLE_INSTALL_TOOL

# Set apache as owner to prevent install error
sudo chown www-data:www-data $INSTALL_DIR/typo3 -R

mysql -uroot -e "
    DROP DATABASE IF EXISTS $TYPO3_DATABASE;
    CREATE DATABASE IF NOT EXISTS $TYPO3_DATABASE;
    GRANT ALL PRIVILEGES ON "$TYPO3_DATABASE".* TO '$TYP3O_DATABASE_USER'@'localhost' IDENTIFIED BY '$TYPO3_DATABASE_PASSWORD';
    FLUSH PRIVILEGES;"

curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/typo3/typo3/install/index.php?mode=123&step=1&password=joh316"
curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/typo3/typo3/install/index.php?mode=123&step=1&password=joh316"
curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/typo3/typo3/install/index.php?mode=123&TYPO3_INSTALL[type]=config&step=1" --data "step=2"
curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/typo3/typo3/install/index.php?mode=123&TYPO3_INSTALL[type]=config&step=2" --data "step=3&TYPO3_INSTALL%5BLocalConfiguration%5D%5BencryptionKey%5D=9667c057098d391c0d7d1b1f0dd4ec8ae07399b4faec9a0c1a8c4500fd4f0a23d5e8251a6327f8778052078a71df9294&TYPO3_INSTALL%5BLocalConfiguration%5D%5Bcompat_version%5D=6&TYPO3_INSTALL%5BDatabase%5D%5Btypo_db_driver%5D=mysql&TYPO3_INSTALL%5BDatabase%5D%5Btypo_db_username%5D=usr_typo3&TYPO3_INSTALL%5BDatabase%5D%5Btypo_db_password%5D=typo3&TYPO3_INSTALL%5BDatabase%5D%5Btypo_db_host%5D=localhost"
curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/typo3/typo3/install/index.php?mode=123&TYPO3_INSTALL[type]=config&step=3" --data "step=4&TYPO3_INSTALL%5Bdb_select_option%5D=EXISTING&TYPO3_INSTALL%5BDatabase%5D%5Btypo_db%5D=db_typo3"
curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/typo3/typo3/install/index.php?mode=123&TYPO3_INSTALL[type]=database&step=4"
curl -c /tmp/cookie -b /tmp/cookie "http://wvs.localhost/typo3/typo3/install/index.php?mode=123&TYPO3_INSTALL[type]=database&step=5" --data "systemToInstall=Introduction&TYPO3_INSTALL%5Bdatabase_type%5D=import%7CCURRENT_TABLES%2BSTATIC&TYPO3_INSTALL%5Bdatabase_import_all%5D=1"
curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/typo3/typo3/install/index.php?mode=123&TYPO3_INSTALL[type]=database&step=5&systemToInstall=Introduction"
curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/typo3/typo3/install/index.php?mode=123&TYPO3_INSTALL[type]=database&step=5&subpackage=Introduction"
curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/typo3/typo3/install/index.php?mode=123&TYPO3_INSTALL[type]=database&step=6" --data "password=typo3&useRealURL=1&colorPicker=%23F18F0B"


