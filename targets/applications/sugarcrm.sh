SUGAR_DB_USER="usr_sugarcrm"
SUGAR_DB_USER_PASSWORD="wvs"
SUGAR_DB_NAME="db_sugarcrm"
SUGAR_INSTALL_FOLDER="sugarcrm"
SUGAR_VERSION_MAJOR="6.5"
SUGAR_VERSION_FULL="6.5.17"

if [ -d "$INSTALL_DIR/$SUGAR_INSTALL_FOLDER" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping SugarCRM installation: SugarCRM is already installed."
    	return
    fi
fi

cd $INSTALL_DIR
sudo rm -rf $SUGAR_INSTALL_FOLDER

download "http://downloads.sourceforge.net/project/sugarcrm/1%20-%20SugarCRM%20$SUGAR_VERSION_MAJOR.X/SugarCommunityEdition-$SUGAR_VERSION_MAJOR.X/SugarCE-$SUGAR_VERSION_FULL.zip?r=&ts=$(timestamp)&use_mirror=optimate" sugarcrm.zip
	
unzip -qq $TMPDIR/sugarcrm.zip -d $INSTALL_DIR
mv $INSTALL_DIR/SugarCE-Full* $INSTALL_DIR/$SUGAR_INSTALL_FOLDER

echo "<?php \$sugar_config_si = array(
'setup_db_host_name' => 'localhost',
'setup_db_sugarsales_user' => '$SUGAR_DB_USER',
'setup_db_sugarsales_password' => '$SUGAR_DB_USER_PASSWORD',
'setup_db_database_name' => '$SUGAR_DB_NAME',
'setup_db_type' => 'mysql',
'setup_db_pop_demo_data' => false,
'setup_db_create_database' => 1,
'setup_db_create_sugarsales_user' => 1,
'setup_db_admin_user_name' => 'root',
'setup_db_admin_password' => '',
'setup_db_drop_tables' => 0,
'setup_db_username_is_privileged' => true,
'dbUSRData' => 'create',
'setup_site_url' => 'http://wvs.localhost/$SUGAR_INSTALL_FOLDER',
'setup_site_admin_user_name'=>'webwvs',
'setup_site_admin_password' => 'webwvs12',
'setup_site_sugarbeet_automatic_checks' => true, 
'default_currency_iso4217' => 'EUR',
'default_currency_name' => 'EUR Euro',
'default_currency_significant_digits' => '2',
'default_currency_symbol' => '€',
'default_date_format' => 'Y-m-d',
'default_time_format' => 'H:i',
'default_decimal_seperator' => '.',
'default_export_charset' => 'utf-8',
'default_language' => 'en_us',
'default_locale_name_format' => 's f l',
'default_number_grouping_seperator' => ',',
'export_delimiter' => ',',
'setup_license_key' => 'LICENSE_KEY', 
'setup_system_name' => 'SugarCRM - WVS Test',
);" | sudo tee $INSTALL_DIR/$SUGAR_INSTALL_FOLDER/config_si.php >/dev/null


mysql -uroot -e "
    DROP DATABASE IF EXISTS $SUGAR_DB_NAME;
    GRANT ALL PRIVILEGES ON *.* TO '*'@'localhost' IDENTIFIED BY '$SUGAR_DB_USER_PASSWORD';
    FLUSH PRIVILEGES;"


cd $INSTALL_DIR/$SUGAR_INSTALL_FOLDER

sudo chown www-data:www-data * -R

wget -q --spider "http://wvs.localhost/$SUGAR_INSTALL_FOLDER/install.php?goto=SilentInstall&cli=true"
