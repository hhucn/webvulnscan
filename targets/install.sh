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
