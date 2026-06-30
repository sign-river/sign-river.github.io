---
title: "从零搭建文件下载服务器完整教程"
date: 2026-06-30
description: "从购买服务器、部署相关软件到挂载文件供下载的全流程记录"
categories:
  - "系统"
tags:
  - "阿里云"
  - "ECS"
  - "Linux"
  - "Ubuntu"
  - "服务器"
  - "文件下载"
  - "Nginx"
draft: false
slug: "file-download-server-setup"
---

> 💡 **前言**：本文记录从零开始搭建一台可供他人下载文件的服务器的完整过程，涵盖服务器选购、环境部署与文件挂载等步骤。

## 1. 概述

（待补充）

## 2. 购买服务器

### 2.1. 打开产品页并选择优惠套餐

本教程选用阿里云 ECS 作为服务器平台。首先打开 [阿里云 ECS 产品页](https://www.aliyun.com/product/ecs?spm=5176.30275541.J_ZGek9Blx07Hclc3Ddt9dg.2.3c872f3dr4kUFP&scm=20140722.S_card@@%E4%BA%A7%E5%93%81@@163972.S_new~UND~card.ID_card@@%E4%BA%A7%E5%93%81@@163972-RL_%E6%9C%8D%E5%8A%A1%E5%99%A8-LOC_2024SPSearchCard-OR_ser-PAR1_0bc059b717827943826333110e2327-V_4-RE_new13-P0_0-P1_0)，在页面中找到 **99 元/年** 的优惠服务器套餐并点击购买。

<a href="images/2026-06-30-13-00-11.png" target="_blank"> <img src="images/2026-06-30-13-00-11.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

### 2.2. 服务器配置与下单

进入配置页面后，操作系统选择 **Ubuntu 24.04 64 位**。

<a href="images/操作系统选择截图.png" target="_blank"> <img src="images/操作系统选择截图.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

同时勾选 **自动续费**，避免到期后服务器被释放导致服务中断。

<a href="images/自动续费选项截图.png" target="_blank"> <img src="images/自动续费选项截图.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

### 2.3. 连接服务器

服务器创建完成后，进入阿里云 ECS 控制台，找到对应实例，点击 **远程连接**，直接使用阿里云自带的远程连接功能接入服务器。

<a href="images/阿里云远程连接截图.png" target="_blank"> <img src="images/阿里云远程连接截图.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 3. 部署相关软件

### 3.1. 基础环境准备

成功接入服务器后，依次执行以下操作。

#### 3.1.1. 更新系统软件包

```bash
sudo apt update && sudo apt upgrade -y
```

#### 3.1.2. 创建下载目录

创建一个固定用于存放下载文件的目录：

```bash
sudo mkdir -p /var/www/download
```

#### 3.1.3. 设置目录权限

将目录所有权赋予当前用户和 Nginx 组，并设置访问权限：

```bash
sudo chown -R $USER:www-data /var/www/download
sudo chmod -R 755 /var/www/download
```

### 3.2. 安装 Nginx

执行以下命令安装 Nginx：

```bash
sudo apt install nginx -y
```

### 3.3. 删除默认站点

执行以下命令，删除 Nginx 自带的默认页面：

```bash
sudo rm -f /etc/nginx/sites-enabled/default
```

### 3.4. 配置 Nginx

在远程连接界面中，通过左侧面板的 **文件管理**，依次展开目录：`/etc` → `nginx` → `conf.d`。

<a href="images/进入%20conf.d%20目录截图.png" target="_blank"> <img src="images/进入%20conf.d%20目录截图.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

右键点击 `conf.d` 文件夹，选择 **新建文件**，文件名为 `download.conf`。

<a href="images/新建%20download.conf%20文件截图.png" target="_blank"> <img src="images/新建%20download.conf%20文件截图.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

双击打开 `download.conf`，写入以下配置内容：

<a href="images/2026-06-30-13-53-46.png" target="_blank"> <img src="images/2026-06-30-13-53-46.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

```nginx
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    server_name _;

    location / {
        root /var/www/download;

        autoindex on;
        autoindex_exact_size off;
        autoindex_localtime on;
        charset utf-8;

        # 核心限速策略：前 5MB 满速，之后限制在 100 KB/s
        limit_rate_after 5m;
        limit_rate 100k;
    }
}
```

编辑完成后，按 **Ctrl+S** 保存。

<a href="images/download.conf%20文件编辑截图.png" target="_blank"> <img src="images/download.conf%20文件编辑截图.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

回到终端，执行以下命令检查 Nginx 配置是否有语法问题：

```bash
sudo nginx -t
```

若输出 `syntax is ok` 和 `test is successful`，代表配置没有问题。

<a href="images/2026-06-30-13-57-41.png" target="_blank"> <img src="images/2026-06-30-13-57-41.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

然后执行以下命令重启 Nginx，使配置生效：

```bash
sudo systemctl restart nginx
```

## 4. 挂载文件供下载

### 4.1. 创建测试文件

执行以下命令，在下载目录中创建一个测试文件：

```bash
echo "Hello, this is a test file!" | sudo tee /var/www/download/test.txt
```

### 4.2. 访问下载界面

根据服务器的公网 IP 地址，在浏览器中输入 `http://<公网IP>/` 进行访问。例如本教程使用的服务器地址为 `http://59.110.167.218/`，打开后即可看到文件下载界面，其中应包含刚才创建的 `test.txt`。

<a href="images/文件下载界面截图.png" target="_blank"> <img src="images/文件下载界面截图.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

### 4.3. 上传文件

以后如需挂载新文件，只需在 **文件管理** 中打开 `/var/www/download` 目录，点击界面左上角的 **上传文件**，选中需要挂载的文件即可。

<a href="images/上传文件截图.png" target="_blank"> <img src="images/上传文件截图.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 5. 验证效果

效果如图所示

<a href="images/2026-06-30-14-08-35.png" target="_blank"> <img src="images/2026-06-30-14-08-35.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>
