#!/bin/sh

DEBUG=true
logfile=/var/log/webvulnscan.log

exec > >(gawk -v pid=$$ '{ print strftime("%F-%T"),pid,$0; fflush(); }' | tee -a $logfile)
    [ ! -z "$DEBUG" ] && exec 2>&1 || exec 2> >(gawk -v pid=$$ '{ print strftime("%F-%T"),pid,$0; fflush(); }' >>$logfile)
    echo "=== Log started for $$ at $(date +%F-%T) ==="

set -e

#grep -q wvsvm /etc/sudoers || /bin/echo -e '\n\nwebvulnscan ALL=(ALL) NOPASSWD: ALL\n' >> /etc/sudoers
# Update System
sudo apt-get -y update > /dev/null 2>&1

sudo DEBIAN_FRONTEND=noninteractive apt-get -qqy install git-core htop axel unzip

sudo chown -R webvulnscan:webvulnscan /wvsvm-init

sudo mkdir -p /mnt/VBoxISO

mounted=$(mount | grep "VBoxGuestAdditions")
if [ "$mounted" = "" ]; then
	sudo mount -o loop /wvsvm-init/VBoxGuestAdditions_4.3.6.iso /mnt/VBoxISO
fi

sudo sh /mnt/VBoxISO/VBoxLinuxAdditions.run --nox11 <<!
yes
!

sudo umount /mnt/VBoxISO

mkdir -p /home/webvulnscan/Desktop/
cd /home/webvulnscan/Desktop/
git clone https://github.com/hhucn/webvulnscan.git
cd webvulnscan
git checkout installscripts
cd targets
./install.sh

echo INSTALLATION successful
function startLogging {
    
}