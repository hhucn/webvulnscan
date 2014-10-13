
MEDIAWIKI_SERVER="http://wvs.localhost"
MEDIAWIKI_DATABASE="db_mediawiki"
MEDIAWIKI_DATABASE_USER="usr_mediawiki"
MEDIAWIKI_DATABASE_PASSWORD="mediawiki"

if [ -d "$INSTALL_DIR/mediawiki" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping MediaWiki installation: MediaWiki is already installed."
    	return
	fi
fi

MEDIAWIKI_COOKIE=$(mktemp $TMPDIR/XXXXXX)

rm -rf $INSTALL_DIR/mediawiki*

download http://download.wikimedia.org/mediawiki/1.21/mediawiki-1.21.2.tar.gz mediawiki.tar.gz
tar xfz $TMPDIR/mediawiki.tar.gz -C $INSTALL_DIR --transform "s#^mediawiki-[0-9.]*#mediawiki#"

mysql -uroot -e \
	"DROP DATABASE IF EXISTS $MEDIAWIKI_DATABASE;
	CREATE DATABASE IF NOT EXISTS $MEDIAWIKI_DATABASE;
	GRANT ALL PRIVILEGES ON "$MEDIAWIKI_DATABASE".* TO '$MEDIAWIKI_DATABASE_USER'@'localhost' IDENTIFIED BY '$MEDIAWIKI_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"

#mysql -u$MEDIAWIKI_DATABASE_USER -p$MEDIAWIKI_DATABASE_PASSWORD $MEDIAWIKI_DATABASE < $INSTALL_DIR/mediawiki/maintenance/tables.sql
#mysql -u$MEDIAWIKI_DATABASE_USER -p$MEDIAWIKI_DATABASE_PASSWORD $MEDIAWIKI_DATABASE < /tmp/path

#http://wvs.localhost/mediawiki/mw-config/index.php


TS=$(wget -q 'http://wvs.localhost/mediawiki/mw-config/index.php' -O -| sed 's/.*name="LanguageRequestTime" value="\([0-9]*\)".*/\1/')


curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Language' --data 'LanguageRequestTime='$TS'&uselang=en&ContLang=en&submit-continue=Continue+%E2%86%92'

#curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=ExistingWiki' 
#curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Welcome'

curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Welcome' --data 'submit-continue=Continue+%E2%86%92'
#curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=DBConnect'

curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=DBConnect' --data 'DBType=mysql&mysql_wgDBserver=localhost&mysql_wgDBname=db_mediawiki&mysql_wgDBprefix=&mysql__InstallUser=usr_mediawiki&mysql__InstallPassword=mediawiki&submit-continue=Continue+%E2%86%92'
curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Upgrade'
#curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=DBSettings'

curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=DBSettings' --data 'mysql__SameAccount=1&mysql_wgDBuser=wikiuser&mysql_wgDBpassword=&mysql__MysqlEngine=InnoDB&mysql__MysqlCharset=utf8&submit-continue=Continue+%E2%86%92'
#curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Name' 

curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Name' --data 'config_wgSitename=Webvuln+Wiki&config__NamespaceType=site-name&config_wgMetaNamespace=MyWiki&config__AdminName=webwvs&config__AdminPassword=webwvs12&config__AdminPassword2=webwvs12&config__AdminEmail=a%40b.com&config__SkipOptional=continue&submit-continue=Continue+%E2%86%92'
#curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Options' 

curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Options' --data 'config__RightsProfile=wiki&config__LicenseCode=none&config_wgEnableEmail=1&config_wgPasswordSender=apache%40wvs.localhost&config_wgEnableUserEmail=1&config_wgEmailAuthentication=1&config_ext-Cite=1&config_ext-ConfirmEdit=1&config_ext-Gadgets=1&config_ext-ImageMap=1&config_ext-InputBox=1&config_ext-Interwiki=1&config_ext-LocalisationUpdate=1&config_ext-Nuke=1&config_ext-ParserFunctions=1&config_ext-PdfHandler=1&config_ext-Poem=1&config_ext-Renameuser=1&config_ext-SpamBlacklist=1&config_ext-SyntaxHighlight_GeSHi=1&config_ext-TitleBlacklist=1&config_ext-Vector=1&config_ext-WikiEditor=1&config_wgEnableUploads=1&config_wgDeletedDirectory=%2Fhome%2Fuser%2Fdev%2Fwebvulnscan%2Ftargets%2Finstalled%2Fmediawiki%2Fimages%2Fdeleted&config_wgLogo=%24wgStylePath%2Fcommon%2Fimages%2Fwiki.png&config_wgMainCacheType=none&config__MemCachedServers=&submit-continue=Continue+%E2%86%92'
#curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Install' 

curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Install' --data 'submit-continue=Continue+%E2%86%92'

curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Install' --data 'LiveLog=&submit-continue=Continue+%E2%86%92'
curl -c $MEDIAWIKI_COOKIE -b $MEDIAWIKI_COOKIE --globoff 'http://wvs.localhost/mediawiki/mw-config/index.php?page=Complete'


exit
cp $SCRIPTDIR/applications/mediawiki.conf $INSTALL_DIR/mediawiki/LocalSettings.php

#sudo chown -R www-data:www-data $INSTALL_DIR/mediawiki

sed -i -e 's#XXX_SCRIPTPATH_XXX#'mediawiki'#g' \
       -e 's#XXX_SERVER_XXX#'$MEDIAWIKI_SERVER'#g' \
       -e 's#XXX_DBNAME_XXX#'$MEDIAWIKI_DATABASE'#g' \
       -e 's#XXX_DBUSER_XXX#'$MEDIAWIKI_DATABASE_USER'#g' \
       -e 's#XXX_DBPASS_XXX#'$MEDIAWIKI_DATABASE_PASSWORD'#g' \
	$INSTALL_DIR/mediawiki/LocalSettings.php
