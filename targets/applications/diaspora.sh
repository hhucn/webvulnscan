cd $INSTALL_DIR/../

# generate certificate
sh gencert.sh diaspora.wvs.localhost >/dev/null
mkdir -p $INSTALL_DIR/ssl/diaspora
mv diaspora.wvs.localhost* $INSTALL_DIR/ssl/diaspora


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

#RVM="$HOME/.rvm/scripts/rvm"
#$RVM --default use 1.9.1 #1.9.3-p448

# install required Ruby libraries
RAILS_ENV=production bundle install --without test development
#gem install rdoc rdoc-data; rdoc-data --install ---- unnötig???

# setup the database
RAILS_ENV=production bundle exec rake db:create db:schema:load

# precompile assets
bundle exec rake assets:precompile

# Update hosts file
if ! grep -q "127.0.0.1 diaspora.wvs.localhost" "/etc/hosts"; then
	sudo sh -c "echo '127.0.0.1 diawpora.wvs.localhost' >> /etc/hosts"
fi

#set diaspora to production mode
sed -e "s#rails_environment: 'development'#rails_environment: 'production'#g" $SCRIPTDIR/installed/diaspora/config/defaults.yml | sudo tee $SCRIPTDIR/installed/diaspora/config/defaults.yml >/dev/null

