
#TYPO3_VERSION="6.0.4"
TYPO3_DATABASE="db_typo3"
TYPO3_DATABASE_USER="usr_typo3"
TYPO3_DATABASE_PASSWORD="typo3"
TYPO3_INSTALL_PASSWORD="typo3"

sudo rm -rf $INSTALL_DIR/typo3
sudo rm -rf $TMP_DIR/typo3*

wget http://get.typo3.org/introduction -O $TMPDIR/typo3.tar.gz -c
tar xfz $TMPDIR/typo3.tar.gz -C $INSTALL_DIR
mv -f $INSTALL_DIR/introduction* $INSTALL_DIR/typo3


#wget http://get.typo3.org/current -O $TMPDIR/typo3.tar.gz -c
#tar xfz $TMPDIR/typo3.tar.gz -C $INSTALL_DIR
#mv -f $INSTALL_DIR/typo3_* $INSTALL_DIR/typo3

#wget http://get.typo3.org/dummy -O $TMPDIR/typo3dummy.tar.gz -c
#tar xfz $TMPDIR/typo3dummy.tar.gz -C $INSTALL_DIR

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


# Create config file
wget --spider "http://wvs.localhost/typo3/typo3/install/index.php?mode=123&step=1&password=joh316"

sed_search="'extTables.php',"
sed_append="'host' => 'localhost', 'password' => 'typo3', 'username' => 'usr_typo3',"
sudo sed -i "/$sed_search/a\ $sed_append" $INSTALL_DIR/typo3/typo3conf/LocalConfiguration.php

#curl --globoff --data "systemToInstall=Introduction" "http://wvs.localhost/typo3/typo3/install/index.php?TYPO3_INSTALL[type]=database&mode=123&step=5&subpackage=Introduction&password=joh316"






#curl --globoff --data "t3-install-form-username=usr_typo3&t3-install-form-password=typo3&t3-install-form-host=localhost" "http://wvs.localhost/typo3/typo3/install/index.php?TYPO3_INSTALL[type]=database&mode=123&step=2&password=joh316"



#sudo wget --spider --keep-session-cookies --save-cookies cookies.txt --post-data "t3-install-password=$TYPO3_INSTALL_PASSWORD&t3-install-password-repeat=$TYPO3_INSTALL_PASSWORD" "http://wvs.localhost/typo3/typo3/install/index.php?TYPO3_INSTALL[type]=extConfig"

#sudo wget --spider --keep-session-cookies --save-cookies cookies.txt --post-data "t3-install-password=$TYPO3_INSTALL_PASSWORD&t3-install-password-repeat=$TYPO3_INSTALL_PASSWORD" "http://wvs.localhost/typo3/typo3/install/index.php?TYPO3_INSTALL[type]=extConfig"

#sudo wget --spider --keep-session-cookies --save-cookies cookies.txt --post-data "t3-install-form-username=$TYPO3_DATABASE_USER&t3-install-form-password=$TYPO3_DATABASE_PASSWORD&t3-install-form-host=localhost&t3-install-form-encryptionkey=83b18432e5daad1ecc2390ddd6224c73e62577e66214db6689e1369a8bf4a30ac8b4c343379585fb0d1074a7ed2dc5e3" "http://wvs.localhost/typo3/typo3/install/index.php?TYPO3_INSTALL[type]=config"

#echo curl --globoff --data "t3-install-password=$TYPO3_INSTALL_PASSWORD&t3-install-password-repeat=$TYPO3_INSTALL_PASSWORD" "http://wvs.localhost/typo3/typo3/install/index.php?TYPO3_INSTALL[type]=extConfig"


#echo curl --globoff --data "t3-install-form-password=$TYPO3_INSTALL_PASSWORD" "http://wvs.localhost/typo3/typo3/install/index.php?TYPO3_INSTALL[type]=extConfig"



# execute typo123-installer
#curl -s -d "t3-install-form-input-text=root2" "wvs.localhost/t6/typo3/install/index.php?TYPO3_INSTALL[type]=config&mode=123&step=2"
#curl -s -d "t3-install-123-newdatabase=db_typo3" "www.localhost/t6/typo3/install/index.php?TYPO3_INSTALL[type]=config&mode=123&step=3"
#curl -s -d "password=" "wvs.localhost/t6/typo3/install/index.php?TYPO3_INSTALL[type]=database&mode=123&systemToInstall=Introduction&step=5"





