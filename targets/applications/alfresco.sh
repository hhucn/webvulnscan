ALFRESCO_VERSION="4.2.1"
ALFRESCO_INSTALL_DIR=$INSTALL_DIR/alfresco-$ALFRESCO_VERSION
ALFRESCO_ADMIN_PASSWORD="admin"
ALFRESCO_DATABASE="alfresco"
ALFRESCO_DATABASE_USER="alfresco"
ALFRESCO_DATABASE_PASSWORD="alfresco"
TOMCAT_WEBAPPS_DIR=$ALFRESCO_INSTALL_DIR/tomcat/webapps

if isDone "$ALFRESCO_INSTALL_DIR" "Alfresco" = true ; then
    return
fi

sudo rm -rf $ALFRESCO_INSTALL_DIR
sudo rm -rf $LOG_DIR/alfresco
sudo rm -f /etc/init.d/alfresco

sudo mkdir -p $LOG_DIR/alfresco

# set specific vars for the installation
sed -e "s#XXX_ALFRESCO_INSTALL_DIR_XXX#$ALFRESCO_INSTALL_DIR#g" \
    -e "s#XXX_ALFRESCO_ADMIN_PASSWORD_XXX#$ALFRESCO_ADMIN_PASSWORD#g" \
    -e "s#XXX_ALFRESCO_DATABASE_XXX#$ALFRESCO_DATABASE#g" \
    -e "s#XXX_ALFRESCO_DATABASE_USER_XXX#$ALFRESCO_DATABASE_USER#g" \
    -e "s#XXX_ALFRESCO_DATABASE_PASSWORD_XXX#$ALFRESCO_DATABASE_PASSWORD#g" \
    $SCRIPTDIR/applications/alfresco_installer.conf \
    | sudo tee $TMPDIR/alfresco_installer.conf >/dev/null

download http://dl.alfresco.com/release/community/4.2.f-build-00012/alfresco-community-4.2.f-installer-linux-x64.bin alfresco-community-4.2.f-installer-linux-x64.bin
chmod a+x $TMPDIR/alfresco-community-4.2.f-installer-linux-x64.bin

mysql -uroot -e \
	"DROP DATABASE IF EXISTS $ALFRESCO_DATABASE;
	CREATE DATABASE IF NOT EXISTS $ALFRESCO_DATABASE;
	GRANT ALL PRIVILEGES ON "$ALFRESCO_DATABASE".* TO '$ALFRESCO_DATABASE_USER'@'localhost' IDENTIFIED BY '$ALFRESCO_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"

sudo $TMPDIR/alfresco-community-4.2.f-installer-linux-x64.bin --optionfile $TMPDIR/alfresco_installer.conf

#Mysql-Connector for tomcat
download http://central.maven.org/maven2/mysql/mysql-connector-java/5.1.30/mysql-connector-java-5.1.30.jar mysql-connector-java-5.1.30.jar
sudo mv $TMPDIR/mysql-connector-java-5.1.30.jar $ALFRESCO_INSTALL_DIR/tomcat/shared/lib/mysql-connector-java-5.1.30.jar

# apply logfile-location bug fixes
sudo rm -rf $TOMCAT_WEBAPPS_DIR/alfresco $TOMCAT_WEBAPPS_DIR/share
sudo mkdir $TOMCAT_WEBAPPS_DIR/alfresco $TOMCAT_WEBAPPS_DIR/share

cd $TOMCAT_WEBAPPS_DIR

# for alfresco.log
sudo unzip -qq alfresco.war -d alfresco/
sudo mv $TOMCAT_WEBAPPS_DIR/alfresco.war $TOMCAT_WEBAPPS_DIR/alfresco/

sudo sed -i -e 's#log4j.appender.File.File=alfresco.log#log4j.appender.File.File='$LOG_DIR'/alfresco/alfresco.log#g' \
    $TOMCAT_WEBAPPS_DIR/alfresco/WEB-INF/classes/log4j.properties

cd alfresco
sudo mv alfresco.war $TOMCAT_WEBAPPS_DIR/alfresco.war.backup

sudo jar -cf alfresco.war *
sudo mv alfresco.war $TOMCAT_WEBAPPS_DIR/


# for share.log
cd $TOMCAT_WEBAPPS_DIR

sudo unzip -qq share.war -d $TOMCAT_WEBAPPS_DIR/share/
sudo mv share.war share/

sudo sed -i -e 's#log4j.appender.File.File=share.log#log4j.appender.File.File='$LOG_DIR'/alfresco/share.log#g' \
    $TOMCAT_WEBAPPS_DIR/share/WEB-INF/classes/log4j.properties

cd share
sudo mv share.war $TOMCAT_WEBAPPS_DIR/share.war.backup
sudo jar -cf share.war *
sudo mv share.war $TOMCAT_WEBAPPS_DIR/

# cleanup
sudo rm -rf $TOMCAT_WEBAPPS_DIR/alfresco
sudo rm -rf $TOMCAT_WEBAPPS_DIR/share

sudo /etc/init.d/alfresco restart
