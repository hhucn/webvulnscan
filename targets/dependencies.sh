#!/bin/bash

echo "Installing dependencies..."

echo "... MySQL server and client \c"
# Install MySQL server and client
# TODO: Still buggy!!!
type mysql >/dev/null 2>&1 && \
	echo " [already installed]" || \
	sudo DEBIAN_FRONTEND=noninteractive apt-get -qq --force-yes install mysql-server mysql-client > /dev/null \
	mysqladmin -u root password $MYSQL_ROOT_PASSWORD \
	echo " [ok]"


# Install Apache2
echo "... Apache2 and PHP5 \c"
sudo DEBIAN_FRONTEND=noninteractive apt-get -qq --force-yes install apache2 php5 libapache2-mod-php5 php5-mysql php5-curl php5-gd php-pear php5-imagick php5-memcache php5-ming > /home/user/test123 #dev/null
sudo chown -R $USER:users /var/www
sudo /etc/init.d/apache2 restart
