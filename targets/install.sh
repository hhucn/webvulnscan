#!/bin/bash -l
# login shell needed for rvm installation

set -e

SCRIPTDIR=$(dirname $(readlink -f $0))
APACHE_DIR="/var/www"
TMPDIR="$SCRIPTDIR/tmp"
INSTALL_DIR="$SCRIPTDIR/installed"
USER_HOME=$(eval echo ~${SUDO_USER})
USER_NAME=$(whoami)
OVERWRITE_EXISTING=false

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
echo "-----------------------------------------------------"
	echo "${1##*/}"
exit
	wget $1 -nv -O $2
}

installPackage() {
	sudo DEBIAN_FRONTEND=noninteractive apt-get -qqy install "$@"
}
timestamp() {
  date +"%s"
}

while getopts "dxh?:" opt; do
    case "$opt" in
    	d)
			sudo rm -rf $INSTALL_DIR
			;;
    	x)
			OVERWRITE_EXISTING=true
			;;
	    h|\?)
			echo ""
		    echo "  Use ./install.sh <<APPLICATION NAME>> to install a specific application."
			echo "  To install all available applications simply call ./install.sh without any arguments."
			echo ""
			echo "  [Arguments]"
			echo "  -d delete all existing applications before start"
			echo "  -x overwrite existing applications"
			echo ""
			echo "  [Available applications]"
			echo "    -> ${!APPLICATIONS[@]}"
			echo ""

		    exit 0
		    ;;
    esac
done


# Check if apache user exists, if yes add this user to the group of the user who started this script
# TODO: Find better solution!
if id -u "www-data" >/dev/null 2>&1; then
	GROUP=`id -g -n $USER`
	sudo usermod -a -G $GROUP www-data
fi


mkdir -p $INSTALL_DIR
mkdir -p $TMPDIR

# delete (invalid) old virtual hosts which will prevent apache from starting
#sudo rm -f /etc/apache2/sites-enabled/wvs.conf


if ! grep -q "127.0.0.1 wvs.localhost" "/etc/hosts"; then
	sudo sh -c "echo '127.0.0.1 wvs.localhost' >> /etc/hosts"
fi

# fix 'Could not reliably determine the server's fully qualified domain name'
sudo sh -c "echo 'ServerName localhost' >> /etc/apache2/conf.d/name"

# Update System
sudo apt-get -y update > /dev/null 2>&1

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
			if [[ ${1} != -* ]]; then
				echo "[ERROR] Application '${1}' unknown"; 
			fi
		fi
		shift;
	done;
fi

# Create index.php with links to the applications
echo '<html>
<head><title>WVS Targets</title>
<style type="text/css">
	li { margin-bottom: 3px; font-size: 1.5em;}
	td { padding: 2px 5px;}
	caption { font-weight: bold; font-size: 1.125em; text-align: left; margin: 10px 0 5px 0}
	.tabTitle td { font-weight: bold; }
</style>
</head>
<body>
	<br />
	<table cellspacing=2 cellpadding=2 border=1 stlye="margin: 50px 0 0 20px;">
		<caption>Available applications</caption>
		<tr class="tabTitle">
			<td>#</td>
			<td>Application</td>
			<td style="width: 300px;">Comment</td>
		</tr>
		<tr>
			<td>01</td>
			<td><a href="./adhocracy" title="Open Adhocracy">Adhocracy</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>02</td>
			<td><a href="http://localhost:8080/share" title="Open Alfresco">Alfresco</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>03</td>
			<td><a href="http://diaspora.wvs.localhost" title="Open Diaspora">Diaspora</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>04</td>
			<td><a href="./dokuwiki" title="Open DokuWiki">DokuWiki</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>05</td>
			<td><a href="./drupal" title="Open Drupal">Drupal</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>06</td>
			<td><a href="#" title="Open EJBCA">EJBCA</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>07</td>
			<td><a href="#" title="Open iDempiere">iDempiere</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>08</td>
			<td><a href="./magento" title="Open Magento">Magento</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>09</td>
			<td><a href="./mediawiki" title="Open MediaWiki">MediaWiki</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>10</td>
			<td><a href="./moodle" title="Open Moodle">Moodle</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>11</td>
			<td><a href="./otrs/index.pl" title="Open OTRS">OTRS</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>12</td>
			<td><a href="./owncloud" title="Open Owncloud">Owncloud</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>13</td>
			<td><a href="./sugarcrm" title="Open SugarCRM">SugarCRM</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>14</td>
			<td><a href="./typo3" title="Open Typo3">Typo3</a></td>
			<td>&nbsp;</td>
		</tr>
		<tr>
			<td>15</td>
			<td><a href="./wordpress" title="Open Wordpress">Wordpress</a></td>
			<td>&nbsp;</td>
		</tr>
	</table>
</html>
<p style="font-weight: bold">Please note: If not other specified, the login for every application is webwvs // webwvs12</p>
' > $INSTALL_DIR/index.php

echo ""
echo ""
echo "################################################################"
echo "Please visit http://wvs.localhost to view installed applications"
echo "################################################################"
echo ""
echo ""
