---
title: "在 VMware Workstation Pro 中部署 SteamOS 测试虚拟机"
date: 2026-09-17
description: "记录使用 Steam Deck Recovery 镜像在 VMware Workstation Pro 中安装 SteamOS，并通过 EFI framebuffer 和 Plasma X11 解决启动黑屏问题的完整过程。"
categories:
  - "系统"
tags:
  - "SteamOS"
  - "VMware Workstation"
  - "虚拟机"
  - "Steam Deck"
  - "Arch Linux"
  - "系统安装"
draft: false
slug: "steamos-vmware-setup"
related_group: "virtual-machine-system-setup"
hidden: true
searchable: true
guide: "/p/virtual-machine-system-setup-guide/"
guide_title: "虚拟机系统部署指南"
---

这次继续使用 Steam Deck Recovery 镜像，把 SteamOS 安装到 VMware Workstation Pro 虚拟机中。

最后的结果是：SteamOS 3.8.14 可以完成安装，也可以正常启动和重启，但 SteamOS 默认的 Gaming Mode 不能在 VMware 虚拟显卡上运行。安装后的黑屏并不是写盘失败，而是当前 Valve Neptune 内核没有提供 `vmwgfx` 驱动，导致 VMware SVGA II 无法建立 DRM 图形设备。

最终使用 EFI framebuffer、`xf86-video-fbdev`、Xorg 和 Plasma X11 绕过了这个限制，并通过两个 systemd 服务实现开机自动进入桌面。

## 一、安装结果与兼容性结论

本次实际使用的环境如下：

```text
VMware Workstation Pro 17.6.4
SteamOS 3.8.14
BUILD_ID=20260707.10
Kernel=6.16.12-valve24.4-1-neptune-616-gfe145653a794
```

最终结果：

- SteamOS 已经成功写入 128 GiB VMware 虚拟磁盘。
- UEFI 启动、A/B 系统分区、`/var` 和 `/home` 均正常。
- 首次启动后，`/home` 自动扩容到约 117 GiB。
- SSH 可以正常连接，并已设置为开机自动启动。
- Plasma X11 可以正常显示，并能在重启后自动进入桌面。
- OpenGL 使用 `llvmpipe` 软件渲染。
- Gaming Mode 和 Gamescope 不可用。
- 当前方案适合系统功能测试，不适合测试真实游戏性能。

## 二、准备 VMware 和 SteamOS Recovery 镜像

本次使用的 Recovery 压缩包为：

```text
D:\vmware\steamos\steamdeck-oobe-repair-20260707.10-3.8.14.img.zip
```

解压后的 IMG 为：

```text
D:\vmware\steamos\recovery\steamdeck-oobe-repair-20260707.10-3.8.14.img
```

VMware 虚拟机工作目录为：

```text
D:\vmware\steamos\workstation
```

开始前安装以下软件：

- VMware Workstation Pro 17.6.4
- 7-Zip
- Oracle VirtualBox，这里只使用它附带的 `VBoxManage.exe` 转换磁盘格式

> VMware 自己的 `vmware-vdiskmanager.exe` 可以创建 VMDK，但不能直接把这份 raw IMG 按本次需要转换为可挂载的 Recovery VMDK，所以这里仍然借用了 `VBoxManage convertfromraw`。

## 三、校验并解压 Recovery 镜像

先在 PowerShell 中检查下载的 ZIP 是否损坏：

```powershell
& 'C:\Program Files\7-Zip\7z.exe' t `
  'D:\vmware\steamos\steamdeck-oobe-repair-20260707.10-3.8.14.img.zip'
```

输出下面这行表示压缩包校验正常：

```text
Everything is Ok
```

然后解压 Recovery 镜像：

```powershell
$zip = 'D:\vmware\steamos\steamdeck-oobe-repair-20260707.10-3.8.14.img.zip'
$out = 'D:\vmware\steamos\recovery'

New-Item -ItemType Directory -Force -Path $out | Out-Null

& 'C:\Program Files\7-Zip\7z.exe' x `
  $zip `
  "-o$out"
```

## 四、转换 Recovery 磁盘并创建目标盘

先把 raw IMG 转换成 VMware 可以挂载的 VMDK：

```powershell
$vb = 'C:\Program Files\Oracle\VirtualBox\VBoxManage.exe'
$img = 'D:\vmware\steamos\recovery\steamdeck-oobe-repair-20260707.10-3.8.14.img'
$vmdk = 'D:\vmware\steamos\steamos-install.vmdk'

& $vb convertfromraw `
  $img `
  $vmdk `
  --format VMDK
```

检查文件是否已经生成：

```powershell
Get-Item 'D:\vmware\steamos\steamos-install.vmdk' |
  Select-Object FullName, Length
```

接下来使用 VMware 自带的工具创建一个 128 GiB 目标盘：

```powershell
$vdisk = 'C:\Program Files (x86)\VMware\VMware Workstation\vmware-vdiskmanager.exe'
$systemDisk = 'D:\vmware\steamos\steamos-disk-128.vmdk'

& $vdisk -c `
  -s 128GB `
  -a lsilogic `
  -t 0 `
  $systemDisk
```

检查两个 VMDK：

```powershell
Get-ChildItem 'D:\vmware\steamos' -Filter '*.vmdk' |
  Select-Object Name, Length
```

后面为了便于管理，我把两块磁盘整理到 `workstation` 目录，并使用了下面的名称：

```text
steamos-recovery.vmdk
steamos-target-128gb.vmdk
```

## 五、创建 VMware 虚拟机

在 VMware Workstation Pro 中新建自定义虚拟机，选择稍后安装操作系统，并按下面的参数配置：

```text
客户机系统：Other Linux 6.x kernel 64-bit
固件：UEFI
Secure Boot：关闭
处理器：4 vCPU
内存：8 GB
网络：NAT
网卡型号：e1000e
显存：256 MB
3D 加速：开启
声音：关闭
```

虚拟机文件为：

```text
D:\vmware\steamos\workstation\SteamOS-VMware.vmx
```

关闭 VMware Workstation 后，可以检查 VMX 中的关键配置：

```ini
guestOS = "other6xlinux-64"
firmware = "efi"
uefi.secureBoot.enabled = "FALSE"
numvcpus = "4"
memsize = "8192"
nvme0.present = "TRUE"
ethernet0.connectionType = "nat"
ethernet0.virtualDev = "e1000e"
mks.enable3d = "TRUE"
svga.graphicsMemoryKB = "262144"
sound.present = "FALSE"
```

安装阶段把 Recovery 盘和 128 GiB 目标盘都接到 VMware NVMe 控制器：

```ini
nvme0.present = "TRUE"

nvme0:0.present = "TRUE"
nvme0:0.fileName = "steamos-recovery.vmdk"

nvme0:1.present = "TRUE"
nvme0:1.fileName = "steamos-target-128gb.vmdk"
```

> 编辑 VMX 前必须完全关闭虚拟机和 VMware Workstation，不能在虚拟机挂起时直接修改。磁盘路径、控制器编号和当前快照链也要以自己的 VMX 为准。

## 六、从 Recovery 环境启动

启动虚拟机后进入 SteamOS Recovery 桌面。先在终端中查看磁盘：

```bash
lsblk -o NAME,SIZE,MODEL,FSTYPE,LABEL,PARTLABEL,MOUNTPOINTS
```

本次环境中，128 GiB 目标盘识别为：

```text
/dev/nvme0n2
Disk model: VMware Virtual NVMe Disk
Disk size: 128 GiB
```

设备名不是固定值。执行任何清盘命令前，必须同时根据容量、型号和现有分区确认目标盘，不能直接照抄 `/dev/nvme0n2`。

## 七、设置 deck 密码并启用 SSH

为了方便复制命令和查看日志，先在 Recovery 环境中给 `deck` 用户设置密码：

```bash
passwd
```

本次临时测试密码使用了：

```text
123456
```

这只是隔离测试环境中的临时密码。正式使用时必须改成强密码，不能继续使用这个值。

启动 SSH：

```bash
sudo systemctl enable --now sshd
```

查看虚拟机地址：

```bash
ip -br addr
```

本次 VMware NAT 分配的地址是：

```text
192.168.233.130
```

在 Windows 宿主机中连接：

```powershell
ssh deck@192.168.233.130
```

VMware NAT 地址可能在重启后变化，应以虚拟机里 `ip -br addr` 的实际输出为准。

## 八、修改 Recovery 安装脚本

Steam Deck Recovery 的恢复脚本是按真实 Steam Deck NVMe 硬盘设计的。VMware 虚拟 NVMe 不支持脚本调用的 NVMe sanitize，因此原脚本会在清理磁盘阶段失败。

本次没有把整份 Recovery 脚本硬编码进文章，因为 Valve 后续镜像中的脚本内容可能变化。实际修改集中在下面三点：

1. 明确把安装目标设置为确认过的 `/dev/nvme0n2`。
2. 跳过 VMware 虚拟 NVMe 不支持的 sanitize。
3. 禁用安装完成后的自动重启，先保留 Recovery 环境检查写盘结果。

用于替代 sanitize 的清理命令为：

```bash
sudo wipefs -a /dev/nvme0n2
sudo dd if=/dev/zero of=/dev/nvme0n2 bs=1M count=64 conv=fsync
```

> 这两条命令会破坏目标盘上的分区和文件系统。必须先通过 `lsblk` 再次确认 128 GiB 目标盘，不能对 Recovery 盘或宿主机磁盘执行。

运行修改后的安装脚本时保留完整日志，便于判断脚本究竟在哪一步退出。本次日志最后出现：

```text
:: Reimaging complete; automatic reboot disabled for VMware verification.

REMOTE_EXIT=0
```

`REMOTE_EXIT=0` 表示安装脚本正常结束。

## 九、把 SteamOS 写入目标盘

脚本完成了以下工作：

- 建立 GPT 分区表。
- 创建 SteamOS A/B 启动与系统分区。
- 格式化 EFI、rootfs、var 和 home。
- 写入 rootfs-A 和 rootfs-B。
- 生成启动配置。
- 安装 GRUB 和 SteamOS EFI 启动器。
- 创建 `Boot0004 SteamOS` UEFI 启动项。

安装完成后检查分区：

```bash
lsblk -o NAME,SIZE,FSTYPE,LABEL,PARTLABEL,MOUNTPOINTS /dev/nvme0n2
sudo efibootmgr -v
```

最初生成的主要分区如下：

```text
/dev/nvme0n2p1  256 MiB  EFI
/dev/nvme0n2p2   64 MiB  EFI-A
/dev/nvme0n2p3   64 MiB  EFI-B
/dev/nvme0n2p4    5 GiB  rootfs-A
/dev/nvme0n2p5    5 GiB  rootfs-B
/dev/nvme0n2p6  256 MiB  var-A
/dev/nvme0n2p7  256 MiB  var-B
/dev/nvme0n2p8  100 MiB  home 初始分区
```

这里看到的 home 初始只有约 100 MiB，不代表 128 GiB 空间丢失。首次从目标盘启动时，SteamOS 会自动扩展最后的 home 分区，最终容量约为 117 GiB。

## 十、断开 Recovery 盘并首次启动

确认安装完成后关闭虚拟机。安装阶段的 VMX 已另外备份为：

```text
SteamOS-VMware.vmx.installed-before-disk-switch-20260917-022146.bak
```

然后断开 `steamos-recovery.vmdk`，只保留安装完成的目标盘，并把目标盘移动到 `nvme0:0`：

```ini
nvme0:0.present = "TRUE"
nvme0:0.fileName = "steamos-target-128gb.vmdk"
```

再次启动后，原来的目标盘会从 `/dev/nvme0n2` 变为 `/dev/nvme0n1`，这是因为 Recovery 盘已经移除，设备枚举顺序发生了变化。

最终实际挂载为：

```text
/dev/nvme0n1p5  rootfs-B  /
/dev/nvme0n1p7  var-B     /var
/dev/nvme0n1p8  home      /home
```

系统能够启动，SSH 也能连接，但 VMware 窗口一直是黑屏。

## 十一、定位安装后黑屏

因为 SSH 仍然正常，所以这次黑屏并不是系统没有安装成功。通过 SSH 进入系统后检查版本、磁盘、显示管理器和显卡：

```bash
cat /etc/os-release
uname -a
lsblk -o NAME,SIZE,FSTYPE,LABEL,PARTLABEL,MOUNTPOINTS
findmnt -no SOURCE,TARGET / /var /home
systemctl status sddm --no-pager -l
lspci -nnk | grep -A4 -Ei 'VGA|Display|3D'
ls -la /dev/dri /dev/fb0
sudo journalctl -b -p warning..alert --no-pager -n 250
```

检查结果说明：

- SteamOS 3.8.14 已经安装并正常挂载系统分区。
- VMware SVGA II 能被 PCI 总线识别。
- 显卡条目没有 `Kernel driver in use`。
- 系统中不存在可用的 `/dev/dri` DRM 设备。
- EFI framebuffer `/dev/fb0` 仍然存在。
- SDDM 停在 `Logind interface found` 附近，无法建立可用的图形 seat。

所以问题已经从“SteamOS 是否安装成功”缩小为“Valve 内核无法驱动 VMware 虚拟显卡”。

## 十二、确认 vmwgfx 缺失

继续检查 `vmwgfx`：

```bash
sudo modprobe vmwgfx
find /lib/modules/"$(uname -r)" -type f -iname '*vmwgfx*'
```

实际结果包含：

```text
modprobe: FATAL: Module vmwgfx not found
```

也就是说，当前 `6.16.12-valve24.4-1-neptune-616-gfe145653a794` 内核没有可用的 `vmwgfx` 模块，`CONFIG_DRM_VMWGFX` 没有启用。

这会造成下面的连锁问题：

```text
VMware SVGA II
        ↓
没有 vmwgfx
        ↓
没有 /dev/dri
        ↓
SDDM 无法获得 DRM 图形 seat
        ↓
Gaming Mode 和普通 SDDM 会话都无法正常显示
```

VirtualBox 那次只需要把默认会话切换到 Plasma X11；VMware 这里更麻烦，因为即使选择 Plasma X11，SDDM 仍然会因缺少 DRM seat 而卡住。因此最终不能继续依赖 SDDM，而是直接启动 Xorg。

## 十三、安装 framebuffer Xorg 驱动

SteamOS 默认把系统分区设为只读。先临时关闭只读保护，初始化软件包密钥并安装 framebuffer 驱动：

```bash
sudo steamos-readonly disable
sudo pacman-key --init
sudo pacman-key --populate archlinux holo
sudo pacman -S xf86-video-fbdev xf86-video-vesa
sudo steamos-readonly enable
```

安装完成后检查：

```bash
pacman -Q xf86-video-fbdev xf86-video-vesa
ls -l /dev/fb0
```

SteamOS 系统更新可能替换 `/usr`，从而覆盖手动安装的软件包。如果以后更新后桌面再次失效，先检查：

```bash
pacman -Q xf86-video-fbdev
```

## 十四、配置 Xorg 使用 /dev/fb0

创建 Xorg 配置文件：

```bash
sudo mkdir -p /etc/X11/xorg.conf.d

cat <<'EOF' | sudo tee /etc/X11/xorg.conf.d/20-vmware-fbdev.conf
Section "Device"
    Identifier "VMware EFI Framebuffer"
    Driver "fbdev"
    Option "fbdev" "/dev/fb0"
    Option "ShadowFB" "true"
EndSection

Section "Screen"
    Identifier "VMware Screen"
    Device "VMware EFI Framebuffer"
    DefaultDepth 24
EndSection
EOF
```

当前显示链路变为：

```text
EFI framebuffer /dev/fb0
        ↓
xf86-video-fbdev
        ↓
Xorg
        ↓
Plasma X11
        ↓
llvmpipe 软件 OpenGL
```

## 十五、为什么不能继续使用 SDDM

SteamOS 默认 SDDM 配置会强制使用 Wayland：

```ini
DisplayServer=wayland
```

Steam Deck 专用配置还会调用：

```text
/usr/lib/steamos/steamos-rotate-x11-screen
```

排障过程中曾尝试增加 `/etc/sddm.conf.d/zzz-vmware.conf`，把会话切换到 X11，但 SDDM 仍然无法在没有 DRM seat 的环境中正常拉起 Xorg。

因此最后停用 SDDM：

```bash
sudo systemctl mask sddm.service
```

这不是因为 Plasma X11 本身不能运行，而是当前 SDDM 启动路径要求的图形设备条件无法满足。后面改用 systemd 分别启动 Xorg 和 Plasma。

## 十六、创建 Xorg 和 Plasma systemd 服务

先创建 Xorg 服务：

```bash
cat <<'EOF' | sudo tee /etc/systemd/system/steamos-vmware-xorg.service
[Unit]
Description=SteamOS VMware framebuffer Xorg
After=systemd-user-sessions.service plymouth-quit.service
Conflicts=display-manager.service

[Service]
Type=simple
ExecStart=/usr/lib/Xorg :0 -ac -noreset -nolisten tcp
Restart=always
RestartSec=2

[Install]
WantedBy=graphical.target
EOF
```

再创建 Plasma X11 服务：

```bash
cat <<'EOF' | sudo tee /etc/systemd/system/steamos-vmware-plasma.service
[Unit]
Description=SteamOS VMware Plasma X11 desktop
Requires=steamos-vmware-xorg.service user@1000.service
After=steamos-vmware-xorg.service user@1000.service

[Service]
Type=simple
User=deck
Group=deck
WorkingDirectory=/home/deck
Environment=HOME=/home/deck
Environment=USER=deck
Environment=LOGNAME=deck
Environment=DISPLAY=:0
Environment=XDG_RUNTIME_DIR=/run/user/1000
Environment=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus
Environment=XDG_SESSION_TYPE=x11
Environment=QT_QPA_PLATFORM=xcb
Environment=LIBGL_ALWAYS_SOFTWARE=1
Environment=KWIN_COMPOSE=N
ExecStartPre=/usr/bin/sleep 3
ExecStart=/usr/bin/startplasma-x11
Restart=on-failure
RestartSec=3

[Install]
WantedBy=graphical.target
EOF
```

启用用户 linger、两个桌面服务和 SSH：

```bash
sudo systemctl daemon-reload
sudo loginctl enable-linger deck
sudo systemctl enable steamos-vmware-xorg.service
sudo systemctl enable steamos-vmware-plasma.service
sudo systemctl enable sshd.service
sudo systemctl mask sddm.service
sudo reboot
```

`Xorg :0 -ac` 会关闭 X Server 的客户端访问控制，因此这个方案只适合隔离的测试虚拟机，不应该直接暴露到不可信网络。这里同时使用 `-nolisten tcp`，避免 Xorg 监听 TCP 端口。

## 十七、重启并验证持久化

重启后检查服务状态：

```bash
systemctl is-active sshd steamos-vmware-xorg steamos-vmware-plasma
systemctl is-enabled sshd steamos-vmware-xorg steamos-vmware-plasma
```

本次实际结果均为：

```text
active
enabled
```

检查桌面进程：

```bash
pgrep -a Xorg
pgrep -a kwin_x11
pgrep -a plasmashell
```

实际可以看到：

```text
/usr/lib/Xorg :0 -ac -noreset -nolisten tcp
/usr/bin/kwin_x11 --replace
/usr/bin/plasmashell --no-respawn
```

检查 OpenGL：

```bash
glxinfo -B | grep -E 'direct rendering|OpenGL renderer|OpenGL core profile version'
```

本次输出为：

```text
direct rendering: Yes
OpenGL renderer string: llvmpipe (LLVM 20.1.8, 256 bits)
OpenGL core profile version string: 4.5 (Core Profile) Mesa 25.3.0
```

桌面位于 VT2。如果排障时切换到了其他 TTY，可以使用下面的组合键返回桌面：

```text
Ctrl+Alt+F2
```

当前 framebuffer 桌面分辨率为：

```text
1024x768
```

## 十八、关闭临时 VNC 并创建快照

排障完成后确认 VMX 中的临时 VNC 已关闭：

```ini
RemoteDisplay.vnc.enabled = "FALSE"
```

然后在 Windows PowerShell 中创建安装完成快照并启动虚拟机：

```powershell
$vmrun = 'C:\Program Files (x86)\VMware\VMware Workstation\vmrun.exe'
$vmx = 'D:\vmware\steamos\workstation\SteamOS-VMware.vmx'

& $vmrun snapshot $vmx 'steamos-installed-plasma-x11'
& $vmrun start $vmx gui
```

创建快照后，VMX 当前引用的是快照增量盘：

```text
steamos-target-128gb-000001.vmdk
```

所以后续不要在 VMware 外部直接替换或移动基础 VMDK，也不要手工破坏快照链。

## 十九、最终结果与已知限制

这次 VMware Workstation Pro 中的 SteamOS 安装最终成功。最关键的判断是：安装后黑屏不等于安装失败。只要 SSH、分区挂载和 systemd 仍然正常，就应该继续检查显卡内核驱动、DRM 设备、显示管理器和桌面会话。

本次黑屏的实际根因是：

```text
Valve Neptune 内核没有 vmwgfx
        ↓
VMware SVGA II 没有 DRM 设备
        ↓
SDDM 和 Gamescope 无法建立正常图形会话
        ↓
虚拟机窗口保持黑屏
```

最终解决方法是：

```text
保留 EFI framebuffer
        ↓
安装 xf86-video-fbdev
        ↓
让 Xorg 直接使用 /dev/fb0
        ↓
绕过 SDDM
        ↓
通过 systemd 启动 Plasma X11
        ↓
使用 llvmpipe 完成软件渲染
```

最终可用边界：

- 可以进入 Plasma X11 桌面。
- 可以进行基础系统配置和功能验证。
- 可以使用 SSH 远程维护。
- 不能使用 SteamOS Gaming Mode。
- 不具备 VMware 虚拟显卡硬件加速。
- 不能用来代表 Steam Deck 或真实 Linux 游戏主机的性能。
- SteamOS 更新后，可能需要重新安装 `xf86-video-fbdev` 并检查自定义服务。

因此，这套虚拟机适合研究 SteamOS 的系统结构、A/B 分区、桌面环境和基础软件行为；如果目标是运行 Gamescope、验证 Vulkan 或测试游戏性能，仍然需要受支持的 AMD GPU、PCIe 显卡直通或真实 Steam Deck 环境。