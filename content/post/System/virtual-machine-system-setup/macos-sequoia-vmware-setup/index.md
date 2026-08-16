---
title: "在 Windows 的 VMware 中安装 macOS Sequoia"
date: 2026-08-16
description: "使用 Apple BaseSystem Recovery、VMware Workstation 和两块 VMDK，从零安装可启动的 macOS Sequoia 虚拟机。"
categories:
  - "系统"
tags:
  - "macOS Sequoia"
  - "VMware Workstation"
  - "虚拟机"
  - "Windows"
  - "Apple Recovery"
  - "系统安装"
draft: false
slug: "macos-sequoia-vmware-setup"
related_group: "virtual-machine-system-setup"
hidden: true
searchable: true
guide: "/p/virtual-machine-system-setup-guide/"
guide_title: "虚拟机系统部署指南"
---

> 在非 Apple 硬件上运行 macOS，以及修改 Windows 版 VMware 的 macOS 来宾支持，可能不受 Apple 或 VMware 官方支持。操作前请自行确认授权、许可条款和风险。

## 1. 准备环境

本次验证使用以下版本：

| 工具 | 版本 | 用途 |
| --- | --- | --- |
| VMware Workstation | 17.6.4 | 运行 macOS 虚拟机 |
| Unlocker | 4.2.8 | VMware 中没有 macOS 来宾选项时使用 |
| OpenCorePkg | 1.0.7 | 只使用其中的 `macrecovery.py` |
| dmg2img | 1.6.7 | 把 `BaseSystem.dmg` 转成 raw IMG |
| VirtualBox | 7.2.14 | 只使用 `VBoxManage.exe` 转换和创建磁盘 |
| Python | Windows Python 3 | 运行 `macrecovery.py` |
| 7-Zip | 26.02 | 解压工具包 |

下载入口：

- [VMware Workstation 产品页](https://www.vmware.com/products/desktop-hypervisor/workstation-and-fusion)
- [Unlocker 4.2.8](https://github.com/DrDonk/unlocker/releases/tag/v4.2.8)
- [OpenCorePkg 1.0.7](https://github.com/acidanthera/OpenCorePkg/releases/tag/1.0.7)
- [dmg2img 工具页](http://vu1tur.eu.org/tools/)
- [VirtualBox 7.2.14 Windows 安装包](https://download.virtualbox.org/virtualbox/7.2.14/VirtualBox-7.2.14-174565-Win.exe)
- [Python for Windows](https://www.python.org/downloads/windows/)
- [7-Zip](https://www.7-zip.org/)

建立工作目录：

```powershell
$base = 'D:\Downloads\SignRiver-Test-OS'
foreach ($d in @('macos','macos\recovery','vmware','tools')) {
    New-Item -ItemType Directory -Force -Path (Join-Path $base $d) | Out-Null
}
```

后文都使用这个路径。如果你换到其他目录，必须同步修改所有命令和 VMX 中的磁盘路径。

## 2. 安装 VMware 并准备 macOS 来宾支持

正常安装 VMware Workstation 17.6.4，启动一次确认程序可用，然后完全退出 VMware：

```powershell
Get-Process vmware,vmware-vmx -ErrorAction SilentlyContinue
```

如果 VMware 的新建虚拟机向导中已经有 64 位 macOS 来宾，可以直接进入下一节。

如果没有 macOS 来宾选项：

1. 备份 VMware 安装目录和现有虚拟机；
2. 解压 Unlocker 4.2.8；
3. 完全退出 VMware；
4. 以管理员身份运行 `windows\unlock.exe`；
5. 使用同目录的 `check.exe` 检查补丁状态。

> VMware 升级或修复安装可能覆盖 Unlocker。不要运行来源不明的 Unlocker，也不要在 VMware 进程仍运行时打补丁。

## 3. 下载 Apple BaseSystem Recovery

解压 `OpenCore-1.0.7-RELEASE.zip` 到：

```text
D:\Downloads\SignRiver-Test-OS\tools\OpenCore-1.0.7
```

本路线不使用 OpenCore 引导器、Kext 或 `config.plist`，只使用：

```text
D:\Downloads\SignRiver-Test-OS\tools\OpenCore-1.0.7\Utilities\macrecovery\macrecovery.py
```

确认 Python 可用，然后动态下载当前 Apple Recovery：

```powershell
python --version

$mr = 'D:\Downloads\SignRiver-Test-OS\tools\OpenCore-1.0.7\Utilities\macrecovery\macrecovery.py'
$out = 'D:\Downloads\SignRiver-Test-OS\macos\recovery'

New-Item -ItemType Directory -Force -Path $out | Out-Null
python $mr download -o $out -v 2>&1 |
  Tee-Object 'D:\Downloads\SignRiver-Test-OS\macos\recovery-download.log'
```

完成后应得到：

```text
D:\Downloads\SignRiver-Test-OS\macos\recovery\BaseSystem.dmg
D:\Downloads\SignRiver-Test-OS\macos\recovery\BaseSystem.chunklist
```

检查文件大小和 SHA256：

```powershell
Get-Item "$out\BaseSystem.dmg", "$out\BaseSystem.chunklist" |
  Select-Object Name,Length

Get-FileHash "$out\BaseSystem.dmg", "$out\BaseSystem.chunklist" -Algorithm SHA256
```

本次成功安装 Sequoia 时得到的文件为：

| 文件 | 大小 | SHA256 |
| --- | ---: | --- |
| `BaseSystem.dmg` | `884317790` bytes | `7314eb401f5e84087f621b3599f0ad21ca3cdcc2685ea2da7f76806792328e20` |
| `BaseSystem.chunklist` | `3352` bytes | `dbf262b83a16d55f1b2d8ce8ce95986561f8e889719524ea4b7aa22a2417ca27` |

Apple 以后可能返回不同版本。若大小或哈希不同，先确认镜像对应的 macOS 版本，不要只看文件名就继续。

## 4. 转换 Recovery 并创建系统盘

安装 VirtualBox 后，确认以下程序存在：

```text
C:\Program Files\Oracle\VirtualBox\VBoxManage.exe
```

解压 dmg2img。本次使用的程序路径为：

```text
D:\Downloads\SignRiver-Test-OS\tools\dmg2img\extracted\dmg2img.exe
```

先把 DMG 转成 raw IMG，再转成 VMDK：

```powershell
$dmg2img = 'D:\Downloads\SignRiver-Test-OS\tools\dmg2img\extracted\dmg2img.exe'
$recovery = 'D:\Downloads\SignRiver-Test-OS\macos\recovery'
$VBoxManage = 'C:\Program Files\Oracle\VirtualBox\VBoxManage.exe'

& $dmg2img `
  "$recovery\BaseSystem.dmg" `
  "$recovery\BaseSystem.img"

if ($LASTEXITCODE -ne 0) { throw 'dmg2img 转换失败' }

& $VBoxManage convertfromraw `
  "$recovery\BaseSystem.img" `
  "$recovery\BaseSystem.vmdk" `
  --format VMDK

if ($LASTEXITCODE -ne 0) { throw 'VBoxManage convertfromraw 失败' }
```

创建 100 GiB 左右的动态系统盘：

```powershell
$mac = 'D:\Downloads\SignRiver-Test-OS\macos'

& $VBoxManage createmedium disk `
  --filename "$mac\macos-disk.vdi" `
  --size 102400 `
  --format VDI

if ($LASTEXITCODE -ne 0) { throw '创建目标 VDI 失败' }

& $VBoxManage clonemedium disk `
  "$mac\macos-disk.vdi" `
  "$mac\macos-disk.vmdk" `
  --format VMDK

if ($LASTEXITCODE -ne 0) { throw '目标盘转 VMDK 失败' }
```

最终要有两块磁盘：

```text
D:\Downloads\SignRiver-Test-OS\macos\recovery\BaseSystem.vmdk
D:\Downloads\SignRiver-Test-OS\macos\macos-disk.vmdk
```

`102400 MiB` 在 macOS 磁盘工具中会显示为约 `107.16 GB`，属于计量单位差异。

## 5. 创建 VMware 虚拟机

在 VMware Workstation 中执行以下操作：

1. 选择**创建新的虚拟机**，使用自定义配置；
2. 选择**稍后安装操作系统**；
3. 来宾系统选择 64 位 macOS；
4. 硬件兼容性选择 Workstation 17.x；
5. 虚拟机名称填写 `macOS Sequoia`；
6. 虚拟机目录设为 `D:\Downloads\SignRiver-Test-OS\vmware`；
7. 设置 4 个 vCPU，每插槽 2 核；
8. 内存设置为 8192 MB；
9. 固件选择 EFI；
10. 不创建新磁盘，或者在完成向导后移除向导创建的磁盘；
11. 完成后不要启动虚拟机，并完全退出 VMware。

找到新生成的 `macOS Sequoia.vmx`，确认虚拟机未运行并备份：

```powershell
$vmrun = 'C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe'
$vmx = 'D:\Downloads\SignRiver-Test-OS\vmware\macOS Sequoia.vmx'

& $vmrun list
Get-Process vmware-vmx -ErrorAction SilentlyContinue
Copy-Item $vmx "$vmx.before-initial-config"
```

用文本编辑器打开 VMX。保留向导生成的其他内容，替换同名配置项；不要在文件末尾重复追加相同键：

```ini
.encoding = "UTF-8"
config.version = "8"
virtualHW.version = "21"
displayName = "macOS Sequoia"
guestOS = "darwin24-64"
firmware = "efi"

numvcpus = "4"
cpuid.coresPerSocket = "2"
memsize = "8192"

smc.present = "TRUE"
smc.version = "0"
board-id.reflectHost = "TRUE"
hw.model.reflectHost = "TRUE"
serialNumber.reflectHost = "TRUE"
smbios.reflectHost = "TRUE"

sata0.present = "TRUE"
sata0.pciSlotNumber = "36"
sata0:0.deviceType = "disk"
sata0:0.fileName = "D:/Downloads/SignRiver-Test-OS/macos/recovery/BaseSystem.vmdk"
sata0:0.present = "TRUE"
sata0:0.redo = ""
sata0:1.deviceType = "disk"
sata0:1.fileName = "D:/Downloads/SignRiver-Test-OS/macos/macos-disk.vmdk"
sata0:1.present = "TRUE"
sata0:1.redo = ""

ethernet0.present = "TRUE"
ethernet0.connectionType = "nat"
ethernet0.virtualDev = "vmxnet3"
ethernet0.addressType = "generated"
ethernet0.pciSlotNumber = "160"

pciBridge0.present = "TRUE"
pciBridge0.pciSlotNumber = "17"
pciBridge4.present = "TRUE"
pciBridge5.present = "TRUE"
pciBridge6.present = "TRUE"
pciBridge7.present = "TRUE"
pciBridge4.virtualDev = "pcieRootPort"
pciBridge4.functions = "8"
pciBridge5.virtualDev = "pcieRootPort"
pciBridge5.functions = "8"
pciBridge6.virtualDev = "pcieRootPort"
pciBridge6.functions = "8"
pciBridge7.virtualDev = "pcieRootPort"
pciBridge7.functions = "8"
pciBridge4.pciSlotNumber = "21"
pciBridge5.pciSlotNumber = "22"
pciBridge6.pciSlotNumber = "23"
pciBridge7.pciSlotNumber = "24"

usb.present = "TRUE"
usb.pciSlotNumber = "34"
usb_xhci.present = "TRUE"
usb_xhci.pciSlotNumber = "192"
keyboard.vusb.present = "TRUE"
keyboard.vusb.enable = "TRUE"
mouse.vusb.present = "TRUE"
mouse.vusb.enable = "TRUE"
mouse.vusb.useBasicMouse = "FALSE"
mouse.present = "FALSE"
vmmouse.present = "TRUE"
usb.generic.allowHID = "TRUE"

svga.vramSize = "268435456"
mks.enable3d = "FALSE"
```

检查关键配置：

```powershell
Select-String -Path $vmx -Pattern `
  '^(guestOS|firmware|sata0|ethernet0|pciBridge[4-7]|usb|usb_xhci|keyboard|mouse|vmmouse|mks)'
```

## 6. 启动 Recovery 并初始化系统盘

启动虚拟机：

```powershell
& $vmrun start $vmx gui
```

首次启动应直接进入 macOS Recovery。先确认鼠标和键盘可用，并且磁盘工具能看到约 107.16 GB 的目标盘。

在**磁盘工具**中：

1. 点击**显示所有设备**；
2. 选择约 107.16 GB 目标磁盘最上层的物理设备；
3. 点击**抹掉**；
4. 名称填写 `Macintosh HD`；
5. 格式选择 **APFS**；
6. 方案选择 **GUID Partition Map**；
7. 完成后退出磁盘工具。

> 不要抹掉 `BaseSystem` 或 Recovery 盘。

创建安装前快照：

```powershell
& $vmrun snapshot $vmx 'pre-sequoia-apfs-install'
```

## 7. 联网安装 macOS Sequoia

VMX 已固定使用 NAT 和 `vmxnet3`。需要确认网络时，在 Recovery 的**终端**中执行：

```bash
ifconfig en0
route -n get default
```

`en0` 应获得 VMware NAT 分配的正常地址。如果只看到 `169.254.x.x`，说明 DHCP 没有成功。

如果 Windows 宿主正在使用 Clash Verge、Mihomo 或其他 Fake-IP/TUN 代理，安装前临时把宿主代理切换为**直连**。本次验证中，规则模式会导致 Recovery 能连接 Apple CDN，但下载长期停在起点。安装完成后再恢复原来的代理模式。

网络正常后：

1. 退出磁盘工具；
2. 选择**安装 macOS**；
3. 选择刚才创建的 `Macintosh HD`；
4. 接受安装过程中的多次自动重启；
5. 重启期间不要强制关闭虚拟机；
6. 等待进入首次设置界面。

进入首次设置后创建快照：

```powershell
& $vmrun snapshot $vmx 'pre-account-setup'
```

## 8. 完成首次设置

如果界面已经是中文或英文，直接按向导选择地区、键盘、网络并创建本地账户。

本次验证使用的 Recovery 在安装后进入了俄语首次设置。如果你也遇到相同情况，按下一节修改语言；如果界面语言正常，跳到第 10 节。

## 9. 将俄语首次设置改为简体中文

先记录 VMX 当前实际连接的磁盘，再正常关机：

```powershell
Select-String -Path $vmx -Pattern '^sata0:[01]\.fileName|^sata0:[01]\.present'
& $vmrun stop $vmx soft
& $vmrun list
Get-Process vmware-vmx -ErrorAction SilentlyContinue
Copy-Item $vmx "$vmx.before-language-recovery"
```

等待虚拟机完全停止。此时 VMX 可能已经因为快照而引用 `macos-disk-000001.vmdk` 等差分盘。下面必须使用 VMX 中的当前文件名，不能改回基础 `macos-disk.vmdk`。

保持 BaseSystem 在 `sata0:0`，把目标系统盘临时改挂到 NVMe。例如当前系统盘是 `macos-disk-000001.vmdk` 时：

```ini
sata0:1.present = "FALSE"

nvme0.present = "TRUE"
nvme0:0.present = "TRUE"
nvme0:0.fileName = "macos-disk-000001.vmdk"
nvme0:0.redo = ""
nvme0.pciSlotNumber = "224"
```

重新启动后会从 SATA 上的 BaseSystem 进入 Recovery，同时能看到 NVMe 上已安装的 Sequoia。打开**终端**，先识别实际盘号：

```bash
diskutil list
diskutil apfs list
```

找到约 107 GB 目标盘对应的 APFS Container、System 卷和 Data 卷。本次验证中目标容器是 `disk2`，Data 卷是 `disk2s1`，System 卷挂载在 `/Volumes/macintosh hd`。你的盘号可能不同，必须按现场输出替换。

把 Data 卷挂载到系统卷的 firmlink 路径：

```bash
diskutil unmount disk2s1
/sbin/mount_apfs /dev/disk2s1 "/Volumes/macintosh hd/System/Volumes/Data"
D="/Volumes/macintosh hd/System/Volumes/Data"
```

备份并修改系统级语言偏好：

```bash
cp -p "$D/Library/Preferences/.GlobalPreferences.plist" \
  "$D/Library/Preferences/.GlobalPreferences.plist.before-zh"

plutil -replace AppleLanguages \
  -json '["zh-Hans-CN","en-US"]' \
  "$D/Library/Preferences/.GlobalPreferences.plist"

plutil -replace AppleLocale -string zh_CN \
  "$D/Library/Preferences/.GlobalPreferences.plist"

plutil -replace Country -string CN \
  "$D/Library/Preferences/.GlobalPreferences.plist"
```

再修改 root 的全局偏好作为兜底：

```bash
R="$D/private/var/root/Library/Preferences/.GlobalPreferences.plist"
cp -p "$R" "$R.before-zh"

/usr/libexec/PlistBuddy -c "Delete :AppleLanguages" "$R" >/dev/null 2>&1
/usr/libexec/PlistBuddy -c "Add :AppleLanguages array" "$R"
/usr/libexec/PlistBuddy -c "Add :AppleLanguages:0 string zh-Hans-CN" "$R"
/usr/libexec/PlistBuddy -c "Add :AppleLanguages:1 string en-US" "$R"

/usr/libexec/PlistBuddy -c "Delete :AppleLocale" "$R" >/dev/null 2>&1
/usr/libexec/PlistBuddy -c "Add :AppleLocale string zh_CN" "$R"

/usr/libexec/PlistBuddy -c "Delete :Country" "$R" >/dev/null 2>&1
/usr/libexec/PlistBuddy -c "Add :Country string CN" "$R"
```

在 Recovery 中关机：

```bash
shutdown -h now
```

虚拟机完全停止后恢复 VMX：

1. 把 `sata0:1.present` 改回 `TRUE`；
2. 保留 `sata0:1.fileName` 当前使用的差分盘名；
3. 删除全部临时 `nvme0...` 行；
4. 不要用早期 VMX 备份覆盖当前文件。

重启后，首次设置界面应显示简体中文。按向导选择国家或地区、键盘和网络，然后创建本地账户。

## 10. 验证结果并创建快照

完成后检查：

- 虚拟机可以从系统盘正常启动；
- 鼠标和键盘可以正常操作；
- 系统显示为 macOS Sequoia / Darwin 24；
- NAT 网络可用；
- 已完成首次设置并进入桌面；
- 宿主代理已恢复到原来的模式。

创建最终快照：

```powershell
& $vmrun snapshot $vmx 'sequoia-ready'
```

日常操作：

```powershell
# GUI 启动
& $vmrun start $vmx gui

# 后台启动
& $vmrun start $vmx nogui

# 正常关机
& $vmrun stop $vmx soft

# 查看快照
& $vmrun listSnapshots $vmx
```

不要在 macOS 正在安装或更新时强制结束 `vmware-vmx.exe`，否则可能损坏 APFS 或快照链。

更多虚拟机系统部署方案请返回[虚拟机系统部署指南](/p/virtual-machine-system-setup-guide/)。
