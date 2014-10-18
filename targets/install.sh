#!/bin/bash -l
# login shell needed for rvm installation

set -e

# include functions
. functions.sh

if [[ $EUID -eq 0 ]]; then
    printError "Please start this script without sudo or root privileges."
    exit 1
fi

SCRIPTDIR=$(dirname $(readlink -f $0))
APACHE_DIR="/var/www"
TMPDIR="$SCRIPTDIR/tmp"
INSTALL_DIR="$SCRIPTDIR/installed"
USER_HOME=$(eval echo ~${SUDO_USER})
USER_NAME=$(whoami)
OVERWRITE_EXISTING=false
LOG_DIR="$SCRIPTDIR/log"
POSTGRES_PASSWORD="postgres"
SKIP_DEPENDENCIES=false

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

mkdir -p $INSTALL_DIR
mkdir -p $TMPDIR
mkdir -p $LOG_DIR

while getopts "dxicsh?:" opt; do
    case "$opt" in
    	d)
			if [ -z $INSTALL_DIR ]; then 
				echo ""
				echo "[ERROR] \$INSTALL_DIR not set!"; 
				echo ""
			else
				sudo rm -rf $INSTALL_DIR/*
				echo ""
				echo "All applications inside 'installed' have been deleted."
				echo ""			
			fi
			buildIndex
			exit 0
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
			if [ -z "$TMPDIR" ]; then 
				echo ""
				echo "[ERROR] \$TMPDIR not set!"; 
				echo ""
			else
				sudo rm -rf -- $TMPDIR/*			
				echo ""
				echo "Temporary files have been deleted..."
				echo ""
			fi
			
			exit 0
			;;
		s)
			SKIP_DEPENDENCIES=true
			;;
		h|\?)
			echo ""
		    	echo "  Use ./install.sh APPLICATION_NAME to install a specific application."
			echo "  To install all available applications simply call ./install.sh without any arguments."
			echo ""
			echo "  [Arguments]"
			echo "  -d delete all existing applications inside directory 'installed'"
			echo "  -x overwrite existing applications during install"
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

shift $(expr $OPTIND - 1 )

# Check if apache user exists, if yes add this user to the group of the user who started this script
# TODO: Find better solution!
if id -u "www-data" >/dev/null 2>&1; then
	GROUP=`id -g -n $USER`
	sudo usermod -a -G $GROUP www-data
fi


# delete (invalid) old virtual hosts which will prevent apache from starting
#sudo rm -f /etc/apache2/sites-enabled/wvs.conf

if ! grep -q "127.0.0.1 wvs.localhost" "/etc/hosts"; then
	sudo sh -c "echo '127.0.0.1 wvs.localhost' >> /etc/hosts"
fi


# Install dependencies
if [ $SKIP_DEPENDENCIES = false ]; then
	. $SCRIPTDIR/applications/dependencies.sh
else
	printInfo "IMPORTANT: Install of dependencies have been skipped. Some installs might not work properly."
fi

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

buildIndex
printInfoIndex
