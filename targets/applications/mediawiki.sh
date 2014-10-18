MEDIAWIKI_DATABASE="db_mediawiki"
MEDIAWIKI_DATABASE_USER="usr_mediawiki"
MEDIAWIKI_DATABASE_PASSWORD="mediawiki"

if [ -d "$INSTALL_DIR/mediawiki" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping MediaWiki installation: MediaWiki is already installed."
    	return
	fi
fi

rm -rf "$INSTALL_DIR"/mediawiki*

download http://download.wikimedia.org/mediawiki/1.21/mediawiki-1.21.2.tar.gz mediawiki.tar.gz
tar xfz $TMPDIR/mediawiki.tar.gz -C "$INSTALL_DIR" --transform "s#^mediawiki-[0-9.]*#mediawiki#"

mysql -uroot -e \
	"DROP DATABASE IF EXISTS $MEDIAWIKI_DATABASE;
	CREATE DATABASE IF NOT EXISTS $MEDIAWIKI_DATABASE;
	GRANT ALL PRIVILEGES ON "$MEDIAWIKI_DATABASE".* TO '$MEDIAWIKI_DATABASE_USER'@'localhost' IDENTIFIED BY '$MEDIAWIKI_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"

php "$INSTALL_DIR"/mediawiki/maintenance/install.php  \
  --dbname "$MEDIAWIKI_DATABASE" --dbserver localhost --dbtype mysql --dbuser "$MEDIAWIKI_DATABASE_USER" --dbpass "$MEDIAWIKI_DATABASE_PASSWORD" \
  --installdbpass "$MEDIAWIKI_DATABASE_PASSWORD" --installdbuser "$MEDIAWIKI_DATABASE_USER" --pass "$MEDIAWIKI_DATABASE_PASSWORD" \
  --scriptpath "/mediawiki" --server "http://wvs.localhost" "Webvuln Wiki" "webwvs"
