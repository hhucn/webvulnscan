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
  htop \
  expect \
  tomcat7 \
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

# Java
if [ -n "$JAVA_HOME" ]; then
    echo "\$JAVA_HOME was already set to: $JAVA_HOME";
else
    sudo sh -c "echo 'export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64
export PATH=$PATH:/usr/lib/jvm/java-7-openjdk-amd64/bin' >> /etc/profile"
    source /etc/profile		# TODO: not working inside this script!?!
fi

# Mysql-Connector for tomcat
#if [ ! -f /var/lib/tomcat7/lib/mysql-connector-java-5.1.30.jar ]; then
#	sudo wget http://central.maven.org/maven2/mysql/mysql-connector-java/5.1.30/mysql-connector-java-5.1.30.jar -nv -O /var/lib/tomcat7/lib/mysql-connector-java-5.1.30.jar -c
#fi

# assign more memory (e.g. for alfresco)
if [ ! -f /usr/share/tomcat7/bin/setenv.sh ]; then
	echo 'export JAVA_OPTS="-Xms256m -Xmx512m"' | sudo tee /usr/share/tomcat7/bin/setenv.sh >/dev/null
fi

# potgres
#sudo su - postgres 
#psql -c "ALTER USER postgres WITH PASSWORD 'postgres'" -d postgres 

