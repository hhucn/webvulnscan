#!/bin/sh

DEBUG=true
logfile=/var/log/webvulnscan.log

sudo grep -q webvulnscan /etc/sudoers || 

if ! sudo grep -q webvulnscan /etc/sudoers ; then
	/bin/echo -e '\n\nwebvulnscan ALL=(ALL) NOPASSWD: ALL\n' | sudo tee -a /etc/sudoers > /dev/null
fi

sudo apt-get -y update > /dev/null 2>&1

sudo DEBIAN_FRONTEND=noninteractive apt-get -qqy install git htop axel unzip

sudo chown -R webvulnscan:webvulnscan /wvsvm-init

sudo mkdir -p /mnt/VBoxISO

mounted=$(mount | grep "VBoxGuestAdditions")
if [ "$mounted" = "" ]; then
	sudo mount -o loop /wvsvm-init/VBoxGuestAdditions_4.3.6.iso /mnt/VBoxISO
fi

echo yes | sudo sh /mnt/VBoxISO/VBoxLinuxAdditions.run --nox11

sudo umount /mnt/VBoxISO

mkdir -p /home/webvulnscan/Desktop/
cd /home/webvulnscan/Desktop/
git clone https://github.com/hhucn/webvulnscan.git
cd webvulnscan
git checkout installscripts
cd targets
./install.sh