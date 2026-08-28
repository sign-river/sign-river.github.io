---
title: "Windows 多账号 Codex 管理：额度看板、快速切换与安全配置"
date: 2026-08-20
description: "本文记录在 Windows 上从源码构建并安装 Codex Switcher 的完整流程：添加本人控制的官方 Codex 账号、查看各账号剩余额度和重置时间，以及配置仅限本机的安全切换策略。文中不涉及批量注册、临时邮箱、账号共享或第三方中转，仅用于管理自有账号。"
categories:
  - "开发"
tags:
  - "Codex"
  - "Codex Switcher"
  - "Windows"
  - "多账号管理"
  - "账号安全"
  - "源码构建"
draft: false
slug: "windows-multi-account-codex-management"
related_group: "codex"
hidden: true
searchable: true
guide: "/p/codex-guide/"
guide_title: "Codex 使用指南"
---

本文记录在 Windows 上安装并使用 Codex Switcher 的过程，包括添加本人控制的官方 Codex 账号、查看各账号的剩余额度和重置时间，以及在本机完成账号切换。

如果日常使用 Codex 的频率较高，单个账号的额度可能无法满足需求。频繁登录和验证不同账号也比较繁琐，因此可以使用 Codex Switcher 集中管理账号，并在额度耗尽或账号出现异常时切换到其他已登录账号。

## 1. 安装 Codex Switcher

打开 [Codex Switcher 的 Releases 页面](https://github.com/VallierDev/codex-switcher/releases)，下载适用于 Windows 的 `Codex Switcher_0.7.8_x64-setup.exe`，也可以直接使用链接下载

[安装包下载链接](https://github.com/VallierDev/codex-switcher/releases/download/v0.7.8/Codex.Switcher_0.7.8_x64-setup.exe)

下载完成后双击安装包，按照向导完成安装即可。

<a href="images/2026-08-21-03-19-47.png" target="_blank"> <img src="images/2026-08-21-03-19-47.png" alt="image" style="max-width: 70%; width: 1000px;"/> </a>

如果官方仓库中的程序在本机运行异常，也可以尝试我修改后的版本：
[Codex Switcher 0.7.8 MSI](https://gitlink.org.cn/signriver/file-warehouse/releases/download/Codex_Switcher/Codex%20Switcher_0.7.8_x64_en-US.msi)

## 2. 登录 Codex 账号

启动应用后，先登录需要管理的账号。

<a href="images/2026-08-21-03-22-43.png" target="_blank"> <img src="images/2026-08-21-03-22-43.png" alt="image" style="max-width: 70%; width: 1000px;"/> </a>

我这里有多个官方账号，因此选择列表中的第一个官方登录入口。

<a href="images/2026-08-21-03-23-21.png" target="_blank"> <img src="images/2026-08-21-03-23-21.png" alt="image" style="max-width: 70%; width: 1000px;"/> </a>

登录流程按页面提示完成即可。登录多个账号后，可以在账号列表中查看它们的状态、剩余额度和重置时间。

<a href="images/2026-08-29-01-56-43.png" target="_blank"> <img src="images/2026-08-29-01-56-43.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 3. 刷新额度与保活

在**代理**界面中，可以开启**自动刷新账号额度**。

<a href="images/2026-08-29-01-57-24.png" target="_blank"> <img src="images/2026-08-29-01-57-24.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

然后在**设置**界面中开启**保活**。

<a href="images/2026-08-29-01-58-09.png" target="_blank"> <img src="images/2026-08-29-01-58-09.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 4. 切换当前账号

需要切换账号时，先彻底退出 `Codex`，确保程序已经关闭。

<a href="images/2026-08-29-01-58-50.png" target="_blank"> <img src="images/2026-08-29-01-58-50.png" alt="image" style="max-width: 40%; width: 1000px;"/> </a>

回到 Codex Switcher，点击目标账号对应的**切换**操作。

<a href="images/2026-08-29-01-59-07.png" target="_blank"> <img src="images/2026-08-29-01-59-07.png" alt="image" style="max-width: 70%; width: 1000px;"/> </a>

切换完成后重新打开 `Codex`，即可使用目标账号。这样可以减少重复登录和验证的操作。
