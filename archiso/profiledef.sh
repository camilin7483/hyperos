#!/usr/bin/env bash
# shellcheck disable=SC2034

iso_name="hyperos"
iso_label="HYPEROS_202607"
iso_publisher="HyperOS <https://hyperos.org>"
iso_application="HyperOS Live/Rescue CD"
iso_version="$(date +%Y.%m.%d)"
install_dir="arch"
buildmodes=('iso')
bootmodes=(
    'bios.syslinux.mbr'
    'bios.syslinux.eltorito'
    'uefi-x64.systemd-boot.esp'
    'uefi-x64.systemd-boot.eltorito'
)
arch="x86_64"
pacman_conf="pacman.conf"
airootfs_image_type="squashfs"
mkinitcpio_conf="mkinitcpio.conf"
airootfs_image_tool_options=('-comp' 'xz' '-Xbcj' 'x86' '-b' '1M')
file_permissions=(
    ["/etc/shadow"]="0:0:400"
    ["/etc/gshadow"]="0:0:400"
    ["/root"]="0:0:750"
    ["/usr/local/bin/hyperos-before"]="0:0:755"
    ["/usr/local/bin/hyperos-welcome"]="0:0:755"
)
