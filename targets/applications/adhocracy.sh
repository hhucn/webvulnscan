ADHOCRACY_DIR="$INSTALL_DIR/adhocracy"

if isDone "$ADHOCRACY_DIR" "Adhocracy" = true ; then
	return
fi

rm -rf $ADHOCRACY_DIR

if [ -f "/etc/init.d/adhocracy_services" ]; then
	sudo /etc/init.d/adhocracy_services stop
	sudo rm -f /etc/init.d/adhocracy_services
fi

echo "
[domains]
main = wvs.localhost

[adhocracy]
relative_urls = True
host = 0.0.0.0" > $TMPDIR/adhocracy_cfg

freePort "5001 5005 5006 5010"

mkdir -p $ADHOCRACY_DIR

wget -nv https://raw.github.com/liqd/adhocracy/develop/build.sh -O $ADHOCRACY_DIR/build.sh
cd $ADHOCRACY_DIR
sh build.sh -c $SCRIPTDIR/applications/adhocracy_buildout.cfg

# Create a index.php file with a redirect to make adhocracy accessible via http://wvs.localhost/adhocracy/
echo "<?php header( 'Location: http://localhost:5001' );?>" > index.php

./adhocracy_buildout/bin/adhocracy_interactive.sh &
