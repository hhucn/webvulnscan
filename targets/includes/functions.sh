#!/bin/bash

function print () {
	if [ "$webvulnscanTargetsVerbose" = 1 ];
	then
		echo ${1}
	fi


}

function checkPackageInstalled() {
	PKG_OK=$(dpkg-query -W --showformat='${Status}\n' "$1"|grep "install ok installed")
	if [ "" == "$PKG_OK" ]; then
		return 1
	else
		return 0
	fi
}

function installPackage() {
	echo "... installing" "$1"	# debug
	sudo DEBIAN_FRONTEND=noninteractive apt-get -qq --force-yes install $1 > /dev/null
}

function usage {
        echo ""
        echo "Install-script usage"
        echo "   -v, make output more verbose"
        echo ""
        echo "   -h, print this message"
        echo ""
        exit
}




