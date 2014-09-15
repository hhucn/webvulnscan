EJBCA_DATABASE="db_ejbca"
EJBCA_DATABASE_USER="usr_ejbca"
EJBCA_DATABASE_PASSWORD="ejbca"
EJBCA_DIR="$INSTALL_DIR/ejbca_ce_6_2_0"
EJBCA_INIT_SCRIPT="/etc/init.d/ejbca"
JBOSS_DIR="$INSTALL_DIR/JBOSS_7_1_1"
JBOSS_VERSION_MINOR="7.1.1"
JBOSS_VERSION_MAJOR="7.1"
MYSQL_CONNECTOR_DIR="$INSTALL_DIR/mysqlConnector"

if [ -d "$EJBCA_DIR" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping EJBCA installation: EJBCA is already installed."
    	return
	fi
fi

# we need to be sure, that ejbca is not running...
if [ -f "$EJBCA_INIT_SCRIPT" ]; then
	sudo $EJBCA_INIT_SCRIPT stop
fi

# Create User and Group
id -u jboss &>/dev/null || sudo useradd -s /bin/bash -r -d /opt/jboss -M -U jboss

id -u ejbca &>/dev/null || sudo useradd -r -d $EJBCA_DIR ejbca
id -u ejbca &>/dev/null || sudo usermod -a -G ejbca, jboss ejbca

# create hosts-entry
if ! grep -q "127.0.0.1 rootca.wvs.localhost" "/etc/hosts"; then
	sudo sh -c "echo '127.0.0.1 rootca.wvs.localhost' >> /etc/hosts"
fi

sudo mkdir -p /var/log/ejbca
sudo chown jboss:jboss /var/log/ejbca

# cleanup
#sudo rm -f $TMPDIR/EJBCA*
sudo rm -rf $EJBCA_DIR
sudo rm -rf $JBOSS_DIR
sudo rm -rf $MYSQL_CONNECTOR_DIR
sudo rm -rf /opt/ejbca
sudo rm -rf /opt/jboss
sudo rm -rf /etc/ejbca
sudo rm -f $INSTALL_DIR/ejbca_superadmin.p12
sudo rm -f $EJBCA_INIT_SCRIPT

# create folders and links
mkdir -p $JBOSS_DIR
mkdir -p $MYSQL_CONNECTOR_DIR

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
	$JBOSS_DIR/standalone/configuration/standalone.xml

sed -i -e 's#9999#7999#g' \
	$JBOSS_DIR/bin/jboss-cli.xml


sed -i -e 's#</paths>#<path name="sun/security/x509"/><path name="sun/security/pkcs11"/><path name="sun/security/pkcs11/wrapper"/><path name="sun/security/action"/></paths>#g' \
	/opt/jboss/modules/sun/jdk/main/module.xml

#mysql connector
mkdir -p /opt/jboss/modules/com/mysql/main/
cd /opt/jboss/modules/com/mysql/main
ln -s $MYSQL_CONNECTOR_DIR/mysql-connector-java-5.1.30.jar mysql-connector-java.jar

cp $SCRIPTDIR/applications/ejbca_config/jboss_mysql_connector_module module.xml

#replace ejbca config-files
sudo rm -rf $EJBCA_DIR/conf/*.sample
sudo cp $SCRIPTDIR/applications/ejbca_config/*.properties $EJBCA_DIR/conf/

sudo chown -R jboss:jboss $JBOSS_DIR
sudo chown -R jboss:jboss $EJBCA_DIR

sudo $EJBCA_INIT_SCRIPT start

# EJBCA 6.2.0 has a bug which causes wrong command-line args intepretation during 'ant install'
# so we need this workaround
sudo sed -i -e 's#<ejbca:cli-hideargs arg="ca init ${ca.name} &quot;'"'"'${ca.dn}'"'"'&quot; ${ca.tokentype} ${ca.tokenpassword} ${ca.keyspec} ${ca.keytype} ${ca.validity} ${ca.policy} ${ca.signaturealgorithm} ${ca.tokenproperties} ${install.certprofile.command} -superadmincn ${superadmin.cn}"/>#<ejbca:cli-hideargs arg="ca init \&quot;${ca.name}\&quot; \&quot;${ca.dn}\&quot; ${ca.tokentype} ${ca.tokenpassword} ${ca.keyspec} ${ca.keytype} ${ca.validity} ${ca.policy} ${ca.signaturealgorithm} --tokenprop ${ca.tokenproperties} ${install.certprofile.command} -superadmincn ${superadmin.cn}"/>#g' \
	-e 's#-certprofile ${ca.certificateprofile}#-certprofile \&quot;${ca.certificateprofile}\&quot;#g' \
	$EJBCA_DIR/bin/cli.xml

#deploy the mysql driver
cd /opt/jboss/bin
sudo sh jboss-cli.sh <<!
connect
/subsystem=datasources/jdbc-driver=com.mysql.jdbc.Driver:add(driver-name=com.mysql.jdbc.Driver,driver-class-name=com.mysql.jdbc.Driver,driver-module-name=com.mysql,driver-xa-datasource-class-name=com.mysql.jdbc.jdbc.jdbc2.optional.MysqlXADataSource)
: reload
exit
!

#now we need to remove the default database which is provided with JBOSS
#if we don't do so, EJBCA will be using this (wrong) DB
sudo sed -i -e '/<datasource jndi/,/<\/datasource>/d' \
	-e '/<driver name="h2"/,/<\/driver>/d' \
	$JBOSS_DIR/standalone/configuration/standalone.xml


sudo $EJBCA_INIT_SCRIPT restart

#create new user in managementRealm
#due to a bug in JBOSS 7.1.1 we can't use add-user.sh and need to add the user manually
#https://issues.jboss.org/browse/AS7-5061

#cd /opt/jboss/bin
#sudo ./add-user.sh <<!
#a
#
#jbAdmin
#jbAdmin12
#jbAdmin12
#yes
#exit
#!

# the password is (as above): jbAdmin12
echo 'jbAdmin=ec7a041db58425f15ffb597668eaef95' | sudo tee $JBOSS_DIR/standalone/configuration/mgmt-users.properties > /dev/null
echo 'jbAdmin=ec7a041db58425f15ffb597668eaef95' | sudo tee $JBOSS_DIR/domain/configuration/mgmt-users.properties > /dev/null

#deploy ejbca.ear
sudo -u jboss sh -c 'cd /opt/ejbca && ant deploy'

sudo $EJBCA_INIT_SCRIPT restart

sudo -u jboss sh -c 'cd /opt/ejbca && ant install'

sudo -u jboss sh -c 'cd /opt/ejbca && ant deploy'

sudo $EJBCA_INIT_SCRIPT restart

sudo cp $EJBCA_DIR/p12/superadmin.p12 $INSTALL_DIR/ejbca_superadmin.p12
sudo chown www-data:www-data $INSTALL_DIR/ejbca_superadmin.p12