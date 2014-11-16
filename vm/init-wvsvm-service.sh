#! /bin/sh
### BEGIN INIT INFO
# Provides:          init_wvsvm
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Initialize the wvsvm VM.
# Description:       Installs packages and preconfigures the VM on first boot.
### END INIT INFO

# Do NOT "set -e"

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="Initialize the wvsvm VM"
NAME=init_wvsvm
SCRIPTNAME=/etc/init.d/$NAME

# Read configuration variable file if it is present
[ -r /etc/default/$NAME ] && . /etc/default/$NAME

# Load the VERBOSE setting and other rcS variables
. /lib/init/vars.sh

# Define LSB log_* functions.
# Depend on lsb-base (>= 3.2-14) to ensure that this file is present
# and status_of_proc is working.
. /lib/lsb/init-functions

#
# Function that starts the daemon/service
#
do_start()
{
	if test '!' -e /wvsvm-init/init-wvsvm.sh ; then
		return 0
	fi

	echo 'Installing wvsvm applications ...'
	echo
	echo
	echo
	/wvsvm-init/init-wvsvm.sh > &> install-wvsvm.log
	reboot
	#if /wvsvm-init/init-wvsvm.sh ; then
	#	reboot
	#fi
}

#
# Function that stops the daemon/service
#
do_stop()
{
	# Return
	#   0 if daemon has been stopped
	#   1 if daemon was already stopped
	#   2 if daemon could not be stopped
	#   other if a failure occurred
	return 0
}


case "$1" in
  start)
	do_start
	case "$?" in
		0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
		2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
	esac
	;;
  stop)
	do_stop
	case "$?" in
		0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
		2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
	esac
	;;
  *)
	echo "Usage: $SCRIPTNAME {start|stop}" >&2
	exit 3
	;;
esac

:
