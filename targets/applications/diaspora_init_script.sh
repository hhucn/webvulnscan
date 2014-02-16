# This is the init script for starting up the
#  Diaspora
#
# chkconfig: 345 91 10
# description: Starts and stops the Diaspora daemon.
# From: http://stackoverflow.com/questions/9122488/how-to-allow-diaspora-to-start-when-server-boot-up

PROC_NAME=Diaspora
DIASPORA_HOME=XXX_DIASPORA_PUBLIC_DIR1_XXX
# Change the user to whichever user you need
RUN_AS_USER=diaspora
startup="cd $DIASPORA_HOME; ./script/server"
# Replace by stop/shutdown command
#shutdown="$DIASPORA_HOME/script/server"

start(){
 echo -n $"Starting $PROC_NAME service: "
 su -l $RUN_AS_USER -c "$startup"
 RETVAL=$?
 echo
}

stop(){
 echo -n $"Stoping $PROC_NAME service: "
 # Uncomment here to allow stop
 # su -l $RUN_AS_USER -c "$shutdown"
 RETVAL=$?
 echo
}

restart(){
  stop
  start
}


# See how we were called.
case "$1" in
start)
 start
 ;;
stop)
 stop
 ;;
restart)
 restart
 ;;
*)
 echo $"Usage: $0 {start|stop|restart}"
 exit 1
esac

exit 0
