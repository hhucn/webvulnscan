EJBCA_DATABASE="db_ejbca"
EJBCA_DATABASE_USER="usr_ejbca"
EJBCA_DATABASE_PASSWORD="ejbca"
EJBCA_DIR="$INSTALL_DIR/ejbca_6_2_0"
JBOSS_DIR="$INSTALL_DIR/JBOSS_7_1_1"
MYSQL_CONNECTOR_DIR="$INSTALL_DIR/mysqlConnector"

# Create User and Group
id -u jboss &>/dev/null || sudo useradd -s /bin/bash -r -d /opt/jboss -M -U jboss

id -u ejbca &>/dev/null || sudo useradd -r -d $EJBCA_DIR -c 'ejbca user' ejbca
id -u ejbca &>/dev/null || sudo usermod -a -G ejbca, jboss ejbca


# create hosts-entry
if ! grep -q "127.0.0.1 rootca.wvs.localhost" "/etc/hosts"; then
	sudo sh -c "echo '127.0.0.1 rootca.wvs.localhost' >> /etc/hosts"
fi

sudo mkdir -p /var/log/ejbca
sudo chown jboss:jboss /var/log/ejbca

# cleanup
sudo rm -f $TMPDIR/EJBCA*
sudo rm -rf $EJBCA_DIR*
sudo rm -rf $JBOSS_DIR*

#mkdir $JBOSS_DIR
cd $INSTALL_DIR
mkdir JBOSS_7_1_1

mkdir $MYSQL_CONNECTOR_DIR

# create symbolic links
sudo ln -s $EJBCA_DIR /opt/ejbca
sudo ln -s $JBOSS_DIR /opt/jboss

# get ejbca and move it to "installed"
wget "http://downloads.sourceforge.net/project/ejbca/ejbca6/ejbca_6_2_0/ejbca_ce_6_2_0.zip?r=&ts=$(timestamp)&use_mirror=optimate" -nv -O $TMPDIR/EJBCA.zip -c
unzip $TMPDIR/EJBCA.zip -d $INSTALL_DIR
mv $INSTALL_DIR/ejbca* $INSTALL_DIR/ejbca

# get JBOSS AS 7.1.1
wget http://download.jboss.org/jbossas/7.1/jboss-as-7.1.1.Final/jboss-as-7.1.1.Final.zip -nv -O $TMPDIR/jboss.zip -c
unzip $TMPDIR/jboss.zip -d $INSTALL_DIR
mv $INSTALL_DIR/jboss* $INSTALL_DIR/$JBOSS_DIR

# get mysql-connector 5.1.30
wget http://central.maven.org/maven2/mysql/mysql-connector-java/5.1.30/mysql-connector-java-5.1.30.jar -nv -O $MYSQL_CONNECTOR_DIR/mysql-connector-java-5.1.30.jar -c

# prepare mysql database
mysql -uroot -e \
	"DROP DATABASE IF EXISTS $EJBCA_DATABASE;
	CREATE DATABASE IF NOT EXISTS $EJBCA_DATABASE;
	GRANT ALL PRIVILEGES ON "$EJBCA_DATABASE".* TO '$EJBCA_DATABASE_USER'@'localhost' IDENTIFIED BY '$EJBCA_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"

cd /opt/jboss/bin
cp standalone.conf standalone.conf.orig

cp /opt/jboss/bin/init.d/jboss-as-standalone.sh /etc/init.d/ejbca
mkdir /etc/ejbca
cp /opt/jboss/bin/init.d/jboss-as.conf /etc/ejbca/ejbca-init.conf


