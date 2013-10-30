#!/bin/bash

function checkPackageInstalled() {
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' "$1"|grep "install ok installed")
	if [ "" == "$PKG_OK" ]; then
		return 1
	else
		return 0
	fi
}

function installPackage() {
	echo "... installing" "$1"	# debug
	sudo DEBIAN_FRONTEND=noninteractive apt-get -qq --force-yes install $1 > /dev/null
}


echo "Installing dependencies..."

# MySQL
if ! checkPackageInstalled "mysql-server"; then
	installPackage "mysql-server"
	mysqladmin -u root password $MYSQL_ROOT_PASSWORD
fi

if ! checkPackageInstalled "mysql-client"; then
	installPackage "mysql-client"
fi

# Apache2 and PHP5
reqPackages=('apache2' 'libapache2-mod-php5' 'php5-mysql' 'php5-curl' 'php5-gd' 'php-pear' 'php5-imagick' 'php5-memcache' 'php5-ming');
instPackages=""

for i in "${reqPackages[@]}"
do
   :
   if ! checkPackageInstalled "$i"; then
	instPackages="$instPackages$i "
   fi	
done

if [ -n "$instPackages" ]; then
	installPackage "$instPackages"
	sudo service apache2 restart
fi
