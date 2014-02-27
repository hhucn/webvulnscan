ADHOCRACY_DIR="$INSTALL_DIR/adhocracy"

mkdir -p $ADHOCRACY_DIR

wget -nv https://raw.github.com/liqd/adhocracy/develop/build.sh -O $ADHOCRACY_DIR/build.sh

cd $ADHOCRACY_DIR
sh build.sh

# Create a index.php file with a redirect to make adhocracy accessible via http://wvs.localhost/adhocracy/
echo "<?php header( 'Location: http://localhost:5001' );?>" > index.php

./adhocracy_buildout/bin/adhocracy_interactive.sh &
