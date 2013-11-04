#!/bin/sh

set -e

SCRIPTDIR=$(dirname $(readlink -f $0))

#Import global config file
. $SCRIPTDIR/includes/global.cfg

installPackage() {
	DEBIAN_FRONTEND=noninteractive apt-get -qqy install "$@"
}

if [ "$(id -u)" -ne 0 ]; then
	echo "This script requires superuser privileges."
	exit 1
fi

. ./applications/dependencies.sh


# Install applications
#. ./applications/magento.sh
. ./applications/mediawiki.sh
