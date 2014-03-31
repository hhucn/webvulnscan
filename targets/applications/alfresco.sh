ALFRESCO_VERSION="4.2.1"
ALFRESCO_INSTALL_DIR=/opt/alfresco-$ALFRESCO_VERSION
ALFRESCO_ADMIN_PASSWORD="admin"
TOMCAT_DIR=$ALFRESCO_INSTALL_DIR/tomcat

#cp /alfresco_installer.conf $TMPDIR/alfresco_installer.conf

sed -e "s#XXX_ALFRESCO_INSTALL_DIR_XXX#$ALFRESCO_INSTALL_DIR#g" \
    -e "sXXX_TOMCAT_DIR_XXX#$TOMCAT_DIR#g" \
    -e "sXXX_ALFRESCO_ADMIN_PASSWORD_XXX#$TOMCAT_DIR#g" \
    $SCRIPTDIR/applications/alfresco_installer.conf \
    | sudo tee $TMPDIR/alfresco_installer.conf >/dev/null

wget http://dl.alfresco.com/release/community/4.2.f-build-00012/alfresco-community-4.2.f-installer-linux-x64.bin -O $TMPDIR/alfresco-community-4.2.f-installer-linux-x64.bin -c

sudo .$TMPDIR/alfresco-community-4.2.f-installer-linux-x64.bin --optionfile $TMPDIR/alfresco_installer.conf
