
ADHOCRACY_DIR="/home/$SUDO_USER/adhocracy"

mkdir -p $ADHOCRACY_DIR

wget https://github.com/liqd/adhocracy/archive/develop.tar.gz -O $ADHOCRACY_DIR/adhocracy.tar.gz -c
tar xfz $ADHOCRACY_DIR/adhocracy.tar.gz -C $ADHOCRACY_DIR

su $SUDO_USER
cd $ADHOCRACY_DIR/adhocracy-develop
sh build.sh
