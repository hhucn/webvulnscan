installPackage \
  mysql-server mysql-client libmysqlclient-dev \
  apache2 libapache2-mod-proxy-html \
  libapache2-mod-php5 php5-mysql php5-gd php-pear php5-imagick php5-memcache php5-ming php5-json php5-mysql \
  libcurl3 libcurl3-dev libcurl4-openssl-dev curl build-essential libssl-dev libxml2-dev libxslt-dev \
  imagemagick libmagickwand-dev \
  git-core \
  redis-server \
  curl \
  python g++ make checkinstall \
  postgresql postgresql-contrib \
  htop \
  expect \
  tomcat7 \
  libapache2-mod-perl2 libjson-xs-perl libdbd-mysql-perl libdbd-mysql-perl libtimedate-perl libgd-text-perl libnet-ldap-perl \
  libpdf-api2-perl libsoap-lite-perl libyaml-libyaml-perl libcrypt-eksblowfish-perl libmail-imapclient-perl \
  libio-socket-ssl-perl libtext-csv-xs-perl libgd-graph-perl libnet-dns-perl libapache-dbi-perl libencode-hanextra-perl
	
# set memory-limit and max_execution_timeinit-wvsvm
sudo sed -ri -e 's#^(memory_limit = ).*$#\1 512M#' -e 's#^(max_execution_time = ).*$#\1 600#' /etc/php5/apache2/php.ini

# replace any comment line starting with # by ; to avoid PHP deprecated messages
#find /etc/php5/cli/conf.d/ -name "*.ini" -exec sed -i -re 's/^(\s*)#(.*)/\1;\2/g' {} \;

# create virtual host if needed
echo "
<virtualhost *:80>
  # Admin email, Server Name (domain name) and any aliases
  ServerAdmin webmaster@domain.com
  ServerName wvs.localhost

  # Index file and Document Root (where the public files are located)
  DirectoryIndex index.php
  DocumentRoot $SCRIPTDIR/installed/

  <Directory $SCRIPTDIR/installed/>
	Options -Indexes +FollowSymLinks +MultiViews +Includes
	AllowOverride All
	Order allow,deny
	Satisfy any
	allow from all
	Require all granted
  </Directory>
</virtualhost>" | sudo tee /etc/apache2/sites-available/wvs.conf >/dev/null


# Enable apache modules
# TODO: lbmethod_byrequests
sudo a2enmod ssl rewrite headers proxy proxy_http proxy_balancer > /dev/null

# Enable subdomain wvs.localhost
# TODO: apache2.4 a2ensite wvs     apache2.2 a2ensite wvs.conf
sudo a2ensite wvs.conf > /dev/null

# disable unneeded files
if [ -f /etc/apache2/sites-available/default-ssl.txt ]
then
    sudo a2dissite default-ssl > /dev/null
fi

if [ -f /etc/apache2/sites-available/default-ssl.txt ]
then
    sudo a2dissite otrs.conf > /dev/null
fi

sudo /etc/init.d/apache2 restart > /dev/null

# NodeJS
wget http://nodejs.org/dist/v0.10.22/node-v0.10.22-linux-x64.tar.gz -O $TMPDIR/nodejs.tar.gz -c
tar xfz $TMPDIR/nodejs.tar.gz -C $TMPDIR
sudo chmod 755 $TMPDIR/node-v*/bin/*
sudo mv -f $TMPDIR/node-v*/bin/* /usr/local/bin/

# Ruby
#curl -L https://get.rvm.io | bash -s stable --rails --autolibs=enabled --with-gems="rdoc rails --no-ri --no-rdoc"
#RVM="$HOME/.rvm/scripts/rvm"

#$RVM requirements
#$RVM install 2.0.0-p353
#echo >&2 su -l -c "source $RVM" # Prevent error: RVM is not a function, selecting rubies with 'rvm use ...' will not work.
#$RVM use 2.0.0-p353

sudo /etc/init.d/apache2 restart > /dev/null

# Postgres
# psql -U postgres -c "CREATE USER wvsvm WITH PASSWORD 'wvsvm';"

