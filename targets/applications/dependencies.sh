printInfo "Please wait, while we install/update necessary dependencies..."

installPackage \
  mysql-server mysql-client libmysqlclient-dev \
  apache2 libapache2-mod-proxy-html \
  libapache2-mod-php5 php5-mcrypt php5-mysql php5-gd php-pear php5-imagick php5-memcache php5-ming php5-json php5-mysql php5-curl php5-xmlrpc php5-intl \
  libcurl3 libcurl3-dev libcurl4-openssl-dev curl build-essential libssl-dev libxml2-dev libxslt-dev \
  imagemagick libmagickwand-dev \
  git-core \
  redis-server \
  curl \
  python g++ make checkinstall chkconfig \
  postgresql postgresql-contrib \
  htop axel unzip \
  expect \
  openjdk-6-jdk openjdk-7-jdk openjdk-7-jre \
  mercurial \
  libapache2-mod-perl2 libjson-xs-perl libdbd-mysql-perl libdbd-mysql-perl libtimedate-perl libgd-text-perl libnet-ldap-perl \
  libpdf-api2-perl libsoap-lite-perl libyaml-libyaml-perl libcrypt-eksblowfish-perl libmail-imapclient-perl \
  libio-socket-ssl-perl libtext-csv-xs-perl libgd-graph-perl libnet-dns-perl libapache-dbi-perl libencode-hanextra-perl
	
# set memory-limit and max_execution_time
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

# fix 'Could not reliably determine the server's fully qualified domain name'
if [ ! -f /etc/apache2/conf.d/name ]; then
	sudo sh -c "echo 'ServerName localhost' >> /etc/apache2/conf.d/name"
fi

# disable unneeded files
if [ -f /etc/apache2/sites-available/default-ssl ]
then
    sudo a2dissite default-ssl > /dev/null
fi

if [ -f /etc/apache2/sites-available/otrs.conf ]
then
    sudo a2dissite otrs.conf > /dev/null
fi

sudo service apache2 restart > /dev/null


# postgres configuration

# change authentication for using an md5 encrypted password instead of peer authentication
sudo sed -i -e 's#postgres                                peer#postgres                                md5#g' \
            -e 's#all                                     peer#all                                     md5#g' \
  /etc/postgresql/9.1/main/pg_hba.conf

sudo service postgresql restart

# ensure that we have a known password
export PGPASSWORD=""
if [[ "$(psql -U postgres -lqt 2>&1)" =~ 'password authentication failed' ]]; then
    # there is a password set we check now if its the one which has been set in install.sh
    export PGPASSWORD=$POSTGRES_PASSWORD
    if [[ "$(psql -U postgres -lqt 2>&1)" =~ 'password authentication failed' ]]; then
        printError "The provided postgres system-user password \"$POSTGRES_PASSWORD\" is invalid"
        exit
    fi
else
    if [[ $(psql -U postgres -c "ALTER USER postgres with password '$POSTGRES_PASSWORD';") =~ 'ERROR' ]]; then
        printError "There ware a problem while setting the postgres system-user password."
    fi
    export PGPASSWORD=$POSTGRES_PASSWORD
fi