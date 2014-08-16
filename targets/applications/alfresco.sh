ALFRESCO_VERSION="4.2.1"
ALFRESCO_INSTALL_DIR=$INSTALL_DIR/alfresco-$ALFRESCO_VERSION
ALFRESCO_ADMIN_PASSWORD="admin"
ALFRESCO_DATABASE="alfresco"
ALFRESCO_DATABASE_USER="alfresco"
ALFRESCO_DATABASE_PASSWORD="alfresco"
TOMCAT_DIR="/var/lib/tomcat7"

if [ -d "$ALFRESCO_INSTALL_DIR" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	echo "[INFO] Skipping Alfresco installation: Alfresco is allready instaled."
    	return
	fi
fi

rm -rf $ALFRESCO_INSTALL_DIR


# Workaround for https://issues.alfresco.com/jira/browse/ALF-5551
sudo mkdir -p /var/log/alfresco
sudo chmod 777 /var/log/alfresco    # TODO:  777 is not THE solution !
sudo chown tomcat7:tomcat7 /var/log/alfresco
sudo /etc/init.d/tomcat7 stop

# set specific vars for the installation
sed -e "s#XXX_ALFRESCO_INSTALL_DIR_XXX#$ALFRESCO_INSTALL_DIR#g" \
    -e "s#XXX_TOMCAT_DIR_XXX#$TOMCAT_DIR#g" \
    -e "s#XXX_ALFRESCO_ADMIN_PASSWORD_XXX#$ALFRESCO_ADMIN_PASSWORD#g" \
    -e "s#XXX_ALFRESCO_DATABASE_XXX#$ALFRESCO_DATABASE#g" \
    -e "s#XXX_ALFRESCO_DATABASE_USER_XXX#$ALFRESCO_DATABASE_USER#g" \
    -e "s#XXX_ALFRESCO_DATABASE_PASSWORD_XXX#$ALFRESCO_DATABASE_PASSWORD#g" \
    $SCRIPTDIR/applications/alfresco_installer.conf \
    | sudo tee $TMPDIR/alfresco_installer.conf >/dev/null

wget http://dl.alfresco.com/release/community/4.2.f-build-00012/alfresco-community-4.2.f-installer-linux-x64.bin -O $TMPDIR/alfresco-community-4.2.f-installer-linux-x64.bin -c
chmod a+x $TMPDIR/alfresco-community-4.2.f-installer-linux-x64.bin

mysql -uroot -e \
	"DROP DATABASE IF EXISTS $ALFRESCO_DATABASE;
	CREATE DATABASE IF NOT EXISTS $ALFRESCO_DATABASE;
	GRANT ALL PRIVILEGES ON "$ALFRESCO_DATABASE".* TO '$ALFRESCO_DATABASE_USER'@'localhost' IDENTIFIED BY '$ALFRESCO_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"

sudo $TMPDIR/alfresco-community-4.2.f-installer-linux-x64.bin --optionfile $TMPDIR/alfresco_installer.conf

sudo /etc/init.d/tomcat7 stop

sudo sed -i -e 's#log4j.appender.File.File=solr.log#log4j.appender.File.File=/var/log/alfresco/solr.log#g' \
    $INSTALL_DIR/alfresco*/alf_data/solr/log4j-solr.properties

sudo chown tomcat7:tomcat7 $INSTALL_DIR/alfresco* -R

# apply bug fixes
cd /var/lib/tomcat7/webapps
sudo rm -rf alfresco share
sudo mkdir alfresco
sudo mkdir share

# for alfresco.log

sudo mv alfresco.war alfresco/

cd alfresco

sudo jar -xf alfresco.war

sudo sed -i -e 's#log4j.appender.File.File=alfresco.log#log4j.appender.File.File=/var/log/alfresco/alfresco.log#g' \
    /var/lib/tomcat7/webapps/alfresco/WEB-INF/classes/log4j.properties

sudo mv alfresco.war ../alfresco.war.backup
sudo jar -cf alfresco.war *
sudo mv alfresco.war ../
cd ..
sudo rm -rf alfresco

# for share.log
cd /var/lib/tomcat7/webapps
sudo mv share.war share/
cd share
sudo jar -xf share.war

sudo sed -i -e 's#log4j.appender.File.File=share.log#log4j.appender.File.File=/var/log/alfresco/share.log#g' \
    /var/lib/tomcat7/webapps/share/WEB-INF/classes/log4j.properties

sudo mv share.war ../share.war.backup
sudo jar -cf share.war *
sudo mv share.war ../
cd ..
sudo rm -rf share

sudo /etc/init.d/tomcat7 start
