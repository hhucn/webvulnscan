# remove old stuff
cd $TMPDIR/
rm -rf idempiere*

# database setup
#sudo su - postgres
su - postgres -s -c "psql -U postgres -c \"CREATE ROLE adempiere SUPERUSER LOGIN PASSWORD 'adempiere'\""

#psql -U postgres -c "CREATE ROLE adempiere SUPERUSER LOGIN PASSWORD 'adempiere'" 
#logout

sudo su - adempiere
createdb  --template=template0 -E UNICODE -O adempiere -U adempiere idempiere
psql -d idempiere -U adempiere -c "ALTER ROLE adempiere SET search_path TO adempiere, pg_catalog"
logout

wget http://superb-dca2.dl.sourceforge.net/project/idempiere/v2.0/server/idempiereServer.gtk.linux.x86_64.zip -nv -O $TMPDIR/idempiere.zip -c
unzip $TMPDIR/idempiere.zip -d $INSTALL_DIR/

cd $INSTALL_DIR/
mv idempiere* idempiere
cd idempiere/idempiere-server

# setup environment
sh console-setup.sh <<!
/usr/lib/jvm/java-6-openjdk-amd64

keyStorePassword






127.0.0.1
8081
8444
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

cd ..

# start idempiere automatically
echo "
#!/bin/sh

### BEGIN INIT INFO
# Provides:          alfresco
# Required-Start:    $local_fs $remote_fs
# Required-Stop:     $local_fs $remote_fs
# Should-Start:      $all
# Should-Stop:       $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Start/stop iDempiere
# Description:       Start/stop iDempiere
### END INIT INFO

$INSTALL_DIR/idempiere/idempiere-server/idempiere start" > $INSTALL_DIR/idempiere/idempiere-server/idempiere-start.sh

sudo cp idempiere-start.sh /etc/init.d/idempiere
sudo chmod +x /etc/init.d/idempiere
sudo update-rc.d idempiere defaults

sudo /etc/init.d/idempiere start
