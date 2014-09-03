MOODLE_DATABASE="db_moodle"
MOODLE_DATABASE_USER="usr_moodle"
MOODLE_DATABASE_PASSWORD="moodle"
MOODLE_WWWROOT="http://wvs.localhost/moodle"
MOODLE_MOODLEDATA="$INSTALL_DIR/moodledata"


if [ -d "$INSTALL_DIR/moodle" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping Moodle installation: Moodle is already installed."
    	return
	fi
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

#exit

#curl --silent -c /tmp/cookie -b /tmp/cookie --globoff "http://wvs.localhost/moodle/admin/index.php?agreelicense=1&confirmrelease=1&lang=en" > /dev/null

# TODO: Read sesskey and pass it to the next curl-call
#http://wvs.localhost/moodle/user/editadvanced.php?id=2

#curl -c $MOODLE_COOKIE -b $MOODLE_COOKIE --globoff "http://wvs.localhost/moodle/user/editadvanced.php?id=2" --data "id=2&course=1&sesskey=uNq0urlJ6u&_qf__user_editadvanced_form=1&mform_isexpanded_id_moodle=1&mform_isexpanded_id_moodle_additional_names=1&mform_isexpanded_id_moodle_optional=1&username=admin&newpassword=webwvs12X!$&newpasswordunmask=off&firstname=User&lastname=User&email=a@b.com&maildisplay=1&mailformat=1&maildigest=0&autosubscribe=1&timezone=99&lang=en&description_editor[format]=1"

curl -c $MOODLE_COOKIE -b $MOODLE_COOKIE --globoff 'http://wvs.localhost/moodle/admin/index.php'
curl -c $MOODLE_COOKIE -b $MOODLE_COOKIE --globoff 'http://wvs.localhost/moodle/admin/index.php?lang=en&agreelicense=1'
curl -c $MOODLE_COOKIE -b $MOODLE_COOKIE --globoff 'http://wvs.localhost/moodle/admin/index.php?agreelicense=1&confirmrelease=1&lang=en'
curl -c $MOODLE_COOKIE -b $MOODLE_COOKIE --globoff 'http://wvs.localhost/moodle/user/editadvanced.php?id=2'

curl -c $MOODLE_COOKIE -b $MOODLE_COOKIE --globoff 'http://wvs.localhost/moodle/user/editadvanced.php' --data 'id=2&course=1&sesskey=40KdGGt0EQ&_qf__user_editadvanced_form=1&mform_isexpanded_id_moodle=1&mform_isexpanded_id_moodle_additional_names=1&mform_isexpanded_id_moodle_optional=1&username=admin&newpassword=webwvs12X%21&firstname=webwvs&lastname=webwvs&email=a%40b.com&maildisplay=1&mailformat=1&maildigest=0&autosubscribe=1&preference_htmleditor=&city=&country=DE&timezone=99&lang=en&description_editor%5Btext%5D=&description_editor%5Bformat%5D=1&firstnamephonetic=&lastnamephonetic=&middlename=&alternatename=&url=&icq=&skype=&aim=&yahoo=&msn=&idnumber=&institution=&department=&phone1=&phone2=&address=&submitbutton=Update+profile'
