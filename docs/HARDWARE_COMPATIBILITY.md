# HyperOS Hardware Compatibility Matrix

**Version:** 0.6.0 Beta  
**Last Updated:** 2024  
**Status:** Active Testing

---

## Overview

This document tracks verified hardware compatibility for HyperOS v0.6.0. Components are classified as:

- ✅ **SUPPORTED**: Fully functional, tested
- ⚠️ **PARTIAL**: Works with limitations or known issues
- ❌ **UNSUPPORTED**: Known incompatibilities
- ❓ **UNKNOWN**: Not yet tested

---

## Processors (CPU)

### Intel

| Generation | Models | Status | Notes |
|------------|--------|--------|-------|
| 14th Gen (Raptor Lake R) | i9-14900K, i7-14700K | ✅ | Requires kernel 6.8+ |
| 13th Gen (Raptor Lake) | i9-13900K, i7-13700K | ✅ | Full support |
| 12th Gen (Alder Lake) | i9-12900K, i7-12700K | ✅ | P/E cores work correctly |
| 11th Gen (Rocket/Tiger Lake) | i9-11900K, i7-1185G7 | ✅ | Iris Xe graphics supported |
| 10th Gen (Comet/Ice Lake) | i9-10900K, i7-1065G7 | ✅ | Stable |
| 8th-9th Gen (Coffee Lake) | i7-9700K, i5-8600K | ✅ | Recommended minimum |
| 6th-7th Gen (Sky/Kaby Lake) | i7-7700K, i5-6600K | ✅ | May need LTS kernel for older models |
| Older (Haswell and earlier) | i7-4790K, etc. | ⚠️ | Use LTS kernel, limited AVX optimizations |

### AMD

| Generation | Models | Status | Notes |
|------------|--------|--------|-------|
| Ryzen 8000 (Zen 4c) | R7 8700G, R5 8600G | ✅ | Excellent iGPU support |
| Ryzen 7000 (Zen 4) | R9 7950X, R7 7700X | ✅ | AM5 platform fully supported |
| Ryzen 5000 (Zen 3) | R9 5950X, R7 5800X3D | ✅ | Optimal performance |
| Ryzen 3000 (Zen 2) | R9 3950X, R7 3700X | ✅ | Stable |
| Ryzen 2000 (Zen+) | R7 2700X, R5 2600 | ✅ | Good support |
| Ryzen 1000 (Zen) | R7 1800X, R5 1600 | ✅ | Minimum recommended |
| FX Series (Pre-Ryzen) | FX-8350, FX-6300 | ⚠️ | Works but no AVX2 optimizations |
| Athlon | 200GE, 3000G | ✅ | Budget builds supported |

---

## Graphics Cards (GPU)

### Intel Integrated

| GPU | Architecture | Status | Driver | Notes |
|-----|--------------|--------|--------|-------|
| UHD Graphics 770 | Rocket/Alder Lake | ✅ | i915/Mesa | Full Wayland support |
| UHD Graphics 730-750 | Comet/Rocket Lake | ✅ | i915/Mesa | Stable |
| UHD Graphics 630 | Coffee/Whiskey Lake | ✅ | i915/Mesa | Recommended minimum |
| UHD Graphics 620 | Kaby/Coffee Lake | ✅ | i915/Mesa | Good for basic use |
| UHD Graphics 610 | Coffee Lake | ⚠️ | i915/Mesa | Limited performance |
| Iris Xe | Tiger/Rocket Lake | ✅ | i915/Mesa | Excellent media encode |
| Iris Plus | Ice/Lake Lake | ✅ | i915/Mesa | Good performance |
| HD Graphics 630 | Kaby Lake | ⚠️ | i915/Mesa | Legacy, works but slow |
| HD Graphics 530 | Skylake | ⚠️ | i915/Mesa | Consider upgrade |

### AMD Radeon

| GPU Series | Examples | Status | Driver | Notes |
|------------|----------|--------|--------|-------|
| RDNA 3 (RX 7000) | RX 7900 XTX, RX 7800 XT | ✅ | amdgpu/Mesa | Native Wayland, Vulkan RADV |
| RDNA 2 (RX 6000) | RX 6900 XT, RX 6700 XT | ✅ | amdgpu/Mesa | Excellent support |
| RDNA 1 (RX 5000) | RX 5700 XT, RX 5600 | ✅ | amdgpu/Mesa | Stable |
| Vega | Vega 64, Vega 56, Vega 8/11 iGPU | ✅ | amdgpu/Mesa | Great Wayland support |
| Polaris | RX 580, RX 570, RX 480 | ✅ | amdgpu/Mesa | Best value, mature drivers |
| Fiji | R9 Fury, Nano | ✅ | amdgpu/Mesa | Legacy but supported |
| GCN 1-3 | R9 390, R9 280, HD 7970 | ⚠️ | amdgpu/radeon | May need radeon driver |
| Pre-GCN | HD 6970, HD 5870 | ❌ | radeon (legacy) | No Wayland, consider upgrade |

### NVIDIA

| GPU Series | Examples | Driver | Status | Notes |
|------------|----------|--------|--------|-------|
| Ada Lovelace (RTX 40xx) | RTX 4090, 4080, 4070 | nvidia-open/nvidia-550 | ✅ | Excellent, native Wayland |
| Ampere (RTX 30xx) | RTX 3090, 3080, 3070 | nvidia-open/nvidia-550 | ✅ | Full support |
| Turing (RTX 20xx) | RTX 2080 Ti, 2070 | nvidia-550 | ✅ | Good Wayland support |
| Pascal (GTX 10xx) | GTX 1080 Ti, 1070 | nvidia-470/nvidia-550 | ✅ | Works well |
| Maxwell (GTX 9xx) | GTX 980 Ti, 970 | nvidia-470 | ⚠️ | Suspend issues on Wayland |
| Kepler (GTX 7xx) | GTX 780 Ti, 770 | nvidia-470 | ⚠️ | Legacy, X11 recommended |
| Fermi (GTX 5xx) | GTX 580, 570 | nvidia-390 | ❌ | No Wayland, EOL driver |
| Older | GTX 4xx, GT 2xx | nouveau | ⚠️ | Basic functionality only |

**Driver Notes:**
- `nvidia-open`: New open kernel module (RTX 20xx+ recommended)
- `nvidia-550`: Latest proprietary driver
- `nvidia-470`: Legacy driver (GTX 9xx/7xx)
- `nouveau`: Open source, limited performance

---

## Network Adapters

### Ethernet

| Vendor | Chipset | Driver | Status | Notes |
|--------|---------|--------|--------|-------|
| Intel | I225-V, I210, I219-V | igc, e1000e | ✅ | Excellent support |
| Intel | I350, 82574L | e1000e | ✅ | Server grade |
| Realtek | RTL8125B (2.5GbE) | r8125 | ✅ | Fast, stable |
| Realtek | RTL8111/8168 | r8168/r8169 | ✅ | Most common |
| Realtek | RTL8105/8106 | r8101 | ✅ | Budget boards |
| Atheros | AR81xx | alx | ✅ | Older systems |
| Broadcom | BCM57xx | tg3 | ✅ | Enterprise NICs |
| Mellanox | ConnectX | mlx5_core | ⚠️ | Server/DPU, may need firmware |

### WiFi

| Vendor | Chipset | Driver | Status | Notes |
|--------|---------|--------|--------|-------|
| Intel | AX210, AX200, AC9560 | iwlwifi | ✅ | Excellent, suspend OK |
| Intel | AC8265, AC8260 | iwlwifi | ✅ | Stable |
| Intel | AC7260, AC7265 | iwlwifi | ✅ | Mature |
| Intel | Older (5100, 5300) | iwlwifi | ⚠️ | May need older firmware |
| MediaTek | MT7921, MT7922 | mt7921e | ✅ | Newer laptops |
| Qualcomm/Atheros | QCA6174, QCA9377 | ath10k | ✅ | Common in laptops |
| Qualcomm/Atheros | QCA9880, QCA99X0 | ath10k | ✅ | Desktop cards |
| Realtek | RTL8822CE | rtw_8822ce | ⚠️ | Needs manual driver install |
| Realtek | RTL88x2BU | 88x2bu | ⚠️ | USB adapters, AUR driver |
| Broadcom | BCM43xx | broadcom-wl | ⚠️ | Proprietary, secure boot issues |
| Broadcom | BCM4313, BCM43224 | brcmfmac | ⚠️ | Hit or miss |

**WiFi Firmware Notes:**
- Intel: Firmware in `linux-firmware` package
- Some Realtek chips require AUR packages
- Broadcom often needs `broadcom-wl-dkms`

---

## Audio

### Audio Solutions

| Type | Codec/Chip | Driver | Status | Notes |
|------|------------|--------|--------|-------|
| Intel HDA | ALC1220, ALC892, ALC887 | snd_hda_intel | ✅ | Most desktop boards |
| Intel HDA | Realtek laptop codecs | snd_hda_intel | ✅ | Auto-muting works |
| Intel SST/SOF | Modern laptops | sof-audio-pci | ✅ | Requires firmware |
| AMD HDMI/DP | Radeon audio | snd_hda_intel | ✅ | GPU output |
| NVIDIA HDMI | GPU audio | snd_hda_intel | ✅ | GPU output |
| USB Audio | Generic DACs | snd_usb_audio | ✅ | Plug & play |
| Bluetooth | A2DP sink | bluez, pipewire | ✅ | Requires pairing |

**Audio Server:** PipeWire + WirePlumber (default)

---

## Bluetooth

| Adapter | Chipset | Driver | Status | Notes |
|---------|---------|--------|--------|-------|
| Intel | AX210, AX200 | btusb | ✅ | Paired with WiFi |
| Intel | AC8265, AC8260 | btusb | ✅ | Stable |
| Realtek | RTL8723BS, RTL8822B | btusb | ⚠️ | May need firmware reload |
| Qualcomm/Atheros | AR3012, QCA6174 | btusb | ✅ | Common |
| Broadcom | BCM20702, BCM43142 | btusb | ⚠️ | Firmware loading issues possible |
| CSR | Cambridge Silicon Radio | btusb | ✅ | Cheap USB dongles |

---

## Storage Controllers

### SATA/NVMe

| Type | Controller | Driver | Status | Notes |
|------|------------|--------|--------|-------|
| NVMe | Samsung, WD, Crucial, SK Hynix | nvme | ✅ | All major brands |
| SATA AHCI | Intel, AMD chipsets | ahci | ✅ | Standard |
| SATA RAID | Intel RST | ahci/Intel RST | ⚠️ | Use AHCI mode for Linux |
| NVMe RAID | Intel VMD | vmd | ⚠️ | May need BIOS disable |

**Filesystems Supported:**
- ext4 (default) ✅
- Btrfs ⚠️ (manual snapshot setup)
- XFS ✅
- FAT32/EFI ✅
- NTFS (read/write) ✅ via ntfs-3g
- exFAT ✅

---

## Laptop Features

| Feature | Status | Notes |
|---------|--------|-------|
| Lid Close/Suspend | ✅ | Configurable in settings |
| Power Button | ✅ | systemd handles |
| Brightness Keys | ✅ | Hyprland binds |
| Touchpad (I2C HID) | ✅ | libinput |
| Touchpad (PS/2) | ✅ | synaptics/libinput |
| Fingerprint Reader | ⚠️ | fprintd, limited device support |
| Webcam | ✅ | UVC standard |
| SD Card Reader | ✅ | mmc_block |
| Thunderbolt 3/4 | ✅ | bolt daemon |
| USB-C PD Charging | ✅ | Kernel handles |
| Hybrid Graphics (Optimus) | ⚠️ | Requires manual setup |

---

## Peripherals

### Input Devices

| Type | Connection | Status | Notes |
|------|------------|--------|-------|
| USB Keyboard | USB | ✅ | Plug & play |
| Bluetooth Keyboard | BT | ✅ | Pairing required |
| USB Mouse | USB | ✅ | Plug & play |
| Bluetooth Mouse | BT | ✅ | Pairing required |
| Gaming Mouse (RGB) | USB | ⚠️ | RGB needs OpenRGB |
| Trackpoint | Internal | ✅ | ThinkPad supported |
| Drawing Tablet | USB | ✅ | Wacom (libwacom), Huion ⚠️ |

### Printers/Scanners

| Brand | Support | Notes |
|-------|---------|-------|
| HP | ✅ | hplip package |
| Brother | ✅ | Official drivers available |
| Canon | ⚠️ | Some models need AUR |
| Epson | ✅ | epson-escpr |
| Xerox | ✅ | Generic drivers |

---

## Known Incompatibilities

| Hardware | Issue | Workaround |
|----------|-------|------------|
| NVIDIA Fermi (GTX 5xx) | No Wayland, EOL driver | Use X11 or upgrade GPU |
| Broadcom BCM43142 | Secure boot conflict | Disable secure boot or enroll keys |
| Realtek RTL8822CE WiFi | Driver not in mainline | Install from AUR |
| Some fingerprint readers | No Linux driver | Windows-only feature |
| Very new CPUs (< 3 months) | May need kernel update | Use LTS or staging kernel |
| Fake/clone hardware | Unpredictable | Buy genuine components |

---

## Testing Protocol

Hardware is marked as **SUPPORTED** when:

1. ✅ Detected automatically
2. ✅ Functions without manual configuration
3. ✅ Survives suspend/resume cycle
4. ✅ Works in Wayland session
5. ✅ Tested on real hardware (not just VM)

Hardware is marked as **PARTIAL** when:

1. ⚠️ Requires manual driver installation
2. ⚠️ Has known bugs with workarounds
3. ⚠️ Limited functionality (e.g., no RGB control)
4. ⚠️ Suspend/resume issues

---

## How to Contribute

If you have tested hardware not listed here:

1. Run `hyper-diagnose --full` and save output
2. Note exact hardware model (use `lspci`, `lsusb`)
3. Test all functions (network, audio, suspend, etc.)
4. Submit results to HyperOS hardware database

```bash
# Example submission command (future)
hyper submit-hardware-report --file report.json
```

---

## Resources

- **Diagnostic Tool:** `scripts/hyper-diagnose.sh`
- **Arch Wiki Hardware:** https://wiki.archlinux.org/title/Hardware
- **PCI Database:** https://pci-ids.ucw.cz/
- **USB Database:** http://www.linux-usb.org/

---

**Disclaimer:** This matrix reflects testing as of v0.6.0 Beta. Hardware compatibility may improve in future releases through kernel updates and driver improvements.
