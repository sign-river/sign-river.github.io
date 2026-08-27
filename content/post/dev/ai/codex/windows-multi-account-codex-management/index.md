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

本文记录在 Windows 上从源码构建并安装 Codex Switcher 的完整流程：添加本人控制的官方 Codex 账号、查看各账号剩余额度和重置时间，以及配置仅限本机的安全切换策略。

像本人 ai 重度依赖，没有 ai 就浑身难受，但是一个号的额度又不够狠狠瞪，这就导致我需要频繁切换账号，太麻烦了，为此我在 github 上找到了一个使用的项目 Codex Switcher，可以在额度耗尽或者账户出错时自动帮你切换账号，非常的好用，接下来我来记录一下使用的流程

首先进入 release 界面 https://github.com/VallierDev/codex-switcher/releases，选择适合 windows 场景的 Codex Switcher_0.7.8_x64-setup.exe，https://github.com/VallierDev/codex-switcher/releases/download/v0.7.8/Codex.Switcher_0.7.8_x64-setup.exe；下载后双击安装即可，安装流程非常简单，这里不过多讲述

<a href="images/2026-08-21-03-19-47.png" target="_blank"> <img src="images/2026-08-21-03-19-47.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

首先进入应用，先进行登录账户操作

<a href="images/2026-08-21-03-22-43.png" target="_blank"> <img src="images/2026-08-21-03-22-43.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

我这里因为有不少官方的账户，所以直接选择第一个官方登录

<a href="images/2026-08-21-03-23-21.png" target="_blank"> <img src="images/2026-08-21-03-23-21.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

登录流程非常简单，这里直接跳过，
