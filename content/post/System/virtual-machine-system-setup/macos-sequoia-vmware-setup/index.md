---
title: "在 Windows 的 VMware 中安装 macOS Sequoia"
date: 2026-08-29
description: "重新整理在 Windows 的 VMware 中部署 macOS Sequoia 虚拟机的步骤、配置与验证方法。"
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
related_group: "virtual-machine-system-setup"
hidden: true
searchable: true
guide: "/p/virtual-machine-system-setup-guide/"
guide_title: "虚拟机系统部署指南"
slug: "macos-sequoia-vmware-setup"
---

本文记录一套我实际验证过的流程：在 Windows 11 上使用 VMware Workstation Pro 17.6.4，创建 macOS Sequoia 虚拟机，并通过 Apple Recovery 在线安装系统。本文中的图片均来自这次实际操作。

> 注意：macOS 在非 Apple 品牌硬件上的虚拟化不属于 Apple 官方支持场景。Unlocker 是第三方补丁，使用前请确认授权、法律和安全风险。不要把它用于生产环境，也不要下载来源不明的“现成 ISO/VMDK”。

## 一、准备软件与目录

建议准备以下版本：VMware Workstation Pro 17.6.4、Unlocker 4.2.8、OpenCorePkg 1.0.7、Python 3.13.x、dmg2img 1.6.7、VirtualBox 7.2.x，以及 7-Zip。

虚拟机文件统一放在空间充足的磁盘，例如：

```text
D:\vmware\macos-vm
```

下文命令都以这个目录为例；如果你使用其他路径，请同步修改命令中的路径。

## 二、下载并安装 VMware Workstation Pro

可以从 Broadcom Support Portal 下载，也可以使用我保存的 17.6.4 安装包：
https://github.com/sign-river/File_warehouse/releases/download/VMware/VMware-workstation-full-17.6.4-24832109.exe

打开 [Broadcom 支持门户](https://support.broadcom.com/) 并注册账号。

<a href="images/2026-08-30-16-32-03.png" target="_blank"> <img src="images/2026-08-30-16-32-03.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

返回主页并登录刚注册的账号。

<a href="images/2026-08-30-16-34-53.png" target="_blank"> <img src="images/2026-08-30-16-34-53.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

进入 VMware Workstation Pro 产品下载页，选择 **17.6.4 for Windows**，接受条款后开始下载。

<a href="images/2026-08-30-16-40-31.png" target="_blank"> <img src="images/2026-08-30-16-40-31.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

返回下载页面，勾选同意相关条款。

<a href="images/2026-08-30-16-42-26.png" target="_blank"> <img src="images/2026-08-30-16-42-26.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

然后下载

<a href="images/2026-08-30-16-42-56.png" target="_blank"> <img src="images/2026-08-30-16-42-56.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

首次下载可能需要填写贸易合规信息。公司字段可以按页面要求填写；个人使用时不要虚构公司信息。确认出口合规声明后提交。

<a href="images/2026-08-30-16-48-14.png" target="_blank"> <img src="images/2026-08-30-16-48-14.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

提交后返回下载页面，再次点击对应的下载按钮。

<a href="images/2026-08-30-16-49-09.png" target="_blank"> <img src="images/2026-08-30-16-49-09.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

双击下载的 `.exe` 安装包。安装位置保持默认即可；安装向导中的选项一般保持默认，一直安装到完成。首次启动 VMware 后退出，方便后续运行 Unlocker。

<a href="images/2026-08-30-16-59-44.png" target="_blank"> <img src="images/2026-08-30-16-59-44.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 三、应用 Unlocker 补丁

打开 https://github.com/DrDonk/unlocker/releases/tag/v4.2.8，下载 zip 包

<a href="images/2026-08-30-17-01-42.png" target="_blank"> <img src="images/2026-08-30-17-01-42.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

下载完成后，将 ZIP 解压到全英文路径，例如 `D:\tools\unlocker428`。

<a href="images/2026-08-30-17-10-47.png" target="_blank"> <img src="images/2026-08-30-17-10-47.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

如果 VMware 正在运行，请完全退出，并确认任务管理器中没有 `vmware.exe` 或 `vmware-vmx.exe`。进入解压目录的 `windows` 文件夹，右键 **“以管理员身份运行”** `unlock.exe`。

<a href="images/2026-08-30-17-13-13.png" target="_blank"> <img src="images/2026-08-30-17-13-13.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

补丁运行结束后，在同一目录以管理员身份运行 `check.exe` 检查状态。

<a href="images/2026-08-30-17-13-54.png" target="_blank"> <img src="images/2026-08-30-17-13-54.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

四个项目都显示 `Patch Status: Patched (1)`，说明补丁已应用成功。若 VMware 后续升级或修复安装，需要重新检查补丁状态。

<a href="images/2026-08-30-17-15-30.png" target="_blank"> <img src="images/2026-08-30-17-15-30.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

重新打开 VMware Workstation Pro。如果弹出新版本更新提示，先选择跳过；升级可能覆盖刚应用的补丁。

<a href="images/2026-08-30-17-17-35.png" target="_blank"> <img src="images/2026-08-30-17-17-35.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 四、创建空白虚拟机

选择 **创建新的虚拟机 → 自定义（高级）**。

<a href="images/2026-08-30-17-18-07.png" target="_blank"> <img src="images/2026-08-30-17-18-07.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

保持当前已经选中的：Workstation 17.5 or later 然后点击 下一步
<a href="images/2026-08-30-17-21-07.png" target="_blank"> <img src="images/2026-08-30-17-21-07.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

选择 **稍后安装操作系统**，点击“下一步”。

<a href="images/2026-08-30-17-23-26.png" target="_blank"> <img src="images/2026-08-30-17-23-26.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

来宾操作系统选择 **Apple macOS**，版本选择 **macOS 15**，点击“下一步”。

<a href="images/2026-08-30-17-35-54.png" target="_blank"> <img src="images/2026-08-30-17-35-54.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

虚拟机名称填写 `macOS Sequoia`。位置选择预先创建的 `D:\vmware\macos-vm`，点击“下一步”。

<a href="images/2026-08-30-17-39-32.png" target="_blank"> <img src="images/2026-08-30-17-39-32.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

处理器设置为 **2 个处理器、每个处理器 2 个内核**，总计 4 个 vCPU。点击“下一步”。

<a href="images/2026-08-30-17-42-34.png" target="_blank"> <img src="images/2026-08-30-17-42-34.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

内存设置为 **8192 MB（8 GB）**。主机内存较少时可以适当降低，但不建议低于 4 GB。

<a href="images/2026-08-30-17-43-39.png" target="_blank"> <img src="images/2026-08-30-17-43-39.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

网络类型选择 **使用网络地址转换（NAT）**。

<a href="images/2026-08-30-17-45-06.png" target="_blank"> <img src="images/2026-08-30-17-45-06.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

I/O 控制器保持默认的 **LSI Logic**。

<a href="images/2026-08-30-17-46-09.png" target="_blank"> <img src="images/2026-08-30-17-46-09.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

虚拟磁盘类型选择 **SATA**。

<a href="images/2026-08-30-17-46-29.png" target="_blank"> <img src="images/2026-08-30-17-46-29.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

选择 **创建新虚拟磁盘**。

<a href="images/2026-08-30-17-47-07.png" target="_blank"> <img src="images/2026-08-30-17-47-07.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

这是向导创建的临时磁盘，后面会移除并换成手动创建的 128 GB 磁盘，因此容量保持默认即可。

<a href="images/2026-08-30-17-48-17.png" target="_blank"> <img src="images/2026-08-30-17-48-17.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

选择将虚拟磁盘拆分为多个文件，点击“下一步”。

<a href="images/2026-08-30-17-48-34.png" target="_blank"> <img src="images/2026-08-30-17-48-34.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

点击“完成”创建虚拟机。

<a href="images/2026-08-30-17-48-57.png" target="_blank"> <img src="images/2026-08-30-17-48-57.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

打开 **编辑虚拟机设置**，

<a href="images/2026-08-30-17-50-15.png" target="_blank"> <img src="images/2026-08-30-17-50-15.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

选中向导生成的临时硬盘，点击 **移除**，再点击“确定”。只移除设备，不要删除后续可能需要的文件。

<a href="images/2026-08-30-17-50-48.png" target="_blank"> <img src="images/2026-08-30-17-50-48.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 五、准备 Recovery 下载环境

首先安装 Python。打开 https://www.python.org/downloads/windows/，在稳定版本区域选择 **Windows installer (64-bit)**。

<a href="images/2026-08-30-17-55-50.png" target="_blank"> <img src="images/2026-08-30-17-55-50.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

安装程序第一页勾选 **Add python.exe to PATH**，然后选择 **Install Now**。

<a href="images/2026-08-30-17-57-17.png" target="_blank"> <img src="images/2026-08-30-17-57-17.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

安装完成后点击 **Disable path length limit**（如果显示该选项），再点击 Close。

<a href="images/2026-08-30-17-59-34.png" target="_blank"> <img src="images/2026-08-30-17-59-34.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

打开 PowerShell，运行下面的命令检查 Python：

```powershell
py -3 --version
```

<a href="images/2026-08-30-18-00-41.png" target="_blank"> <img src="images/2026-08-30-18-00-41.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

如图显示出版本号即为安装成功

<a href="images/2026-08-30-18-01-02.png" target="_blank"> <img src="images/2026-08-30-18-01-02.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

接着下载 OpenCorePkg。打开 https://github.com/acidanthera/OpenCorePkg/releases/tag/1.0.7，下载源码压缩包并解压。

<a href="images/2026-08-30-18-02-02.png" target="_blank"> <img src="images/2026-08-30-18-02-02.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

解压后必须能找到：

```text
D:\tools\OpenCore-1.0.7-RELEASE\Utilities\macrecovery\macrecovery.py
```

注意不要多套一层目录；以 PowerShell 中实际存在的 `macrecovery.py` 路径为准。

<a href="images/2026-08-30-18-05-00.png" target="_blank"> <img src="images/2026-08-30-18-05-00.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

### 下载 Apple Recovery

打开 PowerShell，运行以下命令。脚本会从 Apple 服务器下载 Recovery 文件，过程可能需要几分钟，请不要关闭 PowerShell。

```powershell
$mr = 'D:\tools\OpenCore-1.0.7-RELEASE\Utilities\macrecovery\macrecovery.py'
$out = 'D:\vmware\macos-vm\recovery'

New-Item -ItemType Directory -Force -Path $out | Out-Null

py -3 $mr `
    -b Mac-937A206F2EE63C01 `
    -m 00000000000000000 `
    download `
    -o $out `
    -v
```

<a href="images/2026-08-30-18-06-12.png" target="_blank"> <img src="images/2026-08-30-18-06-12.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

下载完成后检查文件：

```powershell
Get-ChildItem 'D:\vmware\macos-vm\recovery'
```

正常应看到：

```text
BaseSystem.dmg
BaseSystem.chunklist
```

<a href="images/2026-08-30-18-13-48.png" target="_blank"> <img src="images/2026-08-30-18-13-48.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 六、转换 Recovery 并创建 128 GB 系统盘

下一步使用 `dmg2img` 将 `.dmg` 转换成 IMG。打开 https://www.softpedia.com/get/System/Hard-Disk-Utils/DMG2IMG.shtml，下载 Windows 版 `dmg2img-1.6.7-win32.zip`。

<a href="images/2026-08-30-18-16-17.png" target="_blank"> <img src="images/2026-08-30-18-16-17.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

在下载链接页面选择 **Softpedia Secure Download (US)**，确认文件是 ZIP 压缩包。

<a href="images/2026-08-30-18-17-57.png" target="_blank"> <img src="images/2026-08-30-18-17-57.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

将压缩包解压到英文路径，例如：

```text
D:\tools\dmg2img-1.6.7-win32
```

<a href="images/2026-08-30-18-18-26.png" target="_blank"> <img src="images/2026-08-30-18-18-26.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

打开 PowerShell，复制并执行下面的命令：

```powershell
& 'D:\tools\dmg2img-1.6.7-win32\dmg2img.exe' 'D:\vmware\macos-vm\recovery\BaseSystem.dmg' 'D:\vmware\macos-vm\recovery\BaseSystem.img'
```

<a href="images/2026-08-30-18-19-32.png" target="_blank"> <img src="images/2026-08-30-18-19-32.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

还需要安装 VirtualBox，仅借用它的 `VBoxManage.exe` 将 IMG 转成 VMware 的 VMDK。打开 https://www.virtualbox.org/wiki/Downloads，选择 **Windows hosts** 下载。
<a href="images/2026-08-30-18-22-10.png" target="_blank"> <img src="images/2026-08-30-18-22-10.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

安装时基本保持默认即可；安装完成后可以取消“安装后运行 VirtualBox”，点击“完成”。

<a href="images/2026-08-30-18-24-31.png" target="_blank"> <img src="images/2026-08-30-18-24-31.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

在 PowerShell 中执行：

```powershell
& 'C:\Program Files\Oracle\VirtualBox\VBoxManage.exe' convertfromraw 'D:\vmware\macos-vm\recovery\BaseSystem.img' 'D:\vmware\macos-vm\recovery\BaseSystem.vmdk' --format VMDK
```

<a href="images/2026-08-30-18-26-21.png" target="_blank"> <img src="images/2026-08-30-18-26-21.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

现在创建用于安装 macOS 的 128 GB 虚拟硬盘。在 PowerShell 中执行：

```powershell
$vb = 'C:\Program Files\Oracle\VirtualBox\VBoxManage.exe'
$vm = 'D:\vmware\macos-vm'

& $vb createmedium disk --filename "$vm\macos-disk-128.vdi" --size 131072 --format VDI
& $vb clonemedium disk "$vm\macos-disk-128.vdi" "$vm\macos-disk-128.vmdk" --format VMDK
```

回到 VMware 的虚拟机设置界面，点击 **添加** → **硬盘**。

<a href="images/2026-08-30-18-31-49.png" target="_blank"> <img src="images/2026-08-30-18-31-49.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>
点击 添加 → 硬盘

<a href="images/2026-08-30-18-32-24.png" target="_blank"> <img src="images/2026-08-30-18-32-24.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>
SATA
<a href="images/2026-08-30-18-32-50.png" target="_blank"> <img src="images/2026-08-30-18-32-50.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

使用现有虚拟硬盘

<a href="images/2026-08-30-18-33-20.png" target="_blank"> <img src="images/2026-08-30-18-33-20.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

选择：

```text
D:\vmware\macos-vm\recovery\BaseSystem.vmdk
```

<a href="images/2026-08-30-18-33-54.png" target="_blank"> <img src="images/2026-08-30-18-33-54.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

保持现有格式

<a href="images/2026-08-30-18-34-54.png" target="_blank"> <img src="images/2026-08-30-18-34-54.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

以同样方式添加第二块盘：

```text
D:\vmware\macos-vm\macos-disk-128.vmdk
```

遇到格式提示时选择 **保持现有格式**。

<a href="images/2026-08-30-18-36-31.png" target="_blank"> <img src="images/2026-08-30-18-36-31.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

在显示设置中确认没有勾选 **加速 3D 图形**，保存设置后启动虚拟机。

<a href="images/2026-08-30-18-39-48.png" target="_blank"> <img src="images/2026-08-30-18-39-48.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 七、安装 macOS Sequoia

进入恢复环境后选择简体中文，点击“下一步”。

<a href="images/2026-08-30-18-40-54.png" target="_blank"> <img src="images/2026-08-30-18-40-54.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

选择磁盘工具，然后继续

<a href="images/2026-08-30-18-41-49.png" target="_blank"> <img src="images/2026-08-30-18-41-49.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

打开“磁盘工具”，选择“显示所有设备”。选中容量约 128 GB（macOS 可能显示约 137 GB）的物理磁盘，点击“抹掉”。不要选择约 3 GB 的 `BaseSystem` 恢复盘。

<a href="images/2026-08-30-18-44-22.png" target="_blank"> <img src="images/2026-08-30-18-44-22.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

- 名称：Macintosh HD
- 格式：APFS
- 方案：GUID 分区图

点击“抹掉”，完成后点击“完成”。

<a href="images/2026-08-30-18-45-50.png" target="_blank"> <img src="images/2026-08-30-18-45-50.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

抹除完成后点击“完成”，再点击左上角红色按钮退出磁盘工具。

<a href="images/2026-08-30-18-46-41.png" target="_blank"> <img src="images/2026-08-30-18-46-41.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

在恢复菜单中选择 **重新安装 macOS Sequoia**，点击“继续”。

<a href="images/2026-08-30-18-47-14.png" target="_blank"> <img src="images/2026-08-30-18-47-14.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

接受许可协议，安装目标选择刚刚抹除的 **Macintosh HD**，点击“继续”。安装过程会下载完整系统并自动重启多次；不要强制关闭 VMware。

<a href="images/2026-08-30-18-48-51.png" target="_blank"> <img src="images/2026-08-30-18-48-51.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

地区选择 **中国大陆**。

<a href="images/2026-08-30-21-45-51.png" target="_blank"> <img src="images/2026-08-30-21-45-51.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

数据迁移选择 **设置为新机**。

<a href="images/2026-08-30-21-47-01.png" target="_blank"> <img src="images/2026-08-30-21-47-01.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

按向导继续到创建账户页面。设置本地账户名称和密码；个人使用可以先不登录 Apple 账户。

<a href="images/2026-08-30-21-49-01.png" target="_blank"> <img src="images/2026-08-30-21-49-01.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

Apple 账户页面选择 **稍后设置**，并确认跳过。
<a href="images/2026-08-30-21-52-28.png" target="_blank"> <img src="images/2026-08-30-21-52-28.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

定位服务可不启用；出现二次确认时选择 **不使用**。
<a href="images/2026-08-30-21-53-16.png" target="_blank"> <img src="images/2026-08-30-21-53-16.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

时区选择 **中国标准时间**，最近的城市选择 **上海 – 中国大陆**，点击“继续”。

<a href="images/2026-08-30-21-55-10.png" target="_blank"> <img src="images/2026-08-30-21-55-10.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

分析数据共享选项全部不勾选，点击“继续”。

<a href="images/2026-08-30-21-55-48.png" target="_blank"> <img src="images/2026-08-30-21-55-48.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

自动更新页面点击左下角 **自动下载手动安装更新**，再点击“继续”。非官方虚拟机不建议自动安装系统更新。

<a href="images/2026-08-30-21-57-14.png" target="_blank"> <img src="images/2026-08-30-21-57-14.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

完成设置后进入 macOS 桌面。此时先正常关机，并在 VMware 中创建一个“安装完成”快照，再重新启动一次确认可以独立启动。

<a href="images/2026-08-30-21-58-01.png" target="_blank"> <img src="images/2026-08-30-21-58-01.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

点左上角苹果图标，点关机

<a href="images/2026-08-30-22-02-24.png" target="_blank"> <img src="images/2026-08-30-22-02-24.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

虚拟机保持关机状态时，点击 **虚拟机 → 快照 → 拍摄快照…**，名称填写 `macOS Sequoia 安装完成`。
<a href="images/2026-08-30-22-04-46.png" target="_blank"> <img src="images/2026-08-30-22-04-46.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

重新启动虚拟机，确认能正常进入 macOS 桌面。
<a href="images/2026-08-30-22-05-49.png" target="_blank"> <img src="images/2026-08-30-22-05-49.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

如果可以正常进入桌面，主线安装就完成了。

<a href="images/2026-08-30-22-07-51.png" target="_blank"> <img src="images/2026-08-30-22-07-51.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 八、移除临时 Recovery 盘并安装 VMware Tools

再次正常关闭虚拟机，打开虚拟机设置。

<a href="images/2026-08-30-22-09-43.png" target="_blank"> <img src="images/2026-08-30-22-09-43.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

选中容量约 3 GB、路径包含 `BaseSystem` 的临时硬盘，点击“移除”。提示删除文件时选择**仅从虚拟机移除，不删除文件**；保留 128 GB 系统盘。

<a href="images/2026-08-30-22-10-16.png" target="_blank"> <img src="images/2026-08-30-22-10-16.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

启动 macOS，在 VMware 顶部菜单中选择 **虚拟机 → 安装 VMware Tools**。VMware 会挂载自带的 `darwin.iso`。

<a href="images/2026-08-30-22-34-59.png" target="_blank"> <img src="images/2026-08-30-22-34-59.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

打开挂载的 **VMware Tools** 磁盘，双击 **安装 VMware Tools**。

<a href="images/2026-08-30-22-37-04.png" target="_blank"> <img src="images/2026-08-30-22-37-04.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

按向导点击“继续”并输入 macOS 账户密码。安装结束后按提示重新启动。

<a href="images/2026-08-30-22-38-09.png" target="_blank"> <img src="images/2026-08-30-22-38-09.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

如果出现“系统扩展已被阻止”，打开 **系统设置 → 隐私与安全性**，滚动到底部，找到 `VMware, Inc.` 后点击“允许”，再重新启动。

<a href="images/2026-08-30-22-39-54.png" target="_blank"> <img src="images/2026-08-30-22-39-54.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

重启后测试宿主机与虚拟机之间的复制、粘贴和拖放功能。Windows 键在 macOS 客户机中通常映射为 Command 键，因此粘贴快捷键是 **Win + V（⌘ + V）**，不是 Ctrl + V。

<a href="images/2026-08-30-22-40-26.png" target="_blank"> <img src="images/2026-08-30-22-40-26.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

如果复制粘贴正常，说明 VMware Tools 已经生效。弹出的 VMware Tools 磁盘可以在 macOS 桌面上推出；以后需要时可从 VMware 菜单重新挂载。

<a href="images/2026-08-30-22-44-26.png" target="_blank"> <img src="images/2026-08-30-22-44-26.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

最后正常关机，再创建一个快照，例如 `macOS Sequoia-Tools已安装-可用`。之后即可投入使用。

## 九、日常使用与注意事项

- macOS、应用和游戏都会占用 128 GB 虚拟系统盘的空间；该磁盘是动态增长的，不会一开始就占满。
- 系统更新前先创建快照，并手动确认兼容性。
- 不要删除当前使用的 `macos-disk-128*` 文件；旧的 80 GB 文件可以暂时保留。
- RTX 5070 Laptop 没有 macOS 原生驱动，保持 VMware 的 3D 加速关闭，图形性能有限属于预期现象。
- 如果以后需要在 Windows 与 macOS 之间共享大量文件，可以另行配置 VMware 共享文件夹。

至此，macOS Sequoia 虚拟机的安装、清理和 VMware Tools 配置全部完成。

更多虚拟机系统部署方案请返回[虚拟机系统部署指南](/p/virtual-machine-system-setup-guide/)。
