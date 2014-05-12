#sudo apt-get -y install mercurial
cd $TMPDIR/

#rm -rf idempiere-installation-script
rm -rf idempiere*

# remove old installer-folder inside user-home-directory
rm -rf $USER_HOME/installer_201*

hg clone https://bitbucket.org/cboecking/idempiere-installation-script
chmod 766 idempiere-installation-script/*.sh 
./idempiere-installation-script/idempiere_install_script_master_linux.sh -u $USER_NAME -p -l &>idempiere_output.txt

