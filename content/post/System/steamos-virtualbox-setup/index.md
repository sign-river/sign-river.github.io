---
title: "在 VirtualBox 中部署 SteamOS 测试虚拟机"
date: 2026-08-16
description: "把 Valve Steam Deck Recovery 镜像转换为 VirtualBox 虚拟机，并完成可用分辨率、正常关机和 Steam 启动配置。"
categories:
  - "系统"
tags:
  - "SteamOS"
  - "VirtualBox"
  - "虚拟机"
  - "Steam Deck"
  - "Arch Linux"
  - "系统安装"
draft: true
slug: "steamos-virtualbox-setup"
---

本文只保留已经跑通的一条路线：下载 Valve Steam Deck Recovery/OOBE 磁盘镜像，将它转换成 VirtualBox 系统盘，再通过 Arch LTS 内核解决 VMSVGA 分辨率问题。最终得到的是一台适合功能验证的 SteamOS 测试机，而不是传统 ISO 安装出的通用 PC SteamOS。

> 这套方案使用 Steam Deck 恢复镜像，并对系统内核和 GRUB 做测试环境改造。它不属于 Valve 官方支持的通用 PC 安装方式，也不代表真实 Steam Deck 或 Linux 游戏主机的图形性能。

## 1. 准备环境

本次验证使用：

| 资源 | 版本或文件 | 用途 |
| --- | --- | --- |
| VirtualBox | 7.2.14 | 创建和运行虚拟机 |
| Steam Deck Recovery | `steamdeck-oobe-repair-20260707.10-3.8.14.img.bz2` | SteamOS 恢复系统盘 |
| Python 3 | Windows 版本 | 使用标准库 `bz2` 解压镜像 |
| Windows OpenSSH Client | Windows 可选功能 | 从宿主通过 SSH 管理来宾 |

下载入口：

- [VirtualBox 7.2.14 Windows 安装包](https://download.virtualbox.org/virtualbox/7.2.14/VirtualBox-7.2.14-174565-Win.exe)
- [Valve Steam Deck Recovery 说明](https://help.steampowered.com/en/faqs/view/1B71-EDF2-EB6D-2BB3)
- [Valve 恢复镜像索引](https://steamdeck-images.steamos.cloud/recovery/)
- [本次使用的固定恢复镜像](https://steamdeck-images.steamos.cloud/recovery/steamdeck-oobe-repair-20260707.10-3.8.14.img.bz2)
- [Python for Windows](https://www.python.org/downloads/windows/)
- [Windows OpenSSH Client 说明](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse)

宿主至少要为压缩镜像、解压后的 IMG、两块 VDI 和后续快照预留足够空间。数据盘逻辑容量为 128 GiB，但使用动态分配，不会立刻占满宿主磁盘。

## 2. 下载并核对恢复镜像

在 PowerShell 中执行：

```powershell
$dir = 'D:\Downloads\SignRiver-Test-OS\steamos'
New-Item -ItemType Directory -Force $dir | Out-Null

curl.exe -fL --retry 3 `
  -o "$dir\steamdeck-oobe-repair-20260707.10-3.8.14.img.bz2" `
  'https://steamdeck-images.steamos.cloud/recovery/steamdeck-oobe-repair-20260707.10-3.8.14.img.bz2'

Get-FileHash -Algorithm SHA256 `
  "$dir\steamdeck-oobe-repair-20260707.10-3.8.14.img.bz2"
```

本次验证文件为：

```text
大小：3357999306 bytes
SHA256：4254ee02ec34ae8add9aceef1881a2ce675a9d0176171df92e0eaa1bf014c594
```

本文固定使用 `20260707.10-3.8.14`。不要在复现时未经验证就换成索引中的其他镜像。

## 3. 解压镜像并创建虚拟磁盘

使用 Python 标准库解压 `.bz2`。把下面代码保存为 `D:\Downloads\SignRiver-Test-OS\steamos\extract-image.py`：

```python
import bz2
import shutil

src = r"D:\Downloads\SignRiver-Test-OS\steamos\steamdeck-oobe-repair-20260707.10-3.8.14.img.bz2"
dst = r"D:\Downloads\SignRiver-Test-OS\steamos\steamdeck-oobe-repair-20260707.10-3.8.14.img"

with bz2.open(src, "rb") as fin, open(dst, "wb") as fout:
    shutil.copyfileobj(fin, fout, length=4 * 1024 * 1024)
```

运行脚本：

```powershell
python 'D:\Downloads\SignRiver-Test-OS\steamos\extract-image.py'
```

然后把 raw IMG 转成 VDI，并创建一块 128 GiB 动态数据盘：

```powershell
$VBoxManage = 'C:\Program Files\Oracle\VirtualBox\VBoxManage.exe'
$dir = 'D:\Downloads\SignRiver-Test-OS\steamos'

New-Item -ItemType Directory -Force "$dir\vm" | Out-Null

& $VBoxManage convertfromraw `
  "$dir\steamdeck-oobe-repair-20260707.10-3.8.14.img" `
  "$dir\vm\steamos-install.vdi" `
  --format VDI

if ($LASTEXITCODE -ne 0) { throw '恢复盘转换失败' }

& $VBoxManage createmedium disk `
  --filename "$dir\vm\steamos-disk.vdi" `
  --size 131072 `
  --format VDI

if ($LASTEXITCODE -ne 0) { throw '数据盘创建失败' }
```

## 4. 创建 VirtualBox 虚拟机

以 PowerShell 执行：

```powershell
$VBoxManage = 'C:\Program Files\Oracle\VirtualBox\VBoxManage.exe'
$dir = 'D:\Downloads\SignRiver-Test-OS\steamos'

& $VBoxManage createvm --name SteamOS --ostype ArchLinux_64 --register

& $VBoxManage modifyvm SteamOS `
  --memory 8192 `
  --cpus 2 `
  --vram 256 `
  --graphicscontroller vmsvga `
  --accelerate-3d on `
  --firmware efi `
  --nic1 nat `
  --nictype1 82540EM `
  --ioapic on `
  --audio-enabled off `
  --usb off `
  --clipboard-mode bidirectional `
  --drag-and-drop bidirectional
```

创建 SATA 控制器并挂载恢复盘和数据盘：

```powershell
& $VBoxManage storagectl SteamOS `
  --name SATA `
  --add sata `
  --controller IntelAhci `
  --portcount 2

& $VBoxManage storageattach SteamOS `
  --storagectl SATA `
  --port 0 `
  --device 0 `
  --type hdd `
  --medium "$dir\vm\steamos-install.vdi"

& $VBoxManage storageattach SteamOS `
  --storagectl SATA `
  --port 1 `
  --device 0 `
  --type hdd `
  --medium "$dir\vm\steamos-disk.vdi"
```

设置 SSH 端口转发：

```powershell
& $VBoxManage modifyvm SteamOS `
  --natpf1 "ssh,tcp,127.0.0.1,2222,,22"
```

SSH 只绑定到宿主回环地址，不会直接暴露到局域网。

## 5. 首次启动并通过 SSH 接管

启动虚拟机：

```powershell
& $VBoxManage startvm SteamOS --type gui
```

恢复镜像启动的是精简 OOBE/X 会话，而不是完整 KDE Plasma 桌面，因此没有开始菜单、`Super` 菜单或 `Ctrl+Alt+T` 终端属于正常现象。

恢复镜像测试阶段使用 `deck` 用户。按界面完成必要的初始操作后，从宿主连接：

```powershell
ssh -p 2222 deck@127.0.0.1
```

连接成功后立即为账户设置自己的密码，并优先配置 SSH 公钥。本文不记录任何默认密码或私钥。

## 6. 安装 Arch LTS 内核解决分辨率问题

原恢复内核在 VMSVGA 下可能只提供约 640×480。已经验证可用的解决方式是保留原内核，再增加 Arch LTS 内核，让 `vmwgfx` 正常加载。

先在宿主创建快照：

```powershell
$VBoxManage = 'C:\Program Files\Oracle\VirtualBox\VBoxManage.exe'
& $VBoxManage snapshot SteamOS take 'before-arch-lts-vmsvga' `
  --description 'Before installing Arch LTS kernel for VMSVGA support'
```

在来宾中解除只读，并使用本次固定恢复镜像已经验证通过的命令安装 LTS 内核：

```bash
sudo steamos-readonly disable 2>/dev/null || true
sudo pacman -S --noconfirm --needed \
  --assume-installed=initramfs \
  linux-lts
```

本次验证安装的是 `linux-lts 6.18.44-1`。

> `--assume-installed=initramfs` 是针对本文固定恢复镜像仓库状态的兼容参数。执行前确认系统已有 initramfs 工具链和正常的 `/boot` 内容，不要在其他 Linux 系统上照抄。

备份并重新生成 EFI GRUB 配置：

```bash
sudo cp /efi/EFI/steamos/grub.cfg \
  /home/deck/grub.cfg.before-lts

sudo grub-mkconfig -o /efi/EFI/steamos/grub.cfg
sudo grep -E '^menuentry |^submenu ' /efi/EFI/steamos/grub.cfg
find /usr/lib/modules -name 'vmwgfx.ko*' -print
```

从输出中找到 `linux-lts` 对应的完整 GRUB 条目。它的 UUID 会因虚拟磁盘而变化，不能照抄别人的值。本次验证中的条目形式如下：

```text
gnulinux-advanced-<你的 UUID>>gnulinux-linux-lts-advanced-<你的 UUID>
```

先只让下一次启动进入 LTS：

```bash
entry='把这里替换为上一条命令找到的完整 linux-lts 条目'
sudo grub-editenv /efi/EFI/steamos/grubenv set next_entry="$entry"
sudo grub-editenv /efi/EFI/steamos/grubenv list
sudo systemctl poweroff
```

虚拟机关闭后，在宿主再次固定显示配置并启动：

```powershell
& $VBoxManage modifyvm SteamOS `
  --graphicscontroller vmsvga `
  --accelerate-3d on `
  --vram 256

& $VBoxManage startvm SteamOS --type gui
```

重新 SSH 登录并验证：

```bash
uname -r
lspci -nnk | sed -n '/VGA compatible controller/,+5p'
lsmod | grep vmwgfx
DISPLAY=:0 XAUTHORITY=/home/deck/.Xauthority xrandr --current
```

确认 `uname -r` 显示 LTS 内核、`vmwgfx` 已加载，并且 `xrandr` 出现可用分辨率后，再把 LTS 固定为默认启动项。

本次成功路线是备份 `/efi/EFI/steamos/grub.cfg`，然后把文件开头的：

```text
set default="0"
```

改为：

```text
set default="gnulinux-advanced-<你的 UUID>>gnulinux-linux-lts-advanced-<你的 UUID>"
```

修改后重启一次，再执行 `uname -r` 确认仍进入 LTS 内核。

> `grub.cfg` 是生成文件，再次运行 `grub-mkconfig` 会覆盖这个修改。原 `linux-neptune-616` 内核仍保留在 GRUB 高级启动项中，LTS 无法启动时可回退。

## 7. 修复 ACPI 电源按钮

如果宿主发送 ACPI 电源按钮后虚拟机不关机，在来宾中创建配置：

```bash
cat > /home/deck/zz-signriver-poweroff.conf <<'EOF'
[Login]
HandlePowerKey=poweroff
PowerKeyIgnoreInhibited=no
EOF

sudo install -m 644 \
  /home/deck/zz-signriver-poweroff.conf \
  /etc/systemd/logind.conf.d/zz-signriver-poweroff.conf

sudo systemctl restart systemd-logind
systemd-analyze cat-config systemd/logind.conf
```

在宿主测试正常关机：

```powershell
& $VBoxManage controlvm SteamOS acpipowerbutton
```

虚拟机应执行正常关机，而不是保持无响应。

## 8. 正确启动 Steam

重新启动虚拟机后，不要调用 `/usr/bin/steam`。该恢复镜像中的这个入口会进入 OOBE 包装流程，并可能清理 Steam 配置。直接启动实际客户端：

```bash
/usr/lib/steam/steam
```

如果需要从 SSH 中启动 Steam，必须同时提供用户会话环境：

```bash
sudo systemd-run \
  --unit=signriver-steam \
  --property=Restart=no \
  --uid=deck \
  --working-directory=/home/deck \
  --setenv=HOME=/home/deck \
  --setenv=DISPLAY=:0 \
  --setenv=XDG_RUNTIME_DIR=/run/user/1000 \
  --setenv=DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus \
  --setenv=XAUTHORITY=/home/deck/.Xauthority \
  /usr/lib/steam/steam -skipinitialbootstrap
```

Steam 首次启动后会自行下载客户端更新。等待更新完成并登录自己的 Steam 账户。

## 9. 验证并创建快照

确认以下项目：

- SteamOS 能从恢复系统盘稳定启动；
- `uname -r` 显示 LTS 内核；
- `vmwgfx` 已加载；
- `xrandr` 能看到高于 640×480 的可用分辨率；
- 宿主能通过 `127.0.0.1:2222` SSH 连接；
- ACPI 电源按钮可以正常关机；
- `/usr/lib/steam/steam` 可以启动并保留登录状态。

关机后创建最终快照：

```powershell
$VBoxManage = 'C:\Program Files\Oracle\VirtualBox\VBoxManage.exe'
& $VBoxManage snapshot SteamOS take 'steamos-ready' `
  --description 'SteamOS recovery image with LTS kernel, VMSVGA, SSH and Steam validated'
```

日常命令：

```powershell
$VBoxManage = 'C:\Program Files\Oracle\VirtualBox\VBoxManage.exe'

# GUI 启动
& $VBoxManage startvm SteamOS --type gui

# 无界面启动
& $VBoxManage startvm SteamOS --type headless

# 请求正常关机
& $VBoxManage controlvm SteamOS acpipowerbutton

# 查看配置与状态
& $VBoxManage showvminfo SteamOS --machinereadable

# 查看快照
& $VBoxManage snapshot SteamOS list --machinereadable
```

恢复快照会丢弃该快照之后的磁盘状态。恢复前先导出需要保留的项目文件、游戏存档和测试证据。

同属“虚拟机”主题的另一篇文章：[在 Windows 的 VMware 中安装 macOS Sequoia](/p/macos-sequoia-vmware-setup/)。

