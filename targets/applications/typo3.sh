
#TYPO3_VERSION="6.0.4"

wget http://get.typo3.org/current -O $TMPDIR/typo3.tar.gz -c
tar xfz $TMPDIR/typo3.tar.gz -C $INSTALL_DIR
mv $INSTALL_DIR/typo3_* $INSTALL_DIR/typo3

wget http://get.typo3.org/dummy -O $TMPDIR/typo3dummy.tar.gz -c
tar xfz $TMPDIR/typo3dummy.tar.gz -C $INSTALL_DIR

cd $INSTALL_DIR/dummy-*
mv * $INSTALL_DIR/typo3

cd $INSTALL_DIR/typo3
touch typo3conf/ENABLE_INSTALL_TOOL


# Set apache as owner to prevent install error
sudo chown www-data:www-data * -R

# execute typo123-installer
curl -s -d "t3-install-form-input-text=root2" "wvs.localhost/t6/typo3/install/index.php?TYPO3_INSTALL[type]=config&mode=123&step=2"
curl -s -d "t3-install-123-newdatabase=db_typo3" "www.localhost/t6/typo3/install/index.php?TYPO3_INSTALL[type]=config&mode=123&step=3"
curl -s -d "password=" "wvs.localhost/t6/typo3/install/index.php?TYPO3_INSTALL[type]=database&mode=123&systemToInstall=Introduction&step=5"





