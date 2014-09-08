EJBCA_DATABASE="db_ejbca"
EJBCA_DATABASE_USER="usr_ejbca"
EJBCA_DATABASE_PASSWORD="ejbca"
EJBCA_DIR="$INSTALL_DIR/ejbca_ce_6_2_0"
JBOSS_DIR="$INSTALL_DIR/JBOSS_7_1_1"
JBOSS_VERSION_MINOR="7.1.1"
JBOSS_VERSION_MAJOR="7.1"
MYSQL_CONNECTOR_DIR="$INSTALL_DIR/mysqlConnector"

# Create User and Group
id -u jboss &>/dev/null || sudo useradd -s /bin/bash -r -d /opt/jboss -M -U jboss

id -u ejbca &>/dev/null || sudo useradd -r -d $EJBCA_DIR 'ejbca user' ejbca
id -u ejbca &>/dev/null || sudo usermod -a -G ejbca, jboss ejbca


# create hosts-entry
if ! grep -q "127.0.0.1 rootca.wvs.localhost" "/etc/hosts"; then
	sudo sh "echo '127.0.0.1 rootca.wvs.localhost' >> /etc/hosts"
fi

sudo mkdir -p /var/log/ejbca
sudo chown jboss:jboss /var/log/ejbca

# cleanup
#sudo rm -f $TMPDIR/EJBCA*
sudo rm -rf $EJBCA_DIR
sudo rm -rf $JBOSS_DIR
sudo rm -rf /opt/ejbca
sudo rm -rf /opt/jboss
sudo rm -rf /etc/ejbca

# create folders and links
mkdir -p $JBOSS_DIR
mkdir -p $INSTALL_DIR/"$MYSQL_CONNECTOR_DIR"
sudo mkdir /etc/ejbca
sudo mkdir -p /var/log/ejbca
sudo chown jboss:jboss /var/log/ejbca

sudo ln -s $EJBCA_DIR /opt/ejbca
sudo ln -s $JBOSS_DIR /opt/jboss


# get ejbca and move it to "installed"
download "http://downloads.sourceforge.net/project/ejbca/ejbca6/ejbca_6_2_0/ejbca_ce_6_2_0.zip?r=&ts=$(timestamp)&use_mirror=optimate" EJBCA.zip
unzip -qq -o $TMPDIR/EJBCA.zip -d $INSTALL_DIR

# get JBOSS AS
download http://download.jboss.org/jbossas/$JBOSS_VERSION_MAJOR/jboss-as-$JBOSS_VERSION_MINOR.Final/jboss-as-$JBOSS_VERSION_MINOR.Final.zip jboss.zip
unzip -qq -o $TMPDIR/jboss.zip -d $INSTALL_DIR
mv $INSTALL_DIR/jboss-as-$JBOSS_VERSION_MINOR.Final/* $JBOSS_DIR/
rm -rf $INSTALL_DIR/jboss-as-$JBOSS_VERSION_MINOR.Final

# get mysql-connector 5.1.30
download http://central.maven.org/maven2/mysql/mysql-connector-java/5.1.30/mysql-connector-java-5.1.30.jar mysql-connector-java-5.1.30.jar
mv $TMPDIR/mysql-connector-java-5.1.30.jar $MYSQL_CONNECTOR_DIR/mysql-connector-java-5.1.30.jar

# prepare mysql database
mysql -uroot -e \
	"DROP DATABASE IF EXISTS $EJBCA_DATABASE;
	CREATE DATABASE IF NOT EXISTS $EJBCA_DATABASE;
	GRANT ALL PRIVILEGES ON "$EJBCA_DATABASE".* TO '$EJBCA_DATABASE_USER'@'localhost' IDENTIFIED BY '$EJBCA_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"


cd /opt/jboss/bin
cp standalone.conf standalone.conf.orig
	
sed -i -e 's#\#JAVA_HOME="/opt/java/jdk"#'JAVA_HOME="/usr/lib/jvm/java-7-openjdk-amd64/"'#g' \
	standalone.conf

# prevent "success/failure: command not found - error in debian"
sed -e 's#success#$echo "[SUCCESS]"/#g' \
    -e 's#failure#$echo "[FAILURE]"#g' \
    $SCRIPTDIR/applications/ejbca_config/ejbca_init_script.sh \
    | sudo tee /etc/init.d/ejbca >/dev/null

sudo chmod a+x /etc/init.d/ejbca

sudo cp $SCRIPTDIR/applications/ejbca_config/ejbca_init_conf.conf /etc/ejbca/ejbca-init.conf

# ports 8080, 8443... are in use... we need to change them and configure the mysql connector
sed -i -e 's#8080#7080#g' \
		-e 's#8443#7443#g' \
		-e 's#8090#7090#g' \
		-e 's#9999#7999#g' \
		-e 's#9990#7990#g' \
		-e 's#9443#7443#g' \
		-e 's#8009#7009#g' \
		-e 's#<driver name="h2" module="com.h2database.h2">#<driver name="com.mysql.jdbc.Driver" module="com.mysql">#g' \
		-e 's#<xa-datasource-class>org.h2.jdbcx.JdbcDataSource</xa-datasource-class>#<xa-datasource-class>com.mysql.jdbc.jdbc.jdbc2.optional.MysqlXADataSource</xa-datasource-class>#g' \
	$JBOSS_DIR/standalone/configuration/standalone.xml

#sed -i -e 's#8080#7080#g' \
#		-e 's#8443#7443#g' \
#		-e 's#8090#7090#g' \
#		-e 's#9999#7999#g' \
#		-e 's#9990#7990#g' \
#		-e 's#9443#7443#g' \
#		-e 's#8009#7009#g' \
#	$JBOSS_DIR/standalone/configuration/standalone-full.xml

sed -i -e 's#9999#7999#g' \
	$JBOSS_DIR/bin/jboss-cli.xml


sed -i -e 's#</paths>#<path name="sun/security/x509"/><path name="sun/security/pkcs11"/><path name="sun/security/pkcs11/wrapper"/><path name="sun/security/action"/></paths>#g' \
	/opt/jboss/modules/sun/jdk/main/module.xml

mkdir -p /opt/jboss/modules/com/mysql/main/
cd /opt/jboss/modules/com/mysql/main
ln -s $MYSQL_CONNECTOR_DIR/mysql-connector-java-5.1.30.jar mysql-connector-java.jar

cp $SCRIPTDIR/applications/ejbca_config/jboss_mysql_connector_module module.xml

sudo chown -R jboss:jboss $JBOSS_DIR

#cd /opt/jboss/bin
#sudo sh jboss-cli.sh <<!
#connect
#/subsystem=datasources/jdbc-driver=com.mysql.jdbc.Driver:add(driver-name=com.mysql.jdbc.Driver,driver-module-name=com.mysql,driver-xa-datasource-class-name=com.mysql.jdbc.jdbc.jdbc2.optional.MysqlXADataSource)
#:reload
#exit
#!


echo "done"