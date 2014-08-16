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

isInstalled(){
    if [[ -d "$INSTALL_DIR/$1" ]] && [[ -n "$INSTALL_DIR/$1" ]] ; then
        return 0
    else
        return 1
    fi
}

buildIndex() {
OUTPUT='<html>
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
				<td>Status</td>
				<td style="width: 300px;">Comment</td>
			</tr>
			<tr><td>01</td>'
	if isInstalled "adhocracy"; then
		OUTPUT=$OUTPUT.'<td><a href="./adhocracy" title="Open Adhocracy">Adhocracy</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>Adhocracy</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>02</td>'
	if isInstalled "alfresco-4.2.1"; then
		OUTPUT=$OUTPUT.'<td><a href="http://localhost:8080/share" title="Open Alfresco">Alfresco</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>Alfresco</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>03</td>'
	if isInstalled "diaspora"; then
		OUTPUT=$OUTPUT.'<td><a href="http://diaspora.wvs.localhost" title="Open Diaspora">Diaspora</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>Diaspora</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>04</td>'
	if isInstalled "dokuwiki"; then
		OUTPUT=$OUTPUT.'<td><a href="./dokuwiki" title="Open DokuWiki">DokuWiki</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>DokuWiki</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>05</td>'
	if isInstalled "drupal"; then
		OUTPUT=$OUTPUT.'<td><a href="./drupal" title="Open Drupal">Drupal</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>Drupal</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>06</td>'
	if isInstalled "ejbca"; then
		OUTPUT=$OUTPUT.'<td><a href="#" title="Open EJBCA">EJBCA</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>EJBCA</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>07</td>'
	if isInstalled "idempiere"; then
		OUTPUT=$OUTPUT.'<td><a href="#" title="Open iDempiere">iDempiere</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>iDempiere</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>08</td>'
	if isInstalled "magento"; then
		OUTPUT=$OUTPUT.'<td><a href="./magento" title="Open Magento">Magento</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>Magento</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>09</td>'
	if isInstalled "mediawiki"; then
		OUTPUT=$OUTPUT.'<td><a href="./mediawiki" title="Open MediaWiki">MediaWiki</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>MediaWiki</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>10</td>'
	if isInstalled "moodle"; then
		OUTPUT=$OUTPUT.'<td><a href="./moodle" title="Open Moodle">Moodle</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>Moodle</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>11</td>'
	if isInstalled "otrs"; then
		OUTPUT=$OUTPUT.'<td><a href="./otrs/index.pl" title="Open OTRS">OTRS</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>OTRS</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>12</td>'
	if isInstalled "owncloud"; then
		OUTPUT=$OUTPUT.'<td><a href="./owncloud" title="Open Owncloud">Owncloud</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>Owncloud</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>13</td>'
	if isInstalled "sugarcrm"; then
		OUTPUT=$OUTPUT.'<td><a href="./sugarcrm" title="Open SugarCRM">SugarCRM</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>SugarCRM</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>14</td>'
	if isInstalled "typo3"; then
		OUTPUT=$OUTPUT.'<td><a href="./typo3" title="Open Typo3">Typo3</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>Typo3</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	OUTPUT=$OUTPUT.'<tr><td>15</td>'
	if isInstalled "wordpress"; then
		OUTPUT=$OUTPUT.'<td><a href="./wordpress" title="Open Wordpress">Wordpress</a></td><td>installed</td><td>&nbsp;</td>'
	else
		OUTPUT=$OUTPUT.'<td>Wordpress</td><td>not installed</td><td>&nbsp;</td>'
	fi
	OUTPUT=$OUTPUT.'</tr>'

	echo '</table>
		<p style="font-weight: bold">Please note: If not other specified, the login for every application is webwvs // webwvs12</p>
		</html>	'

#echo $OUTPUT	
echo "$OUTPUT" > $INSTALL_DIR/index.php
}

printInfo(){
	echo ""
	echo ""
	echo "################################################################"
	echo "Please visit http://wvs.localhost to view installed applications"
	echo "################################################################"
	echo ""
	echo ""
}

while getopts "dxich?:" opt; do
    case "$opt" in
    	d)
		sudo rm -rf $INSTALL_DIR
		;;
    	x)
		OVERWRITE_EXISTING=true
		;;
	i)
		buildIndex
		echo ""
		echo "Rebuild of index completed..."
		echo ""
		exit 0
		;;	
	c)
		sudo rm -rf $TMPDIR/*
		echo ""
		echo "Temporary files have been deleted..."
		echo ""
		exit 0
		;;
	h|\?)
			echo ""
		    echo "  Use ./install.sh <<APPLICATION NAME>> to install a specific application."
			echo "  To install all available applications simply call ./install.sh without any arguments."
			echo ""
			echo "  [Arguments]"
			echo "  -d delete all existing applications before start"
			echo "  -x overwrite existing applications"
			echo "  -i rebuild index page with applications"
			echo "  -c delete temporary files"
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

rebuildIndex
printInfo


