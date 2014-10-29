#!/bin/sh

set -e

#grep -q wvsvm /etc/sudoers || /bin/echo -e '\n\nwebvulnscan ALL=(ALL) NOPASSWD: ALL\n' >> /etc/sudoers

sudo chown -R webvulnscan:webvulnscan /wvsvm-init

sudo mkdir -p /mnt/VBoxISO
sudo mount -o loop /wvsvm-init/VBoxGuestAdditions_4.3.6.iso /mnt/VBoxISO

sh /mnt/VBoxISO/VBoxLinuxAdditions.run --nox11 <<!
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
