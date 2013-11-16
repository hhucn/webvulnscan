#!/bin/sh

set -e

SCRIPTDIR=$(dirname $(readlink -f $0))
APACHE_DIR="/var/www"
TMPDIR="$SCRIPTDIR/tmp"
INSTALL_DIR="$SCRIPTDIR/installed"

installPackage() {
	sudo DEBIAN_FRONTEND=noninteractive apt-get -qqy install "$@"
}

rm -rf $INSTALL_DIR
mkdir -p $INSTALL_DIR

mkdir -p "$TMPDIR"


# delete (invalid) old virtual hosts which will prevent apache from starting
if [ -d "$DIRECTORY" ]; then
	cd /etc/apache2/sites-available
	sudo rm *wvs
fi

if ! grep -q "127.0.0.1 wvs.localhost" "/etc/hosts"; then
	sudo sh -c "echo '127.0.0.1 wvs.localhost' >> /etc/hosts"
fi

# Update System
sudo apt-get -y update > /dev/null 2>&1


. ./applications/dependencies.sh

# Install applications
. ./applications/owncloud.sh
. ./applications/magento.sh
. ./applications/mediawiki.sh
. ./applications/adhocracy.sh
. ./applications/diaspora.sh


# Create index.php with links to the applications
echo '<html>
<head><title>WVS Targets</title>
<style type="text/css">li { margin-bottom: 3px; font-size: 1.5em;}</style>
</head>
<body>
<ol>
  <li><a href="./adhocracy" title="Open Adhocracy">Adhocracy</li>
  <li><a href="http://diaspora.wvs.localhost" title="Open Diaspora">Diaspora</li>
  <li><a href="./magento" title="Open Magento">Magento</li>
  <li><a href="./mediawiki" title="Open MediaWiki">MediaWiki</li>
  <li><a href="./owncloud" title="Open Owncloud">Owncloud</li>
</ol>' > $INSTALL_DIR/index.php


echo "################################################################"
echo "Please visit http://wvs.localhost to view installed applications"
