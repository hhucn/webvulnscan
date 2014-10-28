GRUYERE_DIR="$INSTALL_DIR/gruyere"

if isDone "$GRUYERE_DIR" "gruyere" = true ; then
	return
fi

rm -rf $GRUYERE_DIR

if [ -f "/etc/init.d/gruyere" ]; then
	sudo /etc/init.d/gruyere stop
	sudo rm -f /etc/init.d/gruyere
fi

mkdir -p $INSTALL_DIR/gruyere

download http://google-gruyere.appspot.com/gruyere-code.zip gruyere.zip
unzip -qq -o $TMPDIR/gruyere.zip -d $INSTALL_DIR/gruyere

sed -e "s#XXX_GRUYERE_INSTALL_DIR_XXX#$INSTALL_DIR/gruyere/gruyere.py#g" \
    $SCRIPTDIR/applications/gruyere_init_script.sh \
    | sudo tee /etc/init.d/gruyere > /dev/null

sudo chmod a+x /etc/init.d/gruyere