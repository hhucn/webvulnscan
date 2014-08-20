ALFRESCO_VERSION="4.2.1"
ALFRESCO_INSTALL_DIR=$INSTALL_DIR/alfresco-$ALFRESCO_VERSION
ALFRESCO_ADMIN_PASSWORD="admin"
ALFRESCO_DATABASE="alfresco"
ALFRESCO_DATABASE_USER="alfresco"
ALFRESCO_DATABASE_PASSWORD="alfresco"
TOMCAT_DIR="/var/lib/tomcat7"

if [ -d "$ALFRESCO_INSTALL_DIR" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping Alfresco installation: Alfresco is allready installed."
    	return
	fi
fi

sudo rm -rf $ALFRESCO_INSTALL_DIR

# set specific vars for the installation
sed -e "s#XXX_ALFRESCO_INSTALL_DIR_XXX#$ALFRESCO_INSTALL_DIR#g" \
    -e "s#XXX_TOMCAT_DIR_XXX#$TOMCAT_DIR#g" \
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
mv $TMPDIR/mysql-connector-java-5.1.30.jar $INSTALL_DIR/$ALFRESCO_INSTALL_DIR/tomcat/shared/lib/mysql-connector-java-5.1.30.jar

sudo /etc/init.d/alfresco restart

