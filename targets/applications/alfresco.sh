ALFRESCO_VERSION="4.2.1"
ALFRESCO_INSTALL_DIR=$INSTALL_DIR/alfresco-$ALFRESCO_VERSION
ALFRESCO_ADMIN_PASSWORD="admin"
ALFRESCO_DATABASE="alfresco"
ALFRESCO_DATABASE_USER="alfresco"
ALFRESCO_DATABASE_PASSWORD="alfresco"
#TOMCAT_DIR="/var/lib/tomcat7"
TOMCAT_WEBAPPS_DIR=$ALFRESCO_INSTALL_DIR/tomcat/webapps

if [ -d "$ALFRESCO_INSTALL_DIR" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping Alfresco installation: Alfresco is allready installed."
    	return
	fi
fi

sudo rm -rf $ALFRESCO_INSTALL_DIR


# Workaround for https://issues.alfresco.com/jira/browse/ALF-5551
sudo rm -rf $LOG_DIR/alfresco
sudo mkdir -p $LOG_DIR/alfresco
#sudo chmod 777 /var/log/alfresco    # TODO:  777 is not THE solution !
#sudo chown tomcat7:tomcat7 /var/log/alfresco
#sudo /etc/init.d/tomcat7 stop

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

# apply bug fixes
#cd $ALFRESCO_INSTALL_DIR/tomcat7/webapps/
sudo rm -rf $TOMCAT_WEBAPPS_DIR/alfresco $TOMCAT_WEBAPPS_DIR/share
sudo mkdir $TOMCAT_WEBAPPS_DIR/alfresco $TOMCAT_WEBAPPS_DIR/share


# for alfresco.log
sudo mv $TOMCAT_WEBAPPS_DIR/alfresco.war $TOMCAT_WEBAPPS_DIR/alfresco/

#cd alfresco

sudo unzip -qq $TOMCAT_WEBAPPS_DIR/alfresco/alfresco.war -d $TOMCAT_WEBAPPS_DIR/alfresco/

sudo sed -i -e 's#log4j.appender.File.File=alfresco.log#log4j.appender.File.File='$LOG_DIR'/alfresco/alfresco.log#g' \
    $TOMCAT_WEBAPPS_DIR/alfresco/WEB-INF/classes/log4j.properties

sudo mv $TOMCAT_WEBAPPS_DIR/alfresco/alfresco.war $TOMCAT_WEBAPPS_DIR/alfresco.war.backup
sudo jar -cf $TOMCAT_WEBAPPS_DIR/alfresco/alfresco.war $TOMCAT_WEBAPPS_DIR/alfresco/*
sudo mv $TOMCAT_WEBAPPS_DIR/alfresco/alfresco.war $TOMCAT_WEBAPPS_DIR/
#cd ..
sudo rm -rf $TOMCAT_WEBAPPS_DIR/alfresco

# for share.log
#cd /var/lib/tomcat7/webapps
sudo mv $TOMCAT_WEBAPPS_DIR/share.war $TOMCAT_WEBAPPS_DIR/share/
#cd share
sudo unzip -qq $TOMCAT_WEBAPPS_DIR/share/share.war -d $TOMCAT_WEBAPPS_DIR/share/

sudo sed -i -e 's#log4j.appender.File.File=share.log#log4j.appender.File.File='$LOG_DIR'/alfresco/share.log#g' \
    $TOMCAT_WEBAPPS_DIR/share/WEB-INF/classes/log4j.properties

sudo mv $TOMCAT_WEBAPPS_DIR/share/share.war $TOMCAT_WEBAPPS_DIR/share.war.backup
sudo jar -cf $TOMCAT_WEBAPPS_DIR/share/share.war $TOMCAT_WEBAPPS_DIR/share/*
sudo mv $TOMCAT_WEBAPPS_DIR/share/share.war $TOMCAT_WEBAPPS_DIR/
#cd ..
sudo rm -rf $TOMCAT_WEBAPPS_DIR/share

sudo /etc/init.d/alfresco restart

