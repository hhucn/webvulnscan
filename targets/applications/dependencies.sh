
installPackage mysql-server mysql-client apache2 libapache2-mod-php5 php5-mysql php5-gd php-pear php5-imagick php5-memcache php5-ming php5-json libcurl3 libcurl3-dev libcurl4-openssl-dev php5-mysql curl build-essential libssl-dev libxml2-dev libxslt-dev imagemagick git-core redis-server curl libmysqlclient-dev libmagickwand-dev python g++ make checkinstall 
	
# set memory-limit and max_execution_time
sudo sed -ri -e 's#^(memory_limit = ).*$#\1 512M#' -e 's#^(max_execution_time = ).*$#\1 600#' /etc/php5/apache2/php.ini

# replace any comment line starting with # by ; to avoid PHP deprecated messages
#find /etc/php5/cli/conf.d/ -name "*.ini" -exec sed -i -re 's/^(\s*)#(.*)/\1;\2/g' {} \;

# create virtual host if needed
if [ ! -f /etc/apache2/sites-available/wvs ]; then
	sudo sh -c "echo '  
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
	   </virtualhost>' >> /etc/apache2/sites-available/wvs"
fi


# Enable apache modules
sudo a2enmod ssl rewrite headers proxy proxy_http proxy_balancer > /dev/null

# Enable subdomain wvs.localhost
sudo a2ensite wvs > /dev/null

sudo a2dissite default-ssl > /dev/null

sudo service apache2 restart > /dev/null

# NodeJS
wget http://nodejs.org/dist/v0.10.22/node-v0.10.22-linux-x64.tar.gz -O $TMPDIR/nodejs.tar.gz -c
tar xfz $TMPDIR/nodejs.tar.gz -C $TMPDIR
sudo chmod 755 $TMPDIR/node-v*/bin/*
sudo mv -f $TMPDIR/node-v*/bin/* /usr/local/bin/


# Ruby
curl -L dspr.tk/1t | bash	# download script to install the most recent stable version of ruby
RVM="$HOME/.rvm/scripts/rvm"

sudo $RVM requirements
sudo $RVM install 1.9.3-p448
echo >&2 su -l -c "source $RVM" # Prevent error: RVM is not a function, selecting rubies with 'rvm use ...' will not work.
sudo $RVM use 1.9.3-p448
export RAILS_ENV=production

