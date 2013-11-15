
installPackage mysql-server mysql-client apache2 libapache2-mod-php5 php5-mysql php5-gd php-pear php5-imagick php5-memcache php5-ming php5-json libcurl3 libcurl3-dev php5-mysql curl
	
# set memory-limit and max_execution_time
sudo sed -ri -e 's#^(memory_limit = ).*$#\1 512M#' -e 's#^(max_execution_time = ).*$#\1 600#' /etc/php5/apache2/php.ini

# replace any comment line starting with # by ; to avoid PHP deprecated messages
#find /etc/php5/cli/conf.d/ -name "*.ini" -exec sed -i -re 's/^(\s*)#(.*)/\1;\2/g' {} \;

# create virtual host if needed
if [ ! -f /etc/apache2/sites-available/wvs ]; then
	sudo echo "   
	   <virtualhost *:80>
	      # Admin email, Server Name (domain name) and any aliases
	      ServerAdmin webmaster@domain.com
	      ServerName wvs.localhost

	      # Index file and Document Root (where the public files are located)
	      DirectoryIndex index.php
	      DocumentRoot $SCRIPTDIR/installed/

	      <Directory $SCRIPTDIR/installed/>
		Options -Indexes FollowSymLinks MultiViews +Includes
		AllowOverride All
		Order allow,deny
		allow from all
	      </Directory>
	   </virtualhost>" > /etc/apache2/sites-available/wvs
fi

sudo a2ensite wvs > /dev/null
sudo service apache2 restart > /dev/null

