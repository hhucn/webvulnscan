sudo rm -rf $INSTALL_DIR/dokuwiki*
sudo rm -rf $TMP_DIR/dokuwiki*

wget http://download.dokuwiki.org/src/dokuwiki/dokuwiki-stable.tgz -nv -O $TMPDIR/dokuwiki-stable.tgz -c
tar xfz $TMPDIR/dokuwiki-stable.tgz -C $INSTALL_DIR --transform "s#^dokuwiki-[0-9.]*[0-9.]*[0-9.]*#dokuwiki#"

sudo chmod 755 $INSTALL_DIR/dokuwiki-12-08/ -R

cd $INSTALL_DIR/dokuwiki-12-08/
sudo chown www-data:www-data lib/plugins -R
sudo chown www-data:www-data data -R
sudo chown www-data:www-data conf -R

curl -c /tmp/cookieDokuWiki -b /tmp/cookieDokuWiki --globoff "http://wvs.localhost/dokuwiki-12-08/install.php" --data "l=en&d[acl]=on&d[title]=WebvulnWiki&d[superuser]=wvs&d[fullname]=wvs&d[email]=a@b.com&d[password]=wvs&d[confirm]=wvs&d[policy]=0&d[allowreg]=on&d[license]=cc-by-sa&d[pop]=on&submit=Save"

sudo rm install.php
