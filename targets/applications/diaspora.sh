DIASPORA_SERVICE_USER="$USER_NAME"

### Requirements
sed -e "s#XXX_DIASPORA_PUBLIC_DIR1_XXX#$INSTALL_DIR/diaspora#g" \
    $SCRIPTDIR/applications/diaspora_init_script.sh \
    | sudo tee /etc/init.d/diaspora >/dev/null
if [ -d "$INSTALL_DIR/diaspora" ]; then
    if [ "$OVERWRITE_EXISTING" = false ]; then
    	printInfo "Skipping Diaspora installation: Diaspora is already installed."
    	return
	fi
fi

sudo rm -rf $INSTALL_DIR/diaspora
sudo rm -rf $TMPDIR/node*

download http://nodejs.org/dist/v0.10.22/node-v0.10.22-linux-x64.tar.gz nodejs.tar.gz
tar xfz $TMPDIR/nodejs.tar.gz -C $TMPDIR
sudo chmod 755 $TMPDIR/node-v*/bin/*
sudo mv -f $TMPDIR/node-v*/bin/* /usr/local/bin/

# Ruby
curl -L https://get.rvm.io | bash -s stable --rails --autolibs=enabled --with-gems="rdoc rails --no-ri --no-rdoc"
RVM="$HOME/.rvm/scripts/rvm"

#RVM
$RVM install 2.0.0-p353
echo >&2 su -l -c "source $RVM" # Prevent error: RVM is not a function, selecting rubies with 'rvm use ...' will not work.
$RVM use 2.0.0-p353

sudo /etc/init.d/apache2 restart > /dev/null

### diaspora install
cd $INSTALL_DIR/../

# generate certificate
sh gencert.sh diaspora.wvs.localhost >/dev/null
mkdir -p $INSTALL_DIR/ssl/diaspora
mv diaspora.wvs.localhost* $INSTALL_DIR/ssl/diaspora

# create diaspora user (if needed)
id -u diaspora &>/dev/null || sudo useradd diaspora

# get diaspora
cd $INSTALL_DIR
#rm -rf diaspora
test -e diaspora || git clone -b master git://github.com/diaspora/diaspora.git
cd diaspora

# setup the virtual host file - apache will be used as a reverse proxy

sed -e "s#XXX_DIASPORA_PUBLIC_DIR1_XXX#$INSTALL_DIR/diaspora/public/#g" \
    -e "s#XXX_DIASPORA_PUBLIC_DIR2_XXX#$INSTALL_DIR/diaspora/public#g" \
    -e "s#XXX_DIASPORA_SSL_CERT_XXX#$INSTALL_DIR/ssl/diaspora/diaspora.wvs.localhost.crt#g" \
    -e "s#XXX_DIASPORA_SSL_PRIV_KEY_XXX#$INSTALL_DIR/ssl/diaspora/diaspora.wvs.localhost.key#g" \
    $SCRIPTDIR/applications/diaspora.conf \
    | sudo tee /etc/apache2/sites-available/diaspora.wvs.conf >/dev/null

# enable virtual host and restart apache
sudo a2ensite diaspora.wvs.conf > /dev/null
sudo /etc/init.d/apache2 restart

# setup config files
cp config/diaspora.yml.example config/diaspora.yml
sed -i -e '0,/#certificate_authorities:/{s/#certificate_authorities:/certificate_authorities:/}' config/diaspora.yml 

cp config/database.yml.example config/database.yml
sed -i -e '/postgres:/,+6 s/^/#/' config/database.yml

RVM="$HOME/.rvm/scripts/rvm"
#$RVM --default use 1.9.1 #1.9.3-p448

sudo gem install bundler rdoc rdoc-data

# install required Ruby libraries
RAILS_ENV=production bundle install --without test development
#gem install <= 1.8.6 : unsupported
 #= 1.8.7 : gem install rdoc-data; rdoc-data --install
 #= 1.9.1 : gem install rdoc-data; rdoc-data --install
#>= 1.9.2 : nothing to do! Yay!rdoc rdoc-data; rdoc-data --install ---- unnötig???

# setup the database
RAILS_ENV=production bundle exec rake db:create db:schema:load

# precompile assets
bundle exec rake assets:precompile

# Update hosts file
if ! grep -q "127.0.0.1 diaspora.wvs.localhost" "/etc/hosts"; then
	sudo sh -c "echo '127.0.0.1 diaspora.wvs.localhost' >> /etc/hosts"
fi

#set diaspora to production mode
sed -e "s#rails_environment: 'development'#rails_environment: 'production'#g" $SCRIPTDIR/installed/diaspora/config/defaults.yml | sudo tee $SCRIPTDIR/installed/diaspora/config/defaults.yml >/dev/null

#modify init script
sed -e "s#XXX_DIASPORA_PUBLIC_DIR1_XXX#$INSTALL_DIR/diaspora#g" \
    -e "s#XXX_DIASPORA_SERVICE_USER_XXX#$DIASPORA_SERVICE_USER#g" \
	$SCRIPTDIR/applications/diaspora_init_script.sh \
	| sudo tee /etc/init.d/diaspora >/dev/null

sudo chmod a+x /etc/init.d/diaspora
