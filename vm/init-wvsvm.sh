#!/bin/sh

#grep -q wvsvm /etc/sudoers || /bin/echo -e '\n\nwebvulnscan ALL=(ALL) NOPASSWD: ALL\n' >> /etc/sudoers # Update System
apt-get -y update > /dev/null 2>&1

DEBIAN_FRONTEND=noninteractive apt-get -qqy install git-core htop axel unzip

chown -R webvulnscan:webvulnscan /wvsvm-init

mkdir -p /mnt/VBoxISO

if mount | grep -q "VBoxGuestAdditions"; then
#mounted=$(mount | grep "VBoxGuestAdditions")
#if [ "$mounted" = "" ]; then
	mount -o loop /wvsvm-init/VBoxGuestAdditions_4.3.6.iso /mnt/VBoxISO
fi

sh /mnt/VBoxISO/VBoxLinuxAdditions.run --nox11 <<!
yes
!

sudo umount /mnt/VBoxISO


# install applications
sh -c "/wvsvm-init/init-wvsvm-apps.sh" webvulnscan


echo INSTALLATION successful
function startLogging {
    
}