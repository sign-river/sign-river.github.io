---
title: "启动器报错“游戏数据访问错误。我们没有游戏数据目录的读写权限。请联系支持人员”"
date: 2026-07-15
description: "启动器报错“游戏数据访问错误。我们没有游戏数据目录的读写权限。请联系支持人员”的排查与解决方法，整理常见原因、操作步骤和相关报错截图。"
categories:
  - "报错"
tags:
  - "Paradox Launcher"
  - "P 社启动器"
  - "启动器故障"
  - "问题排查"
  - "Windows"
draft: false
slug: "paradox-launcher-error-08"
---

> 本文整理自《群星常见问题合集及解决办法》，原作者：唏嘘南溪。文档内容会随实际反馈持续修正。

## 1. 报错现象

启动器报错“游戏数据访问错误。我们没有游戏数据目录的读写权限。请联系支持人员”。

## 2. 解决方法

<a href="images/error-01.png" target="_blank"><img src="images/error-01.png" alt="启动器报错“游戏数据访问错误。我们没有游戏数据目录的读写权限。请联系支持人员”相关报错截图 1" style="display: block; max-width: 100%; width: auto; height: auto; margin: 1rem auto;"/></a>

方法一：

转到 Windows 安全中心

在“病毒和威胁防护设置”下，点击“管理设置”

向下滚动到“受控文件夹访问”，然后单击“管理受控文件夹访问权限”

点击“允许应用通过受控文件夹访问”

点击“+添加允许的应用程序”，然后点击“浏览所有应用程序”

将以下文件添加进去

C:\Users(用户)\用户名\AppData\Local\Programs\Paradox Interactive\launcher，在其中找到你当前启动器版本的文件，如 launcher-v2.2024.10，进入该文件夹，添加文件 Paradox Launcher.exe。上述是默认路径，如果你启动器安装到了其他的地方，按照你自己的路径即可。

在 Steam 的库中右键 stellaris 图标，管理->浏览本地文件，找到 dowser.exe 和 stellaris.exe，把它们添加进去

回到 windows 安全中心，在”勒索软件防护”下，再次执行上述操作

方法二：

如果感到 windows 安全防护没有必要存在，我们可以直接把它关掉一劳永逸

同时按下 win+R，输入 gpedit.msc，打开策略组编辑器

通过计算机配置>>管理模版>>windows 组件>>Microsoft Defender 防病毒

在右侧找到”允许反恶意软件服务始终保持运行状态”,双击打开，选择已禁用，点击确定即可

## 3. 仍未解决

如果上述方法不适用，建议记录完整报错文字、复现步骤和 `error.log` 内容后再进一步排查。也可以联系原文作者（QQ：3217344726）反馈，以便补充或修正方案。

