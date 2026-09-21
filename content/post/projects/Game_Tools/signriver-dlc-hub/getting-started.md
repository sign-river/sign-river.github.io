---
title: "快速开始"
description: "从下载解压到完成第一次 DLC 解锁。"
type: "project-docs"
url: "/p/signriver-dlc-hub/getting-started/"
weight: 10
toc: true
draft: false
---

SignRiver DLC Hub 目前支持 Windows、SteamOS 与 macOS（Intel）。本文以 Windows 端为例，另外两端操作基本一致。

## 1. 下载并解压

从 [GitHub Releases](https://github.com/sign-river/SignRiver-DLC-Hub/releases) 下载对应平台的压缩包：Windows 选 `windows-x64`，SteamOS 选 `steamos-x64`，macOS 选 `macos-x64`。

把压缩包解压到本地磁盘上任意可读写的目录，例如 `D:\Tools\SignRiver-DLC-Hub`，然后双击其中的 **唏嘘南溪 DLC 一键解锁工具.exe** 启动程序。

<a href="../images/2026-09-22-04-42-49.png" target="_blank"> <img src="../images/2026-09-22-04-42-49.png" alt="image" style="max-width: 60%; width: 1000px;"/> </a>

解压后的目录中除了主程序，还有 `app`、`config`、`data` 等运行所需的目录，请保持它们与主程序在同一层。

> 必须先解压，再运行。直接在压缩包里双击启动会缺少依赖目录，程序无法正常加载。
>
> macOS 首次打开若提示“无法打开”或“已损坏”，SteamOS 若提示权限不足，可参考程序内「报错指南」中的对应条目处理。

## 2. 首次启动与公告

程序启动后会先弹出公告窗口，内容包括更新方式、使用方法和遇到问题时的处理入口。阅读后点击 **关闭公告** 进入主界面。

如果不想在短期内重复看到同一条公告，可以点击 **下次公告更新前不再显示**；之后仍可在 **设置 → 常规设置** 中重新打开公告提醒。

<a href="../images/2026-09-22-04-16-54.png" target="_blank"> <img src="../images/2026-09-22-04-16-54.png" alt="image" style="max-width: 60%; width: 1000px;"/> </a>

## 3. 确认游戏目录

程序会自动扫描 Steam 库并定位游戏目录。界面显示 **路径正常** 或 **路径已验证**，表示当前目录有效。

如果状态异常，先点击 **重新扫描**；仍然识别不到时，再点击 **选择目录** 手动指定游戏根目录。目录确认无误后，还可以用 **启动游戏** 和 **打开目录** 快速验证。

在 **当前游戏** 下拉框中可以切换要处理的游戏，点击 **复制游戏列表** 会把当前支持的游戏列表复制到剪贴板。

## 4. 勾选 DLC 并解锁

在 DLC 列表中勾选需要的条目，或直接点击 **全选 DLC**，然后点击 **一键解锁**。

程序会先写入解锁补丁，补丁就绪后再从云端下载并安装所选的 DLC。下载与写入的进度可以在 **下载任务** 页查看，完成后对应条目会显示 **已安装**。

<a href="../images/2026-09-22-04-17-30.png" target="_blank"> <img src="../images/2026-09-22-04-17-30.png" alt="image" style="max-width: 60%; width: 1000px;"/> </a>

> 执行解锁前请先关闭游戏，程序检测到游戏正在运行时会拒绝执行。
