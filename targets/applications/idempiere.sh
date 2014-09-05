IDEMPIERE_INSTALL_DIR="$INSTALL_DIR"/idempiere/idempiere-server
IDEMPIERE_SERVICE_USER="$USER_NAME"

if [ -d "$INSTALL_DIR/idempiere" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping iDempiere installation: iDempiere is already installed."
    	return
	fi
fi

# remove old stuff
rm -rf "$TMPDIR"/idempiere*
sudo rm -rf "$INSTALL_DIR"/idempiere*

# database setup
# database and role arrangements
if psql -U postgres -lqt | cut -d \| -f 1 | grep -w 'idempiere'; then
    psql -U postgres -c "DROP DATABASE idempiere"
fi

#if [[ $(psql -U postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='adempiere'" | grep -q 1) != '1' ]] ; then
#	psql -U postgres -c "CREATE ROLE adempiere SUPERUSER LOGIN PASSWORD 'adempiere'"
#fi

psql -U postgres -c "CREATE DATABASE idempiere OWNER adempiere"

download http://superb-dca2.dl.sourceforge.net/project/idempiere/v2.0/server/idempiereServer.gtk.linux.x86_64.zip idempiere.zip
unzip -qq $TMPDIR/idempiere.zip -d $INSTALL_DIR/

cd $INSTALL_DIR
mv idempiere.* idempiere
cd idempiere/idempiere-server

# setup environment
sh console-setup.sh <<!
/usr/lib/jvm/java-6-openjdk-amd64
$IDEMPIERE_INSTALL_DIR
keyStorePassword

9080
9443
N
2
127.0.0.1
5432
idempire
adempiere
adempiere
postgres
127.0.0.1
adempiere
adempiere
root@127.0.0.1
Y
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