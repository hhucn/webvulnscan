#!/bin/sh

grep -q webvulnscan /etc/sudoers || /bin/echo -e '\n\nwebvulnscan ALL=(ALL) NOPASSWD: ALL\n' >> /etc/sudoers

apt-get -y update >/dev/null 2>&1

DEBIAN_FRONTEND=noninteractive apt-get -qqy install git-core htop axel unzip

chown -R webvulnscan:webvulnscan /wvsvm-init

mkdir -p /mnt/VBoxISO

if mount | grep -q "VBoxGuestAdditions"; then
	mount -o loop /wvsvm-init/VBoxGuestAdditions_4.3.6.iso /mnt/VBoxISO
fi

echo yes | sudo sh /mnt/VBoxISO/VBoxLinuxAdditions.run --nox11

sudo umount /mnt/VBoxISO

# install applications
su -c "/wvsvm-init/init-wvsvm-apps.sh" webvulnscan

echo INSTALLATION successful
