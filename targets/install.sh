#!/bin/bash

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

sudo rm -rf $INSTALL_DIR
mkdir -p $INSTALL_DIR

mkdir -p "$TMPDIR"


# delete (invalid) old virtual hosts which will prevent apache from starting
wvs_vhosts=(/etc/apache2/sites-available/*wvs.conf)
wvs_vhosts_len=${#wvs_vhosts[@]}

for (( i=0; i<${wvs_vhosts_len}; i++ ));
do
	f=${wvs_vhosts[$i]}
	filename=${f##*/}
	
	if ! [ "$filename" == "*wvs.conf" ]; then
		echo $filename "processing............:"
		#sudo a2dissite $filename > /dev/null   #"${filename:0:-5}"
		#sudo rm -rf /etc/apache2/sites-available/$filename
		#sudo rm -rf /etc/apache2/sites-enables/$filename
	fi
done

if ! grep -q "127.0.0.1 wvs.localhost" "/etc/hosts"; then
	sudo sh -c "echo '127.0.0.1 wvs.localhost' >> /etc/hosts"
fi

# Update System
sudo apt-get -y update > /dev/null 2>&1

# Install dependencies
. $SCRIPTDIR/applications/dependencies.sh

# Install applications
. $SCRIPTDIR/applications/owncloud.sh
. $SCRIPTDIR/applications/magento.sh
. $SCRIPTDIR/applications/mediawiki.sh
. $SCRIPTDIR/applications/adhocracy.sh
. $SCRIPTDIR/applications/diaspora.sh
. $SCRIPTDIR/applications/typo3.sh
. $SCRIPTDIR/applications/sugarcrm.sh
. $SCRIPTDIR/applications/wordpress.sh

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
  <li><a href="./wordpress" title="Open Wordpress">Wordpress</li>
</ol>' > $INSTALL_DIR/index.php


echo "################################################################"
echo "Please visit http://wvs.localhost to view installed applications"
