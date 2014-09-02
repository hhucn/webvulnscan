#! /bin/sh
### BEGIN INIT INFO
# Provides: diaspora
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: Diaspora application server
# Description: Start / stop the Diaspora app server
### END INIT INFO

# Author: FABIAN Tamas Laszlo <giganetom@gmail.com>

# PATH should only include /usr/* if it runs after the mountnfs.sh script
PATH=/sbin:/usr/sbin:/bin:/usr/bin
DESC="Diaspora application server"
NAME="XXX_DIASPORA_SERVICE_USER_XXX"
DIASPORA_HOME="XXX_DIASPORA_PUBLIC_DIR1_XXX"

# if you use mySQL:
STARTSCRIPT=./script/server
# if you use postgres use the following line instead
# STARTSCRIPT="export DB=postgres; ./script/server"

LOGFILE=$DIASPORA_HOME/log/startscript.log
SCRIPTNAME=$0
USER=diaspora
STARTUP_TIMEOUT=100

. /lib/init/vars.sh
. /lib/lsb/init-functions

check_unicorn() {
    pgrep -f "unicorn_rails master"
}

check_sidekiq() {
    pgrep -f "sidekiq 2"
}

do_start()
{
    if ! touch $LOGFILE; then
        log_failure_msg "Could not touch logfile"
        return 2
    fi

    if ! chown $USER $LOGFILE; then
        log_failure_msg "Could not chown logfile"
        return 2
    fi

    if check_unicorn && check_sidekiq; then
        log_warning_msg "Diaspora is already running"
        return 1
    fi

    if ! su -l $USER -c "cd $DIASPORA_HOME; $STARTSCRIPT >> $LOGFILE 2>&1 &"; then
        log_failure_msg "Could not run start script"
        return 2
    fi

    [ "$VERBOSE" != no ] && log_action_msg "Waiting for Diaspora processes... "
    c=0
    while ! check_unicorn > /dev/null || ! check_sidekiq > /dev/null; do
        if [ $c -gt $STARTUP_TIMEOUT ]; then
            log_failure_msg "Timeout waiting for Diaspora processes"
            return 2
        fi
        c=`expr $c + 1`
        sleep 1
        [ "$VERBOSE" != no ] && echo -n "."
    done
    [ "$VERBOSE" != no ] && log_action_end_msg 0
}

do_stop()
{
    for i in `check_unicorn`; do
        [ "$VERBOSE" != no ] && log_action_msg "Killing unicorn master with PID $i"
        kill -TERM $i
        [ "$VERBOSE" != no ] && log_action_end_msg $?
    done

    for i in `check_sidekiq`; do
        [ "$VERBOSE" != no ] && log_action_msg "Killing sidekiq with PID $i"
        kill -TERM $i
        [ "$VERBOSE" != no ] && log_action_end_msg $?
    done

    return 0
}

case "$1" in
  start)
    [ "$VERBOSE" != no ] && log_daemon_msg "Starting $DESC" "$NAME"
    do_start
    case "$?" in
        0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
        *) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
    esac
    ;;
  stop)
    [ "$VERBOSE" != no ] && log_daemon_msg "Stopping $DESC" "$NAME"
    do_stop
    case "$?" in
        0|1) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
        2) [ "$VERBOSE" != no ] && log_end_msg 1 ;;
    esac
    ;;
  status)
    log_daemon_msg 'Checking for running Diaspora processes'

    unicorn_running=false
    for i in `check_unicorn`; do
        log_action_msg "Found unicorn master qith PID $i"
        unicorn_running=true
    done

    sidekiq_running=false
    for i in `check_sidekiq`; do
        log_action_msg "Found sidekiq with PID $i"
        sidekiq_running=true
    done

    if $unicorn_running && $sidekiq_running; then
        log_action_msg "Diaspora health is OK"
        log_end_msg 0
    else
        if $unicorn_running; then
            log_failure_msg "Unicorn is RUNNING, but sidekiq is DOWN!"
            log_end_msg 1
            return 1
        fi
        if $sidekiq_running; then
            log_failure_msg "Sidekiq is RUNNING, but unicorn is DOWN!"
            log_end_msg 1
            return 1
        fi
        log_daemon_msg "All Diaspora processes are DOWN"
        log_end_msg 0
    fi
    ;;
  restart|force-reload)
    [ "$VERBOSE" != no ] && log_daemon_msg "Restarting $DESC" "$NAME"
    do_stop
    case "$?" in
      0|1)
        do_start
        case "$?" in
            0) [ "$VERBOSE" != no ] && log_end_msg 0 ;;
            1) [ "$VERBOSE" != no ] && log_failure_msg "old process is still running" && log_end_msg 1 ;;
            *) [ "$VERBOSE" != no ] && log_failure_msg "failed to start" && log_end_msg 1 ;;
        esac
        ;;
      *)
        [ "$VERBOSE" != no ] && log_failure_msg "failed to stop"
        [ "$VERBOSE" != no ] && log_end_msg 1
        ;;
    esac
    ;;
  *)
    echo "Usage: $SCRIPTNAME {start|stop|status|restart|force-reload}" >&2
    exit 3
    ;;
esac

:
