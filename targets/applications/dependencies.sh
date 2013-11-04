
installPackage mysql-server mysql-client \
	apache2 libapache2-mod-php5 php5-mysql php5-curl php5-gd php-pear php5-imagick php5-memcache php5-ming

sed -ri -e 's#^(memory_limit = ).*$#\1 512M#' -e 's#^(max_execution_time = ).*$#\1 600#' /etc/php5/apache2/php.ini

# replace any comment line starting with # by ; to avoid PHP deprecated messages
#find /etc/php5/cli/conf.d/ -name "*.ini" -exec sed -i -re 's/^(\s*)#(.*)/\1;\2/g' {} \;

service apache2 restart > /dev/null

