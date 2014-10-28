IDEMPIERE_INSTALL_DIR="$INSTALL_DIR"/idempiere/idempiere-server
IDEMPIERE_SERVICE_USER="$USER_NAME"

if isDone "$INSTALL_DIR/idempiere" "iDempiere" = true ; then
    return
fi

if [ -f "/etc/init.d/idempiere" ]; then
	sudo /etc/init.d/idempiere stop
	sudo rm -f /etc/init.d/idempiere
fi

# remove old stuff
rm -rf "$TMPDIR"/idempiere*
sudo rm -rf "$INSTALL_DIR"/idempiere*
sudo rm -rf /etc/init.d/idempire

# database setup
# database and role arrangements
export PGPASSWORD=$POSTGRES_PASSWORD
if psql -U postgres -lqt | cut -d \| -f 1 | grep -w 'idempiere'; then
    psql -U postgres -c "DROP DATABASE idempiere"
fi

psql -U postgres -c "CREATE USER adempiere SUPERUSER ENCRYPTED PASSWORD 'adempiere'";

psql -U postgres -c "CREATE DATABASE idempiere OWNER adempiere"

download http://superb-dca2.dl.sourceforge.net/project/idempiere/v2.0/server/idempiereServer.gtk.linux.x86_64.zip idempiere.zip
unzip -qq $TMPDIR/idempiere.zip -d $INSTALL_DIR/

cd $INSTALL_DIR
mv idempiere.* idempiere
cd idempiere/idempiere-server

echo "ADEMPIERE_KEYSTOREPASS=myPassword
	IDEMPIERE_HOME="$IDEMPIERE_INSTALL_DIR"
	ADEMPIERE_APPS_SERVER=localhost
	ADEMPIERE_WEB_PORT=9080
	ADEMPIERE_SSL_PORT=9443
	ADEMPIERE_DB_TYPE=PostgreSQL
	ADEMPIERE_DB_SERVER=localhost
	ADEMPIERE_DB_PORT=5432
	ADEMPIERE_DB_NAME=idempiere
	ADEMPIERE_DB_USER=adempiere
	ADEMPIERE_DB_PASSWORD=adempiere
	ADEMPIERE_DB_SYSTEM=postgres
	ADEMPIERE_MAIL_SERVER=localhost
	ADEMPIERE_ADMIN_EMAIL=root@localhost
	ADEMPIERE_MAIL_USER=
	ADEMPIERE_MAIL_PASSWORD=" > idempiereEnv.properties

# setup environment
sh console-setup.sh <<!








	









!

# create database
cd utils
sh RUN_ImportIdempiere.sh <<!

!


sed -e "s#XXX_IDEMPIERE_DIR_XXX#$IDEMPIERE_INSTALL_DIR/#g" \
    -e "s#XXX_IDEMPIERE_USER_XXX#$IDEMPIERE_SERVICE_USER#g" \
    $SCRIPTDIR/applications/idempiere_init_script.sh \
    | sudo tee /etc/init.d/idempiere >/dev/null

sudo chmod +x /etc/init.d/idempiere
sudo update-rc.d idempiere defaults

sudo /etc/init.d/idempiere start