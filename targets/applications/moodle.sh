MOODLE_DATABASE="db_moodle"
MOODLE_DATABASE_USER="usr_moodle"
MOODLE_DATABASE_PASSWORD="moodle"
MOODLE_WWWROOT="$INSTALL_DIR/moodle"
MOODLE_MOODLEDATA="/home/user/dev/webvulnscan/targets/moodledata"

sudo rm -rf $TMPDIR/moodle

wget "http://downloads.sourceforge.net/project/moodle/Moodle/stable27/moodle-latest-27.tgz?r=&ts=$(timestamp)&use_mirror=optimate" -nv -O $TMPDIR/moodle.tgz -c

tar xfz $TMPDIR/moodle.tgz -C $INSTALL_DIR

mysql -uroot -e \
	"DROP DATABASE IF EXISTS $MOODLE_DATABASE;
	CREATE DATABASE IF NOT EXISTS $MOODLE_DATABASE;
	GRANT ALL PRIVILEGES ON "$MOODLE_DATABASE".* TO '$MOODLE_DATABASE_USER'@'localhost' IDENTIFIED BY '$MOODLE_DATABASE_PASSWORD';
	FLUSH PRIVILEGES;"
exit
sed -e 's#XXX_MOODLEDATA_XXX#'$MOODLE_MOODLEDATA'#g' \
    -e 's#XXX_WWWROOT_XXX#'$MOODLE_WWWROOT'#g' \
    -e 's#XXX_DBNAME_XXX#'$MOODLE_DATABASE'#g' \
    -e 's#XXX_DBUSER_XXX#'$MOODLE_DATABASE_USER'#g' \
    -e 's#XXX_DBPASS_XXX#'$MOODLE_DATABASE_PASSWORD'#g' \
    $SCRIPTDIR/applications/moodle.conf \
    >"$INSTALL_DIR/moodle/config.php"


curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/moodle/admin/index.php?agreelicense=1&confirmrelease=1&lang=en"

# TODO: Read sesskey and pass it to the next curl-call
#http://wvs.localhost/moodle/user/editadvanced.php?id=2

curl -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/moodle/admin/upgradesettings.php?return=site" --data "id=2&course=1&sesskey=uNq0urlJ6u&_qf__user_editadvanced_form=1&mform_isexpanded_id_moodle=1&mform_isexpanded_id_moodle_additional_names=1&mform_isexpanded_id_moodle_optional=1&username=admin&newpassword=Moodle1$&newpasswordunmask=off&firstname=User&lastname=User&email=a@b.com&maildisplay=1&mailformat=1&maildigest=0&autosubscribe=1&timezone=99&lang=en&description_editor[format]=1"
