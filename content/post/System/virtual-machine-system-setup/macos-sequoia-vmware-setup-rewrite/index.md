---
title: "在 Windows 的 VMware 中安装 macOS Sequoia（重写版）"
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
draft: true
slug: "macos-sequoia-vmware-setup-rewrite"
---

首先是下载 vmare，你可以选择按照下面的教程从官网下载，或是直接从我上传的这里下载 xxx 版本 https://github.com/sign-river/File_warehouse/releases/download/VMware/VMware-workstation-full-17.6.4-24832109.exe

进入 https://support.broadcom.com/，注册

<a href="images/2026-08-30-16-32-03.png" target="_blank"> <img src="images/2026-08-30-16-32-03.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

回到主页面登录

<a href="images/2026-08-30-16-34-53.png" target="_blank"> <img src="images/2026-08-30-16-34-53.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

然后直接进入 https://support.broadcom.com/group/ecx/productdownloads?subfamily=VMware%20Workstation%20Pro&freeDownloads=true，点击xxx，选择xxx

<a href="images/2026-08-30-16-40-31.png" target="_blank"> <img src="images/2026-08-30-16-40-31.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

点击 xxx 后回到界面勾选同意

<a href="images/2026-08-30-16-42-26.png" target="_blank"> <img src="images/2026-08-30-16-42-26.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

然后下载

<a href="images/2026-08-30-16-42-56.png" target="_blank"> <img src="images/2026-08-30-16-42-56.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

填写个人信息，以下每个框的意思是 xxx，需要填写 xxx。填完后点击 xxx

<a href="images/2026-08-30-16-48-14.png" target="_blank"> <img src="images/2026-08-30-16-48-14.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

回到 xxx 界面，重新点击 xxx

<a href="images/2026-08-30-16-49-09.png" target="_blank"> <img src="images/2026-08-30-16-49-09.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

双击下载后的 exe，一路上都是傻瓜问题，一路下一步即可，然后安装，直到安装完成

<a href="images/2026-08-30-16-59-44.png" target="_blank"> <img src="images/2026-08-30-16-59-44.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

接下来是下载 unlock

打开 https://github.com/DrDonk/unlocker/releases/tag/v4.2.8，下载 zip 包

<a href="images/2026-08-30-17-01-42.png" target="_blank"> <img src="images/2026-08-30-17-01-42.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

下载完成后吧他解压到一个全英文的文件夹里

<a href="images/2026-08-30-17-10-47.png" target="_blank"> <img src="images/2026-08-30-17-10-47.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

如果之前打开过 wmxxx，先完全退出，然后进入 xxx 文件夹，右键以管理员身份执行 xxx

<a href="images/2026-08-30-17-13-13.png" target="_blank"> <img src="images/2026-08-30-17-13-13.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

运行成功后运行 xxx 检查状态

<a href="images/2026-08-30-17-13-54.png" target="_blank"> <img src="images/2026-08-30-17-13-54.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

四项都有（1），说明补丁应用成功

<a href="images/2026-08-30-17-15-30.png" target="_blank"> <img src="images/2026-08-30-17-15-30.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

接下来启动 VMware Workstation Pro，遇到新版本提示选择跳过，否则可能覆盖我们刚打的补丁

<a href="images/2026-08-30-17-17-35.png" target="_blank"> <img src="images/2026-08-30-17-17-35.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

创建虚拟机，高级，下一步

<a href="images/2026-08-30-17-18-07.png" target="_blank"> <img src="images/2026-08-30-17-18-07.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

保持当前已经选中的：Workstation 17.5 or later 然后点击 下一步
<a href="images/2026-08-30-17-21-07.png" target="_blank"> <img src="images/2026-08-30-17-21-07.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

选择 xxx，然后下一步

<a href="images/2026-08-30-17-23-26.png" target="_blank"> <img src="images/2026-08-30-17-23-26.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>
