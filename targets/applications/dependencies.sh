#!/bin/bash

#####################################################################
###  Script to install dependencies required for almost           ###
###  all applications                                             ###
#####################################################################

print "Installing dependencies..."

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

# Set PHP memory limit and max execution time
# TODO: implement dynamic way to find .ini?
sed -ri 's/^(memory_limit = )[0-9]+(M.*)$/\1'${PHP_MEMORY_LIMIT}'\2/' /etc/php5/apache2/php.ini
sed -ri 's/^(max_execution_time = )[0-9]+(.*)$/\1'${PHP_MAX_EXECUTION_TIME}'\2/' /etc/php5/apache2/php.ini

# replace any comment line starting with # by ; to avoid PHP deprecated messages
find /etc/php5/cli/conf.d/ -name "*.ini" -exec sed -i -re 's/^(\s*)#(.*)/\1;\2/g' {} \;

service apache2 restart > /dev/null

