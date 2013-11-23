#!/bin/sh

set -e

SCRIPTDIR=$(dirname $(readlink -f $0))
APACHE_DIR="/var/www"
TMPDIR="$SCRIPTDIR/tmp"
INSTALL_DIR="$SCRIPTDIR/installed"

installPackage() {
	sudo DEBIAN_FRONTEND=noninteractive apt-get -qqy install "$@"
}



# Check if apache user exists, if yes add this user to the group of the user who started this script
# TODO: Find better solution!
if id -u "www-data" >/dev/null 2>&1; then
	GROUP=`id -g -n $USER`
	sudo usermod -a -G $GROUP www-data
fi

#rm -rf $INSTALL_DIR
#mkdir -p $INSTALL_DIR

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


#. ./applications/dependencies.sh

# Install applications
. ./applications/owncloud.sh
. ./applications/magento.sh
. ./applications/mediawiki.sh
. ./applications/adhocracy.sh
. ./applications/diaspora.sh
. ./applications/typo3.sh
. ./applications/sugarcrm.sh

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
  <li><a href="./typo3" title="Open Typo3">Typo3</li>
  <li><a href="./sugarcrm" title="Open SugarCRM">SugarCRM</li>
</ol>' > $INSTALL_DIR/index.php


echo "################################################################"
echo "Please visit http://wvs.localhost to view installed applications"
