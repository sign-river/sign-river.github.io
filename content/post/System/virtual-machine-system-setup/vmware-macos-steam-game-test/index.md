---
title: "VMware macOS 虚拟机 Steam 游戏实测：从无法启动到《都市：天际线》勉强可用"
date: 2026-08-22
description: "以 Paradox 系列 Steam 游戏为测试载荷，验证 VMware macOS Sequoia 虚拟机的图形兼容性、DLC 状态检查能力及实际使用边界。"
categories:
  - "系统"
tags:
  - "macOS Sequoia"
  - "VMware Workstation"
  - "虚拟机"
  - "Steam"
  - "都市：天际线"
  - "群星"
  - "钢铁雄心 IV"
  - "图形兼容性"
draft: false
slug: "vmware-macos-steam-game-test"
related_group: "virtual-machine-system-setup"
hidden: true
searchable: true
guide: "/p/virtual-machine-system-setup-guide/"
guide_title: "虚拟机系统部署指南"
---

本文不是游戏玩法或帧率评测，而是一次在 VMware macOS Sequoia 虚拟机中使用 Steam 验证游戏兼容性和 DLC 状态的实录。测试目标很明确：确认 macOS 客户端能否启动目标游戏、进入主菜单、识别已解锁的 DLC，并完成必要的界面操作。

虚拟机的安装与基础配置可参考[在 Windows 的 VMware 中安装 macOS Sequoia](/p/macos-sequoia-vmware-setup/)。本文只记录 Steam 和游戏启动之后遇到的问题，以及为完成验证所做的调整。

## 1. 测试环境与目标

本次测试使用的是 Windows 宿主机上的 VMware Workstation macOS 虚拟机。虚拟机配置为 4 个 vCPU、8 GiB 内存，并开启 VMware 3D 加速。虚拟显存最初配置为 256 MiB，之后为了排查图形性能问题提高到 1 GiB。

测试内容包括：

- 在 Steam 中启动《群星》和《钢铁雄心 IV》；
- 在 Steam 中启动《都市：天际线》；
- 进入游戏主菜单，观察 DLC 列表和解锁状态；
- 不进入实际地图或长时间游玩，不以虚拟机中的游戏帧率作为验收指标；
- 验证 SignRiver 在 macOS 上的客户端和 DLC 工作流是否具备继续测试的条件。

> 这里的“可用”只表示能够完成启动、主菜单和 DLC 状态验证，并不表示虚拟机具备正常游戏所需的图形性能。

## 2. Paradox 游戏的初始结果

首先使用 Steam 启动《群星》和《钢铁雄心 IV》。两款游戏都无法在当前 VMware macOS 图形环境中正常运行，未能稳定进入可用的游戏主界面。

这说明“macOS 能进入桌面”和“Steam 能启动游戏”并不等于“游戏的图形渲染路径可用”。尤其是 Paradox 游戏使用的渲染、窗口和输入链路更复杂，虚拟机中的兼容性不能只根据 Steam 客户端本身判断。

随后测试《都市：天际线》。它能够启动并进入主菜单，左侧 DLC 列表可以显示，部分项目右侧出现绿色状态图标，说明 DLC 解锁链路至少已经能够在 macOS 游戏端体现出来。因此后续排查都围绕这款“可以启动但严重卡顿”的游戏进行。

## 3. 第一个问题：游戏看似无法点击

第一次启动《都市：天际线》时，法律声明或首次启动界面看起来无法点击。后来通过 `Command + Tab` 切出游戏，才发现 macOS 后台弹出了系统权限对话框，要求为游戏授予“输入监控”权限。

这个弹窗被全屏游戏窗口遮挡，游戏实际上处于被系统对话框阻塞的状态，所以鼠标点击不会传递到游戏。处理方法是：

1. 使用 `Command + Tab` 切换到 macOS 的系统设置；
2. 打开 **系统设置 → 隐私与安全性 → 输入监控**；
3. 为 `Cities` 开启输入监控权限；
4. 完全退出并重新启动游戏。

> 如果游戏窗口能显示但按钮完全没有反应，先检查是否有被全屏窗口遮挡的 macOS 权限弹窗，不要立即判断为游戏坐标错位或鼠标失效。

权限处理完成后，游戏主菜单可以正常显示，DLC 状态也能够继续验证。中文语言可以从 **OPTIONS → GAMEPLAY → Language** 中选择简体中文。

## 4. 进入设置页面后严重卡顿

进入游戏设置页面后，问题变得更加明显：下拉框可以展开，但点击选项经常没有反应；其他按钮也需要快速连续点击很多次才能生效。这个现象与普通的鼠标按键损坏不同，更像是 Unity UI 事件线程和虚拟图形渲染速度过慢，导致点击事件长时间得不到处理。

当时设置页面显示的关键状态大致如下：

- 显示模式已经是窗口化；
- 内部渲染分辨率仍然接近桌面尺寸，为 `2247×1360`；
- 阴影、材质、细节等级、阴影距离、各向异性过滤和抗锯齿等选项处于较高档位；
- 窗口虽然有边框，但实际渲染量并没有明显下降。

因此，单纯把全屏切换成窗口化并不能解决问题。必须同时降低实际渲染分辨率和图形质量。

## 5. 调整 VMware 虚拟显卡

在确认 macOS 虚拟机已经完全关机、没有残留 `vmware-vmx.exe` 进程后，修改 VMware 的 VMX 配置：

```text
mks.enable3d = "TRUE"
svga.vramSize = "1073741824"
svga.graphicsMemoryKB = "1048576"
```

这会把虚拟显存请求从 256 MiB 提高到 1 GiB，同时保留 3D 加速。修改前应备份 VMX 文件，并且只修改 VMX 文本配置，不要触碰 `.vmdk`、快照链或 `.lck` 锁文件。

不过，虚拟显存容量不等于真实 GPU 性能。启动 macOS 后从 VMware 日志观察到，来宾侧实际注册的 SVGA 显存仍可能被限制在约 128 MiB。VMware 也不能把宿主机的 NVIDIA RTX 5070 以原生 Metal GPU 的形式直通给 macOS，因此提高显存只能作为排查手段，不能期待它把虚拟机变成正常的游戏主机。

## 6. 找到游戏真正使用的配置文件

《都市：天际线》安装目录是：

```text
/Users/signriver/Library/Application Support/Steam/steamapps/common/Cities_Skylines
```

游戏应用本体位于：

```text
/Users/signriver/Library/Application Support/Steam/steamapps/common/Cities_Skylines/Cities.app
```

最初只修改了 Unity 的 macOS 偏好文件：

```text
/Users/signriver/Library/Preferences/com.ColossalOrder.CitiesSkylines.plist
```

这个文件确实记录了窗口模式和分辨率，但游戏启动后又从自己的二进制配置中恢复了桌面分辨率，所以只改 plist 并没有完全生效。

真正需要修改的是：

```text
/Users/signriver/Library/Application Support/Colossal Order/Cities_Skylines/gameSettings.cgs
```

这个文件不是普通文本，而是以 `CGSF` 开头的二进制配置。它包含 `screenWidth`、`screenHeight`、`fullscreen` 以及画质相关字段。修改前必须退出游戏并备份文件，不能直接使用文本编辑器覆盖。

## 7. 固定窗口大小并降低画质

最终将 `gameSettings.cgs` 中的关键值调整为：

```text
screenWidth = 1280
screenHeight = 720
fullscreen = 0
dofMode = 0
antialiasing = 0
texturesQuality = 0
shadowsQuality = 0
shadowsDistance = 0
anisotropicFiltering = 0
levelOfDetail = 0
vsync = 0
```

同时再次写入 macOS 偏好值：

```text
Screenmanager Is Fullscreen mode = 0
Screenmanager Resolution Width = 1280
Screenmanager Resolution Height = 720
UnityGraphicsQuality = 0
```

为了防止 Steam 或 Unity 再次按桌面尺寸启动，在 Steam 的《都市：天际线》启动参数中加入：

```text
-screen-width 1280 -screen-height 720 -screen-fullscreen 0 -noWorkshop -disableMods
```

其中：

- `-screen-width 1280` 和 `-screen-height 720` 固定窗口内部渲染尺寸；
- `-screen-fullscreen 0` 强制使用窗口模式；
- `-noWorkshop` 和 `-disableMods` 只关闭创意工坊内容与模组，方便排除额外加载和脚本干扰，不会关闭 DLC。

Steam 的配置文件路径为：

```text
/Users/signriver/Library/Application Support/Steam/userdata/<Steam 用户目录>/config/localconfig.vdf
```

实际修改前先通过 Steam 自身的 `-shutdown` 参数退出客户端，避免 Steam 运行中重写 `localconfig.vdf`。

## 8. 最终结果

调整完成后，游戏不再是“完全卡住、点击几乎没有反馈”的状态，而是能够以窗口模式进入主菜单，点击响应明显恢复，足以完成：

- 进入《都市：天际线》主菜单；
- 打开设置和 DLC 列表；
- 查看 DLC 是否显示为已解锁；
- 完成 SignRiver macOS 客户端的基础验证。

但它仍然存在明显卡顿，尤其是在打开设置页面或切换复杂 UI 时。这个结果说明配置调整降低了负载，却没有改变 VMware macOS 虚拟图形路径的性能上限。

## 9. 结论与使用边界

本次测试得出的结论是：

1. 《群星》和《钢铁雄心 IV》在当前 VMware macOS 虚拟机中无法稳定运行，不能用它们作为 macOS 虚拟机的可用性证明；
2. 《都市：天际线》可以进入主菜单并显示 DLC 状态，适合作为当前 SignRiver macOS 端的验证载荷；
3. macOS 输入监控权限、Unity 配置文件和 Steam 启动参数都会影响测试结果；
4. 窗口化本身不代表降低了渲染负担，必须同时固定较低的内部渲染分辨率并降低画质；
5. 提高 VMware 虚拟显存只能缓解部分资源分配问题，不能替代真实 GPU 或原生 Metal 支持。

因此，这套 macOS 虚拟机适合用于验证程序启动、Steam 游戏主菜单、DLC 状态和跨平台工作流，不适合作为 macOS 游戏性能、帧率或长期游玩环境。

> 如果目标只是确认 DLC 解锁是否正确，进入游戏主菜单即可，不需要进入地图。这样可以减少虚拟机图形负载，也能避免把“游戏可启动”误解为“游戏可流畅运行”。
