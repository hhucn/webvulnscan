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

#mkdir -p /home/wvsvm/Desktop

#cp /wvsvm-init/aufgaben.tar.bz2 /home/wvsvm/
#tar -C /home/wvsvm/ -x -f /wvsvm-init/aufgaben.tar.bz2
#tar -C /home/wvsvm/ -x -f /wvsvm-init/xfce-config.tar.bz2

#echo -e 'Username: webvulnscan\nPassword: 123456\nroot with sudo -s\n' > /home/wvsvm/Desktop/password
chown -R webvulnscan:webvulnscan /home/webvulnscan/

#aptitude purge -y linux-image-2.6.24-26-generic linux-restricted-modules-2.6.24-26-generic linux-ubuntu-modules-2.6.24-26-generic linux-headers-2.6.24-16

#find /wvsvm-init -type f -exec shred -n 0 -z --remove '{}' ';'
#rm -rf /wvsvm-init

echo INSTALLATION successful
