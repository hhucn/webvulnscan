MOODLE_DATABASE="db_moodle"
MOODLE_DATABASE_USER="usr_moodle"
MOODLE_DATABASE_PASSWORD="moodle"
MOODLE_WWWROOT="http://wvs.localhost/moodle"
MOODLE_MOODLEDATA="$INSTALL_DIR/moodledata"

if isDone "$INSTALL_DIR/moodle" "Moodle" = true ; then
    return
fi


sudo rm -rf "$INSTALL_DIR"/moodle
sudo rm -rf "$INSTALL_DIR"/moodledata

download "http://downloads.sourceforge.net/project/moodle/Moodle/stable27/moodle-latest-27.tgz?r=&ts=$(timestamp)&use_mirror=optimate" moodle.tgz

tar xfz "$TMPDIR"/moodle.tgz -C "$INSTALL_DIR"

mysql -uroot -e \
	"DROP DATABASE IF EXISTS $MOODLE_DATABASE;
	CREATE DATABASE IF NOT EXISTS $MOODLE_DATABASE;
	GRANT ALL PRIVILEGES ON "$MOODLE_DATABASE".* TO '$MOODLE_DATABASE_USER'@'localhost' IDENTIFIED BY '$MOODLE_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"

sed -e 's#XXX_MOODLEDATA_XXX#'$MOODLE_MOODLEDATA'#g' \
    -e 's#XXX_WWWROOT_XXX#'$MOODLE_WWWROOT'#g' \
    -e 's#XXX_DBNAME_XXX#'$MOODLE_DATABASE'#g' \
    -e 's#XXX_DBUSER_XXX#'$MOODLE_DATABASE_USER'#g' \
    -e 's#XXX_DBPASS_XXX#'$MOODLE_DATABASE_PASSWORD'#g' \
    "$SCRIPTDIR"/applications/moodle.conf \
    >"$INSTALL_DIR"/moodle/config.php

sudo mkdir -p "$INSTALL_DIR"/moodledata
sudo chown www-data:www-data "$INSTALL_DIR"/moodledata

sudo -u www-data /usr/bin/php "$INSTALL_DIR"/moodle/admin/cli/install_database.php --agree-license --adminuser=webwvs --adminpass=webwvs123
