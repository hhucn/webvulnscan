MOODLE_DATABASE="db_moodle"
MOODLE_DATABASE_USER="usr_moodle"
MOODLE_DATABASE_PASSWORD="moodle"
MOODLE_WWWROOT="http://wvs.localhost/moodle"
MOODLE_MOODLEDATA="$INSTALL_DIR/moodledata"

if isDone "$INSTALL_DIR/moodle" "Moodle" = true ; then
    return
fi

MOODLE_COOKIE=$(mktemp $TMPDIR/XXXXXX)

sudo rm -rf $INSTALL_DIR/moodle
sudo rm -rf $INSTALL_DIR/moodledata

download "http://downloads.sourceforge.net/project/moodle/Moodle/stable27/moodle-latest-27.tgz?r=&ts=$(timestamp)&use_mirror=optimate" moodle.tgz

tar xfz $TMPDIR/moodle.tgz -C $INSTALL_DIR

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
    $SCRIPTDIR/applications/moodle.conf \
    >"$INSTALL_DIR/moodle/config.php"

sudo mkdir -p $INSTALL_DIR/moodledata
sudo chown www-data:www-data $INSTALL_DIR/moodledata

curl -c $MOODLE_COOKIE -b $MOODLE_COOKIE --globoff 'http://wvs.localhost/moodle/admin/index.php'
curl -c $MOODLE_COOKIE -b $MOODLE_COOKIE --globoff 'http://wvs.localhost/moodle/admin/index.php?lang=en&agreelicense=1'

SESSION_KEY=$(curl -s -c $MOODLE_COOKIE -b $MOODLE_COOKIE --globoff 'http://wvs.localhost/moodle/admin/index.php'| sed -n 's#.*"sesskey":"\([^"]*\)".*#\1#p')
curl -c $MOODLE_COOKIE -b $MOODLE_COOKIE --globoff 'http://wvs.localhost/moodle/admin/index.php?agreelicense=1&confirmrelease=1&lang=en'

curl -c $MOODLE_COOKIE -b $MOODLE_COOKIE --globoff "http://wvs.localhost/moodle/user/editadvanced.php?id=2" --data 'id=2&course=1&sesskey='"$SESSION_KEY"'&_qf__user_editadvanced_form=1&mform_isexpanded_id_moodle=1&mform_isexpanded_id_moodle_additional_names=1&mform_isexpanded_id_moodle_optional=1&username=admin&newpassword=webwvs12X!&newpasswordunmask=off&firstname=User&lastname=User&email=a@b.com&maildisplay=1&mailformat=1&maildigest=0&autosubscribe=1&timezone=99&lang=en&description_editor[format]=1'
