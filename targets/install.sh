#!/bin/bash -l
# login shell needed for rvm installation

set -e

SCRIPTDIR=$(dirname $(readlink -f $0))
APACHE_DIR="/var/www"
TMPDIR="$SCRIPTDIR/tmp"
INSTALL_DIR="$SCRIPTDIR/installed"
USER_HOME=$(eval echo ~${SUDO_USER})
USER_NAME=$(whoami)

declare -A APPLICATIONS
APPLICATIONS[adhocracy]=adhocracy.sh
APPLICATIONS[owncloud]=owncloud.sh 
APPLICATIONS[magento]=magento.sh 
APPLICATIONS[mediawiki]=mediawiki.sh 
APPLICATIONS[diaspora]=diaspora.sh 
APPLICATIONS[typo3]=typo3.sh 
APPLICATIONS[sugarcrm]=sugarcrm.sh 
APPLICATIONS[wordpress]=wordpress.sh 
APPLICATIONS[idempiere]=idempiere.sh 
APPLICATIONS[alfresco]=alfresco.sh 
APPLICATIONS[dokuwiki]=dokuwiki.sh 
APPLICATIONS[otrs]=otrs.sh 
APPLICATIONS[drupal]=drupal.sh 
APPLICATIONS[moodle]=moodle.sh
APPLICATIONS[ejbca]=ejbca.sh  


# Download function
# $1 - url
# $2 - destination


download() {
	wget $1 -nv -O $2
}

installPackage() {
	sudo DEBIAN_FRONTEND=noninteractive apt-get -qqy install "$@"
}
timestamp() {
  date +"%s"
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
sudo rm -f /etc/apache2/sites-enabled/*wvs.conf
sudo rm -f /etc/apache2/sites-enabled/otrs.conf

if ! grep -q "127.0.0.1 wvs.localhost" "/etc/hosts"; then
	sudo sh -c "echo '127.0.0.1 wvs.localhost' >> /etc/hosts"
fi


#sudo apt-get -y update > /dev/null 2>&1

# Install dependencies
. $SCRIPTDIR/applications/dependencies.sh

# Install the applications
if [[ -z "$1" ]]; then
	# no arguments passed.. we'll install all applications
	for x in "${!APPLICATIONS[@]}"; do 
		. $SCRIPTDIR/applications/${APPLICATIONS[${x}]}
	done
else
	while [ "$1" != "" ]; do
		if [ ${APPLICATIONS[${1}]+_} ]; then 
			. $SCRIPTDIR/applications/${APPLICATIONS[${1}]}
		else 
			echo "[ERROR] Application '${1}' unknown"; 
		fi
		shift;
	done;
fi
 
#echo 

# Update System
#sudo apt-get -y update > /dev/null 2>&1

# Install dependencies
#. $SCRIPTDIR/applications/dependencies.sh


# Install applications
	#. $SCRIPTDIR/applications/adhocracy.sh
#. $SCRIPTDIR/applications/owncloud.sh
#. $SCRIPTDIR/applications/magento.sh
#. $SCRIPTDIR/applications/mediawiki.sh
	#. $SCRIPTDIR/applications/diaspora.sh
#. $SCRIPTDIR/applications/typo3.sh
#. $SCRIPTDIR/applications/sugarcrm.sh
#. $SCRIPTDIR/applications/wordpress.sh
	#. $SCRIPTDIR/applications/idempiere.sh
	#. $SCRIPTDIR/applications/alfresco.sh
#. $SCRIPTDIR/applications/dokuwiki.sh
#. $SCRIPTDIR/applications/otrs.sh
	#. $SCRIPTDIR/applications/drupal.sh
#	. $SCRIPTDIR/applications/moodle.sh

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
  <li><a href="./dokuwiki" title="Open DokuWiki">DokuWiki</li>
  <li><a href="./otrs/index.pl" title="Open OTRS">OTRS</li>
  <li><a href="./drupal" title="Open OTRS">Drupal</li>
  <li><a href="./moodle" title="Open OTRS">Moodle</li>
  <li><a href="http://localhost:8080/share" title="Open OTRS">Alfresco</li>
</ol>' > $INSTALL_DIR/index.php

echo ""
echo ""
echo "################################################################"
echo "Please visit http://wvs.localhost to view installed applications"
echo "################################################################"
echo ""
echo ""
