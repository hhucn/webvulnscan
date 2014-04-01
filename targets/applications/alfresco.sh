ALFRESCO_VERSION="4.2.1"
ALFRESCO_INSTALL_DIR=$INSTALL_DIR/alfresco-$ALFRESCO_VERSION
ALFRESCO_ADMIN_PASSWORD="admin"
ALFRESCO_DATABASE="alfresco"
ALFRESCO_DATABASE_USER="alfresco"
ALFRESCO_DATABASE_PASSWORD="alfresco"

TOMCAT_DIR=$ALFRESCO_INSTALL_DIR/tomcat

#cp /alfresco_installer.conf $TMPDIR/alfresco_installer.conf

sed -e "s#XXX_ALFRESCO_INSTALL_DIR_XXX#$ALFRESCO_INSTALL_DIR#g" \
    -e "s#XXX_TOMCAT_DIR_XXX#$TOMCAT_DIR#g" \
    -e "s#XXX_ALFRESCO_ADMIN_PASSWORD_XXX#$TOMCAT_DIR#g" \
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

$TMPDIR/alfresco-community-4.2.f-installer-linux-x64.bin --optionfile $TMPDIR/alfresco_installer.conf
