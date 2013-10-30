#!/bin/bash

SCRIPTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"


#Import global config file
. $SCRIPTDIR/global.cfg


clear

# Create a temp folder for later operations
mkdir -p $SCRIPT_TMP_FOLDER

# Remove old stuff from tmp folder (if there's something)
rm -rf $SCRIPT_TMP_FOLDER/~

# Install dependencies
. ./dependencies.sh

# Install applications
. ./applications/magento.sh


# Cleanup
rm -rf $SCRIPT_TMP_FOLDER/~
