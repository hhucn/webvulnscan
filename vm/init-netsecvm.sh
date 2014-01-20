#!/bin/sh

set -e

aptitude clean && aptitude update && aptitude dist-upgrade -y && aptitude clean && \
aptitude install -y \
	build-essential gdb unzip zip mercurial htop \
	linux-headers-2.6.24-32 linux-headers-2.6.24-32-generic \
    dkms \
	nasm dosbox \
	xfonts-base xkb-data xserver-xorg-video-vesa xserver-xorg xserver-xorg-input-mouse xserver-xorg-input-synaptics xserver-xorg-input-kbd \
	xfwm4 xfdesktop4 xfce4-taskmanager xfce4-session xfce4-taskmanager xfce4-panel xfce4-utils xfce4-appfinder xfce4-battery-plugin \
	tango-icon-theme tango-icon-theme-common xcursor-themes xfwm4-themes  \
	gtk2-engines-xfce xfce4-icon-theme \
	gdm gdm-themes xterm xarchiver thunar xfce4-terminal geany evince \
	nmap
aptitude clean

sed -i 's#^timeout\s\{0,\}3#timeout 0#' /boot/grub/menu.lst
grep -q netsec /etc/sudoers || /bin/echo -e '\n\nnetsec ALL=(ALL) NOPASSWD: ALL\n' >> /etc/sudoers
grep -q netsec /etc/gdm/gdm.conf || ( \
	sed -i 's#\(AutomaticLoginEnable=\)false#\1true#' /etc/gdm/gdm.conf && \
	sed -i 's#\(AutomaticLogin=\)#\1netsec#' /etc/gdm/gdm.conf \
)

# Add obscure service for IDS task
echo 'cisco-sccp 2000/tcp' >> /etc/services

chmod a+x /netsec-init/vbox-guestutils.sh
if ! /netsec-init/vbox-guestutils.sh; then
	echo "Installation of VirtualBox guest additions FAILED!"
	exit 1
fi

grep -q kernel.randomize_va_space /etc/sysctl.conf || /bin/echo -e '\n\n# Disable ASLR\nkernel.randomize_va_space=0' >> /etc/sysctl.conf && sysctl -p

mkdir -p /home/netsec/Desktop
cp /netsec-init/aufgaben.tar.bz2 /home/netsec/
tar -C /home/netsec/ -x -f /netsec-init/aufgaben.tar.bz2
tar -C /home/netsec/ -x -f /netsec-init/xfce-config.tar.bz2
echo -e 'Benutzername: netsec\nPasswort: 123456\nroot-Rechte mit sudo -s\n' > /home/netsec/Desktop/passwort
chown -R netsec:netsec /home/netsec/

aptitude purge -y linux-image-2.6.24-26-generic linux-restricted-modules-2.6.24-26-generic linux-ubuntu-modules-2.6.24-26-generic linux-headers-2.6.24-16

find /netsec-init -type f -exec shred -n 0 -z --remove '{}' ';'
rm -rf /netsec-init

echo INSTALLATION successful
