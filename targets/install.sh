#!/bin/sh

set -e

SCRIPTDIR=$(dirname $(readlink -f $0))
APACHE_DIR="/var/www"
TMPDIR="$SCRIPTDIR/tmp"

mkdir -p "$TMPDIR"

installPackage() {
	DEBIAN_FRONTEND=noninteractive apt-get -qqy install "$@"
}

if [ "$(id -u)" -ne 0 ]; then
	echo "This script requires superuser privileges."
	exit 1
fi

# Update System
apt-get -y update > /dev/null 2>&1

. ./applications/dependencies.sh

# Install applications
. ./applications/owncloud.sh
. ./applications/magento.sh
 ./applications/mediawiki.sh
 ./applications/adhocracy.sh
