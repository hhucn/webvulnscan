DOKUWIKI_NAME="WebvulnWiki"
DOKUWIKI_SERVER="http://wvs.localhost"
DOKU_DATABASE="db_dokuwiki"
DOKUWIKI_DATABASE_USER="usr_dokuwiki"
DOKUWIKI_DATABASE_PASSWORD="dokuwiki"


wget http://download.dokuwiki.org/src/dokuwiki/dokuwiki-stable.tgz -nv -O $TMPDIR/dokuwiki-stable.tgz -c
tar xfz $TMPDIR/dokuwiki-stable.tgz -C $INSTALL_DIR --transform "s#^dokuwiki-[0-9.]*[0-9.]*[0-9.]*#dokuwiki#"

sudo chmod 755 $INSTALL_DIR/dokuwiki-12-08/ -R

cd $INSTALL_DIR/dokuwiki-12-08/
sudo chown www-data:www-data lib/plugins -R
sudo chown www-data:www-data data -R


