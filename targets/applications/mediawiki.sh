
MEDIAWIKI_WIKI_NAME="WebvulnWiki"
MEDIAWIKI_SERVER="http://localhost"
MEDIAWIKI_DATABASE="db_mediawiki"
MEDIAWIKI_DATABASE_USER="usr_mediawiki"
MEDIAWIKI_DATABASE_PASSWORD="mediawiki"

wget http://download.wikimedia.org/mediawiki/1.21/mediawiki-1.21.2.tar.gz -nv -O- | \
	tar xfz - -C $APACHE_DIR --transform "s#^mediawiki-[0-9.]*/#mediawiki/#"

mysql -uroot -e \
	"CREATE DATABASE IF NOT EXISTS $MEDIAWIKI_DATABASE;
	GRANT ALL PRIVILEGES ON "$MEDIAWIKI_DATABASE".* TO '$MEDIAWIKI_DATABASE_USER'@'localhost' IDENTIFIED BY '$MEDIAWIKI_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"
