
TYPO3_VERSION="6.1.5"

wget http://downloads.sourceforge.net/project/typo3/TYPO3%20Source%20and%20Dummy/TYPO3%20$TYPO3_VERSION/typo3_src%2Bdummy-$TYPO3_VERSION.zip -O $TMPDIR/typo3.zip -c

unzip $TMPDIR/typo3.zip -d $INSTALL_DIR -qq
mv $INSTALL_DIR/typo3_* $INSTALL_DIR/typo3

cd $INSTALL_DIR/typo3
touch typo3conf/ENABLE_INSTALL_TOOL
