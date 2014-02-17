
# dependencies: genisoimage cpio

ISO_URL=http://cdimage.debian.org/debian-cd/7.4.0/i386/iso-cd/debian-7.4.0-i386-CD-1.iso
UBUNTU_ISO=debian-7.4.0-i386-CD-1.iso
#http://cdimage.debian.org/debian-cd/7.3.0/amd64/iso-cd/debian-7.3.0-amd64-CD-1.iso
OUT_ISO=vm.iso
VM_NAME=netsecvm
GUEST_ADDITIONS_FILE=VBoxGuestAdditions_4.3.6.iso
GUEST_ADDITIONS_URL=http://download.virtualbox.org/virtualbox/4.3.6/VBoxGuestAdditions_4.3.6.iso
OVA_NAME=netsecvm.ova

default: all

all: prepare
	$(MAKE) iso
	$(MAKE) makevm

prepare: download
	$(MAKE) cdtar
	$(MAKE) copystuff

update: copystuff
	$(MAKE) iso
	$(MAKE) startvm

download:
	test -f "${UBUNTU_ISO}" || wget "${ISO_URL}" -O "${UBUNTU_ISO}"
	test -f "${GUEST_ADDITIONS_FILE}" || wget "${GUEST_ADDITIONS_URL}" -O "${GUEST_ADDITIONS_FILE}"

cdtar:
	mkdir -p mount
	sudo umount mount 2>/dev/null || true
	sudo mount -o loop "${UBUNTU_ISO}" mount
	sudo rm -rf cdroot
	mkdir cdroot
	cd cdroot && tar cf - ../mount --transform 's,^mount/,,' | tar xf -
	sudo umount mount && rm -r mount
	chmod -R a+rw cdroot

initrd-mod:
	test -e cdroot/install.386/initrd.orig.gz || cp cdroot/install.386/initrd.gz cdroot/install.386/initrd.orig.gz

	sudo rm -rf initrd
	mkdir -p initrd
	cd initrd && gunzip <../cdroot/install.386/initrd.orig.gz | sudo cpio -i
	cp preseed initrd/preseed.cfg
	
	mkdir -p initrd/netsec-init
	#cp init-netsecvm.sh initrd/netsec-init/
	#cp init_netsec_service.sh initrd/netsec-init/
	cp "${GUEST_ADDITIONS_FILE}" initrd/netsec-init/

	cd initrd && find . | sudo cpio -o --format=newc | gzip -9 > ../cdroot/install.386/initrd.gz
	sudo rm -rf initrd

copystuff: initrd-mod
	#cp isolinux.cfg cdroot/isolinux/isolinux.cfg

iso:
	genisoimage -o "${OUT_ISO}" -quiet \
		-force-rr -J -joliet-long \
		-b isolinux/isolinux.bin -c isolinux/boot.cat \
		-no-emul-boot -boot-load-size 4 -boot-info-table \
		cdroot

clean:
	sudo rm -rf mount cdroot initrd aufgaben aufgaben.tar.bz2 "${OUT_ISO}"

cleanall: clean
	rm -f "${UBUNTU_ISO}" "${GUEST_ADDITIONS_FILE}"

makevm:
	VBoxManage createvm --name ${VM_NAME} --register
	VBoxManage modifyvm ${VM_NAME} --ostype Ubuntu --memory 512 --vram 12 --audio none --pae off --ioapic on
	VBoxManage modifyvm ${VM_NAME} --nic1 nat
	VBoxManage createhd --filename ${VM_NAME}.vdi --size 8000 --format VDI
	VBoxManage storagectl ${VM_NAME} --name "SATA Controller" --add sata --controller IntelAhci
	VBoxManage storageattach  ${VM_NAME} --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium ${VM_NAME}.vdi
	VBoxManage storagectl ${VM_NAME} --name "IDE Controller" --add ide --controller PIIX4
	VBoxManage storageattach ${VM_NAME} --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium ${OUT_ISO}
	$(MAKE) startvm
	

ova:
	./set_vm_description.py ${VM_NAME} 'Webvulnscan VM with preinstalled applications'
	VBoxManage storageattach ${VM_NAME} --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium emptydrive
	VBoxManage setextradata ${VM_NAME} GUI/Fullscreen off
	VBoxManage setextradata ${VM_NAME} GUI/LastGuestSizeHint 1000,700
	VBoxManage setextradata ${VM_NAME} GUI/LastNormalWindowPosition 100,100,1000,745
	VBoxManage modifyvm ${VM_NAME} --nic1 none

	rm -f "${OVA_NAME}"
	VBoxManage -nologo export ${VM_NAME} -o "${OVA_NAME}" \
		--vsys 0 \
		--product 'Webvulnscan-VM' \
		--vendor 'Lehrstuhl Rechnernetze, HHU Düsseldorf' \
		--vendorurl 'https://github.com/hhucn/webvulnscan' \
		--version "$$(date +%Y-%m-%d)"
	chmod a+r "${OVA_NAME}"
	sha512sum "${OVA_NAME}" > "${OVA_NAME}.sha512"

stopvm:
	VBoxManage -nologo controlvm ${VM_NAME} poweroff 2> /dev/null || true
	sleep 1

startvm: stopvm
	VBoxManage -nologo startvm ${VM_NAME}

.PHONY: default all prepare u update download cdtar i vm-tarball initrd-mod copystuff iso clean cleanall ova stopvm startvm
