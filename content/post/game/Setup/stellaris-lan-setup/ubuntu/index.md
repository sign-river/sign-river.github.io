---
title: "群星联机优化指南（Ubuntu 24.04 64 位）"
date: 2026-02-22
description: "基于 Ubuntu 24.04 64 位的 OpenVPN 虚拟局域网搭建教程"
draft: false
slug: "stellaris-lan-openvpn-ubuntu"
related_group: "stellaris-lan-setup"
hidden: true
searchable: true
guide: "/p/stellaris-lan-openvpn-guide/"
guide_title: "群星联机优化指南"
categories:
  - "系统"
tags:
  - "群星"
  - "Stellaris"
  - "OpenVPN"
  - "联机"
  - "虚拟局域网"
  - "游戏工具"
  - "网络配置"
  - "Ubuntu"
---

## 1. 引言

**你需要准备**：

- 一台云服务器 (VPS)：本文以 **Ubuntu 24.04 64 位**系统为例
- 基础工具：**WindTerm**（SSH 终端，推荐）
- 一颗折腾的心：虽然步骤较多，但为了流畅的银河征途，一切都是值得的！

## 2. 服务器准备与基础环境搭建

俗话说"工欲善其事，必先利其器"。搭建群星联机节点，核心在于网络质量而非服务器的计算性能。本章将指导您完成服务器的选购及基础环境的配置。

### 2.1. 服务器选购建议

在购买 VPS 时，请重点关注以下三点：

#### 2.1.1. 带宽是核心

群星联机数据交换量较大。根据实测，**约 10Mbps 带宽**可支撑 **1～2 车人**（每车约 10 人）同时游玩，**带宽越大，后期卡顿概率越低**。

#### 2.1.2. 地理位置

尽量选择距离您和朋友们地理位置都比较近的数据中心，以物理手段降低延迟。

#### 2.1.3. 配置够用即可

如果这台服务器仅用于群星加速，CPU、内存和硬盘空间可以选最低配（如 1 核 1G），以降低成本。

### 2.2. 安装必要组件

购买并登录服务器（使用 SSH 工具）后，我们需要安装解压工具和核心软件 OpenVPN。请依次执行以下指令：

#### 2.2.1. 下载 SSH 客户端（推荐 WindTerm）

为方便操作，建议使用 **WindTerm** 作为 SSH 终端：免费、绿色免安装，解压即用，支持多标签与会话管理。

- **国内镜像下载（Windows 64 位便携版）**：
  [WindTerm 2.7.0 便携版 (x86_64)](https://gitlink.org.cn/signriver/WindTerm/releases/download/2.7.0-Mirror/WindTerm_2.7.0_Windows_Portable_x86_64.zip)

  下载后解压到任意目录，路径中不要有中文，双击运行 `WindTerm.exe` 即可。

  <a href="images/2026-02-24-21-38-02.png" target="_blank"> <img src="images/2026-02-24-21-38-02.png" alt="image" style="max-width: 100%; width: 700px;"/> </a>

  存储位置选择第一个应用程序目录

  <a href="images/2026-02-24-21-39-32.png" target="_blank"> <img src="images/2026-02-24-21-39-32.png" alt="image" style="max-width: 100%; width: 500px;"/> </a>

#### 2.2.2. 使用 WindTerm 连接云服务器

1. 打开 WindTerm，点击 **「会话」→「新建会话」**。

   <a href="images/2026-02-24-21-47-17.png" target="_blank"> <img src="images/2026-02-24-21-47-17.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

2. 选择 **SSH**，在 **主机** 中填写服务器公网 IP，**端口** 一般为 `22`（若云厂商使用其他端口请按实际填写）。

- 若商家提供公网 ip 如下图，在 **主机** 中直接填写公网 IP 即可，**端口** 保持默认无需修改。

  <a href="images/2026-02-24-21-52-54.png" target="_blank"> <img src="images/2026-02-24-21-52-54.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

- 若购买的是超低价共享型 VPS，公网 IP 后带有额外端口，则在 **主机** 中填公网 IP，在 **端口** 处删掉默认的 `22`，改为 IP 后面显示的那个端口号。

  <a href="images/2026-02-24-21-54-33.png" target="_blank"> <img src="images/2026-02-24-21-54-33.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

- 按照情况填写表单

  <a href="images/2026-02-24-21-49-25.png" target="_blank"> <img src="images/2026-02-24-21-49-25.png" alt="image" style="max-width: 100%; width: 700px;"/> </a>

> 💡 **连接小贴士**：
>
> - **多次尝试**：首次连接可能失败，这是正常现象。如果连接不上，请多试几次，通常第二次或第三次就能成功连接。
> - **端口放行**：阿里云服务器默认放行 22 端口，但其他云厂商（如腾讯云、华为云等）可能需要在控制台的「安全组」中手动放行 22 端口才能连接。如果遇到连接超时，请登录云控制台检查安全组规则。

<a href="images/2026-03-06-04-50-12.png" target="_blank"> <img src="images/2026-03-06-04-50-12.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

3. 切换到账户标签页，**用户名** 默认填写为 `root`（如果有指定其他 SSH 用户名则填写对应名称），密码填写你在云服务器控制台设置的远程登录密码。

   <a href="images/2026-02-24-22-03-47.png" target="_blank"> <img src="images/2026-02-24-22-03-47.png" alt="image" style="max-width: 100%; width: 500px;"/> </a>

   <a href="images/2026-02-24-22-05-31.png" target="_blank"> <img src="images/2026-02-24-22-05-31.png" alt="image" style="max-width: 100%; width: 500px;"/> </a>

> ⚠️ **重要：不同云厂商的默认用户名可能不同**：
>
> - **阿里云**：默认用户名为 `root`
> - **腾讯云**：部分镜像默认用户名为 `ubuntu` 或 `centos`
> - **华为云**：部分镜像默认用户名为 `ubuntu` 或 `root`
> - **AWS**：默认用户名为 `ec2-user`（Amazon Linux）或 `ubuntu`（Ubuntu 镜像）
>
> 请根据您购买的云服务器型号和控制台提示，填写正确的用户名。如果不确定，可以查看云厂商的文档或购买时的邮件通知。

4. 连接成功则如图所示，如果返回上一界面可能是密码有误请重新输入

   接下来就可以输入指令对服务器进行操作了

   <a href="images/2026-02-24-22-08-44.png" target="_blank"> <img src="images/2026-02-24-22-08-44.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

#### 2.2.3. 特殊情况：非 root 用户获取 root 权限

> 💡 **仅当您的云服务器默认用户名不是 `root` 时，需要执行本节操作**
>
> 如果您在 WindTerm 中使用非 root 用户名（如 `ubuntu`、`centos` 等）成功登录，您会发现无法直接修改 `/etc/` 等系统目录。此时需要先启用 root 账户并设置密码。

1. **首次登录（使用默认用户名）**：

   假设您的默认用户名是 `ubuntu`，在 WindTerm 中填写：
   - 主机：您的服务器公网 IP
   - 端口：22（或云厂商指定的 SSH 端口）
   - 用户名：`ubuntu`（或其他默认用户名）
   - 密码：您在云服务器控制台设置的密码

2. **设置 root 密码**：

   登录成功后，执行以下命令设置 root 密码：

   ```bash
   sudo passwd root
   ```

   系统会提示您输入新密码：

   ```
   Enter new UNIX password:
   Retype new UNIX password:
   ```

   > 💡 **密码输入提示**：在终端输入密码时，**屏幕上不会显示任何字符**（包括星号或圆点），这是 Linux 的安全机制。如果您担心输错，可以：
   >
   > - 先在记事本或 QQ 等地方写好密码
   > - 复制密码
   > - 在终端中粘贴（右键点击终端窗口或按 Shift+Insert）
   > - 按回车确认

输入两次密码后，如果显示 `passwd: password updated successfully` 则表示设置成功。

<a href="images/2026-03-06-04-51-03.png" target="_blank"> <img src="images/2026-03-06-04-51-03.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

3. **重新建立会话（使用 root 用户）**：

   设置完 root 密码后，关闭当前会话（输入 `exit` 或直接关闭窗口），然后在 WindTerm 中重新建立会话：
   - 主机：您的服务器公网 IP
   - 端口：22
   - 用户名：`root`（现在可以改用 root 了）
   - 密码：刚才设置的 root 密码

   重新连接后，您就拥有了完整的 root 权限，可以继续后续的 OpenVPN 安装和配置了。

#### 2.2.3. 更新系统并安装所需软件

一次完成系统更新及 unzip、OpenVPN 的安装（解压服务端和运行 VPN 都需要）：

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y unzip openvpn
```

将鼠标移至文中代码框上方，点击“复制”按钮，然后回到终端右键粘贴并回车即可，后续操作同理。

<a href="images/2026-02-24-22-14-44.png" target="_blank"> <img src="images/2026-02-24-22-14-44.png" alt="image" style="max-width: 100%; width: 700px;"/> </a>

<a href="images/2026-02-24-22-17-25.png" target="_blank"> <img src="images/2026-02-24-22-17-25.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

输入以下命令并回车，即可重启服务器：

```bash
reboot
```

指令执行后再次按下回车，然后耐心等待片刻，待服务器自动重启并重新出现大量系统信息输出后，即表示重启已完成。

<a href="images/2026-02-24-22-24-44.png" target="_blank"> <img src="images/2026-02-24-22-24-44.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

#### 2.2.4. 版本检查（重要！）

安装完成后，输入以下命令查看版本，判断是否安装成功：

```bash
openvpn --version
```

<a href="images/2026-02-24-22-18-49.png" target="_blank"> <img src="images/2026-02-24-22-18-49.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

然后记住你的 openvpn 版本，会影响后面的操作步骤

### 2.3. 开放防火墙端口（关键步骤）

为了让游戏数据能顺利进出服务器，我们需要开放两个特定的端口：**3074 (UDP)** 和 **3075 (TCP)**。这通常涉及两道关卡：**服务器内部防火墙**和**云厂商安全组**。

#### 2.3.1. 第一关：服务器内部防火墙 (UFW)

Ubuntu 24.04 默认使用 **ufw** 作为防火墙前端。若未启用 ufw，端口默认可能未被限制；若已启用，需放行上述端口。

检查防火墙状态：

```bash
sudo ufw status
```

若显示 `Status: inactive`，说明防火墙未启用，可跳过本小节，直接配置 **云厂商安全组**。

<a href="images/2026-02-24-22-30-31.png" target="_blank"> <img src="images/2026-02-24-22-30-31.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

若显示 `Status: active`，请执行以下命令放行端口并重载。若尚未启用 ufw 但打算启用，可先执行 `sudo ufw enable`（提示时输入 y 确认），再执行下面的放行命令：

<a href="images/2026-02-24-22-32-06.png" target="_blank"> <img src="images/2026-02-24-22-32-06.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

放行 3074 (UDP) 和 3075 (TCP)：

```bash
sudo ufw allow 3074/udp
sudo ufw allow 3075/tcp
sudo ufw reload
```

验证是否成功：

```bash
sudo ufw status numbered
```

<a href="images/2026-02-24-22-32-46.png" target="_blank"> <img src="images/2026-02-24-22-32-46.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

若在规则列表中看到 3074/udp 和 3075/tcp，即代表操作成功。

#### 2.3.2. 第二关：云厂商安全组 (Security Group)

⚠️ **这是新手最容易忽略的一步！**

绝大多数云服务器（阿里云、腾讯云、华为云等）在网页控制台都有一层额外的 **「安全组」** 或 **「防火墙」** 设置。

请登录您的云服务器控制台，找到 **安全组 → 配置规则 → 手动添加**，填入以下信息：

<a href="images/2026-02-24-22-33-52.png" target="_blank"> <img src="images/2026-02-24-22-33-52.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

规则 1 (UDP)

- 协议类型：UDP
- 端口范围：3074/3074
- 授权对象：0.0.0.0/0（所有 IP）
- 策略：允许

规则 2 (TCP)

- 协议类型：TCP
- 端口范围：3075/3075
- 授权对象：0.0.0.0/0（所有 IP）
- 策略：允许

<a href="images/2026-02-24-22-34-25.png" target="_blank"> <img src="images/2026-02-24-22-34-25.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

### 2.4. 特殊情况：共享型 VPS 的端口转发（NAT 映射）

> ⚠️ **以下内容仅适用于购买了「超低价共享型 VPS」的用户，拥有独立公网 IP 的独立服务器用户可直接跳过本节。**

部分超低价 VPS 服务商并非给您一台独立的机器，而是**一台物理主机由多个用户共享**。在这种情况下，您拿到的并非一个独立的公网 IP，而是一个 **"IP: 端口"** 的访问入口（例如 `160.202.254.14:10272`），其中 `10272` 是您的 SSH 登录端口。

在这种架构下，**3074 和 3075 端口由宿主机的主网关统一管理，您没有权限直接对外暴露这两个端口**，因此客户端无法通过标准端口直接连接到您服务器内的 OpenVPN 服务。

**解决方案：在服务商管理面板中配置端口转发（NAT 映射）**

您的 VPS 服务商通常会在其控制面板中提供端口转发功能，可以将宿主机上一个分配给您的外部端口，映射到您虚拟机内部的指定端口。

**操作步骤如下：**

1. 登录您的 VPS 服务商管理面板，找到您的实例
2. 找到 **端口转发（NAT / Port Forwarding）** 或类似选项
3. 添加两条转发规则（外部端口由系统分配或您自行填写）：

| 内部端口（本机 OpenVPN） | 协议 | 外部端口（映射后对外暴露） |
| :----------------------: | :--: | :------------------------: |
|           3074           | UDP  |         例：40074          |
|           3075           | TCP  |         例：40075          |

<a href="images/2026-02-24-22-35-19.png" target="_blank"> <img src="images/2026-02-24-22-35-19.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

4. **记录下服务商分配给您的两个外部端口号**，在后续配置客户端时需要用到

> 💡 **注意**：内部防火墙（ufw）和云厂商安全组仍然需要开放 **3074（UDP）** 和 **3075（TCP）**，因为这是 OpenVPN 服务在您虚拟机内部实际监听的端口。端口转发规则是将外部流量"转进来"，服务本身不变。

## 3. 服务端文件部署与核心配置

在第一章准备好环境后，我们需要将加速器的"心脏"——服务端核心文件部署到服务器中。这一步看似简单，但文件路径的准确性和脚本的执行权限直接决定了后续服务能否启动。

首先，我们需要先从 [原作者博客](https://www.dogfight360.com/blog/1590/#comment-41142) 中下载关键文件 [教程 .zip](https://www.dogfight360.com/blog/wp-content/uploads/2021/07/%E6%95%99%E7%A8%8B.zip), 解压后从中提取出 server.zip

<a href="images/2026-02-24-22-43-14.png" target="_blank"> <img src="images/2026-02-24-22-43-14.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

### 3.1. 上传文件

在右侧文件资源管理器中，打开下拉框，点击第一个'/'

<a href="images/2026-02-24-22-39-46.png" target="_blank"> <img src="images/2026-02-24-22-39-46.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

然后进入 tmp 目录

<a href="images/2026-02-24-22-41-50.png" target="_blank"> <img src="images/2026-02-24-22-41-50.png" alt="image" style="max-width: 100%; width: 500px;"/> </a>

点击右上角三个点，选择上传文件到当前目录

<a href="images/2026-02-24-22-42-53.png" target="_blank"> <img src="images/2026-02-24-22-42-53.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

选择本章初解压获得的 server.zip 文件上传

<a href="images/2026-02-24-22-44-23.png" target="_blank"> <img src="images/2026-02-24-22-44-23.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

如图即上传成功

<a href="images/2026-02-24-22-46-02.png" target="_blank"> <img src="images/2026-02-24-22-46-02.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

### 3.2. 解压与部署

文件上传完成后，我们需要通过 SSH 终端将其解压到 OpenVPN 的标准配置目录中。

#### 3.2.1. 创建标准目录

为了规范化管理，我们统一将文件存放在 `/etc/openvpn` 目录下。输入以下命令创建目录（如果系统已自动创建，此命令会提示已存在，忽略即可）：

```bash
sudo mkdir -p /etc/openvpn
```

#### 3.2.2. 解压文件

输入以下命令，将刚才上传到临时目录的文件解压到配置目录：

```bash
sudo unzip /tmp/server.zip -d /etc/openvpn/
```

#### 3.2.3. 验证解压结果

解压完成后，我们要确认文件是否都在。输入以下命令查看目录内容：

```bash
ls -l /etc/openvpn/
```

请仔细核对输出结果，确保目录下包含以下关键文件：

- `server_tcp.conf` （TCP 配置文件）
- `server_udp.conf`（UDP 配置文件）
- `checkpsw.sh` （密码验证脚本）
- `psw-file` （账号密码文件）

<a href="images/2026-02-24-22-48-40.png" target="_blank"> <img src="images/2026-02-24-22-48-40.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

### 3.3. 关键步骤：赋予执行权限

⚠️ **这是最容易被新手忽略的一步！**

`checkpsw.sh` 是一个 Shell 脚本，OpenVPN 需要调用它来验证客户端传来的账号密码。如果它没有 **「可执行权限」**，服务器就会 **拒绝所有连接请求**，导致报错。

#### 3.3.1. 赋予权限

输入以下命令，将脚本标记为可执行文件：

```bash
sudo chmod +x /etc/openvpn/checkpsw.sh
```

#### 3.3.2. 再次验证

再次输入查看命令：

```bash
ls -l /etc/openvpn/checkpsw.sh
```

观察输出结果的第一个字段：

- 如果显示 `-rwxr-xr-x` （包含 `x` 且文件名通常变绿），说明权限设置成功。
- 如果显示 `-rw-r--r--` （没有 `x`)，说明失败，请重新执行 `chmod` 命令。

<a href="images/2026-02-24-22-49-26.png" target="_blank"> <img src="images/2026-02-24-22-49-26.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

---

至此，所有的文件都已就位，且具备了运行条件。下一章我们将进入最核心、也最复杂的环节：修改配置文件以适配群星的低延迟需求及新版系统的兼容性。

## 4. 核心配置与版本兼容性修正

文件部署完成后，我们需要对 OpenVPN 的配置文件进行"手术"。本章的核心目标是：关闭加密以降低延迟，并修正新旧版本的语法差异。

首先，在左侧文件管理器中按照路径/etc/openvpn/找到 OpenVPN 的配置文件目录：

<a href="images/2026-02-24-22-53-53.png" target="_blank"> <img src="images/2026-02-24-22-53-53.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

### 4.1. 修改 TCP 配置文件

#### 4.1.1. 打开 tcp 文件

双击打开 server_tcp.conf，如果让你选择打开方式，选择记事本即可：

<a href="images/2026-02-24-22-55-52.png" target="_blank"> <img src="images/2026-02-24-22-55-52.png" alt="image" style="max-width: 100%; width: 700px;"/> </a>

#### 4.1.2. 编辑 tcp 指南

> **注意：以下为新版 OpenVPN 关键配置语法变更！**

请注意：不同 OpenVPN 版本所需的修改各不相同。如果忘记自己的 OpenVPN 版本，请返回前文“版本检查（重要！）”部分重新确认。

- 如果你的 OpenVPN 版本为 **2.5.x**，只需**将 `cipher none` 替换为 `data-ciphers none`**（这样可避免加密兼容性及报错问题）。
- 如果你的 OpenVPN 版本为 **2.6.x 及以上**，除了**将 `cipher none` 换为 `data-ciphers none`**，还要**把 `client-cert-not-required` 替换为 `verify-client-cert none`**（否则服务将无法启动）。

请根据你的实际版本，按需修改对应条目，确保配置兼容并能顺利启动。

<a href="images/2026-02-24-23-07-20.png" target="_blank"> <img src="images/2026-02-24-23-07-20.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

然后！记得 ctrl+S 保存，会弹出弹窗让你将文件上传回服务器，点击是

<a href="images/2026-02-24-23-08-09.png" target="_blank"> <img src="images/2026-02-24-23-08-09.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

### 4.2. 修改 UDP 配置文件

于上文修改 tcp 文件同理，不再赘述

<a href="images/2026-02-24-23-12-55.png" target="_blank"> <img src="images/2026-02-24-23-12-55.png" alt="image" style="max-width: 100%; width: 700px;"/> </a>

<a href="images/2026-02-24-23-12-40.png" target="_blank"> <img src="images/2026-02-24-23-12-40.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

### 4.3. 设置连接账号密码

最后，我们需要配置 psw-file 账号密码文件。客户端连接时必须填写这里设置的内容。

#### 4.3.1. 打开密码文件

双击打开 psw-file

<a href="images/2026-02-24-23-14-24.png" target="_blank"> <img src="images/2026-02-24-23-14-24.png" alt="image" style="max-width: 100%; width: 700px;"/> </a>

#### 4.3.2. 设置账号

文件内容的格式非常简单：用户名 空格 密码。
您可以删除原有的默认内容，填入您自己的账号。

示例（设置用户名为 stellaris，密码为 123456）：

```text
stellaris 123456
```

<a href="images/2026-02-24-23-15-35.png" target="_blank"> <img src="images/2026-02-24-23-15-35.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

然后 Ctrl+S 保存并上传文件

至此，配置文件的修改工作全部完成。下一章我们将尝试启动服务，并教您如何看懂启动日志来验证修改是否成功。

## 5. 服务启动验证与自动化部署

配置文件的修改只是纸上谈兵，我们需要通过实际运行来验证服务能否启动。如果配置文件有语法错误（例如 OpenVPN 版本不兼容），在这一步就会暴露出来。确认无误后，我们将配置开机自启。

### 5.1. 手动启动测试

在后台静默运行之前，我们先在前台手动启动一次，以便直观地看到启动日志。

#### 5.1.1. 测试 TCP 服务

在 Ubuntu 中 OpenVPN 一般位于 `/usr/sbin/openvpn`（不确定可执行 `which openvpn` 查看）。

<a href="images/2026-02-24-23-17-03.png" target="_blank"> <img src="images/2026-02-24-23-17-03.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

直接启动 TCP 服务端：

```bash
sudo /usr/sbin/openvpn --cd /etc/openvpn/ --config server_tcp.conf
```

<a href="images/2026-02-24-23-17-42.png" target="_blank"> <img src="images/2026-02-24-23-17-42.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

#### 5.1.2. 观察启动日志

终端会输出一长串日志。请耐心观察最后一行：

- ✅ 如果显示 **`Initialization Sequence Completed`**，说明 TCP 服务启动成功，配置文件无误。
- ❌ 如果显示 **`Exiting due to fatal error`** 或其他报错，请仔细检查报错信息（通常是 `cipher` 或 `auth` 参数写错了），并返回上一章重新修改。

确认成功后，按 `Ctrl + C` 停止服务。

#### 5.1.3. 测试 UDP 服务

重复上述步骤，测试 UDP 配置文件：

```bash
sudo /usr/sbin/openvpn --cd /etc/openvpn/ --config server_udp.conf
```

<a href="images/2026-02-24-23-19-53.png" target="_blank"> <img src="images/2026-02-24-23-19-53.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

同样等待出现 **`Initialization Sequence Completed`** 后，按 `Ctrl + C` 停止。

### 5.2. 配置开机自启动

为了让加速器在服务器重启后自动运行，我们使用 **systemd** 创建两个服务单元。

下列指令直接复制粘贴后回车即可

#### 5.2.1. 创建 TCP 服务单元

```bash
sudo tee /etc/systemd/system/openvpn-stellaris-tcp.service << 'EOF'
[Unit]
Description=OpenVPN Stellaris TCP
After=network.target

[Service]
Type=simple
ExecStart=/usr/sbin/openvpn --cd /etc/openvpn/ --config server_tcp.conf
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
```

<a href="images/2026-02-24-23-22-52.png" target="_blank"> <img src="images/2026-02-24-23-22-52.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

#### 5.2.2. 创建 UDP 服务单元

```bash
sudo tee /etc/systemd/system/openvpn-stellaris-udp.service << 'EOF'
[Unit]
Description=OpenVPN Stellaris UDP
After=network.target

[Service]
Type=simple
ExecStart=/usr/sbin/openvpn --cd /etc/openvpn/ --config server_udp.conf
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
```

<a href="images/2026-02-24-23-23-22.png" target="_blank"> <img src="images/2026-02-24-23-23-22.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

#### 5.2.3. 启用并启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable openvpn-stellaris-tcp openvpn-stellaris-udp
sudo systemctl start openvpn-stellaris-tcp openvpn-stellaris-udp
```

<a href="images/2026-02-24-23-26-05.png" target="_blank"> <img src="images/2026-02-24-23-26-05.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

检查状态（应均为 active (running)）：

```bash
sudo systemctl status openvpn-stellaris-tcp openvpn-stellaris-udp
```

<a href="images/2026-02-24-23-27-46.png" target="_blank"> <img src="images/2026-02-24-23-27-46.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

> 💡 **提示**：查看完服务状态后，按 `Ctrl + C` 即可退出浏览模式，返回命令行提示符。

### 5.3. 可选：重启验证

若想确认开机自启是否生效，可重启服务器后再检查端口（非必须，上面 `systemctl status` 正常即可）。

#### 5.3.1. 重启服务器

```bash
sudo reboot
```

SSH 会断开，按回车等待 1～2 分钟后重新连接。

#### 5.3.2. 验证端口监听状态

重新连接后执行：

```bash
ss -ulnp | grep 3074
ss -tlnp | grep 3075
```

#### 5.3.3. 确认结果

观察输出结果：

- 若 UDP 3074 和 TCP 3075 均有对应进程在监听，说明加速器已成功在后台自动运行，服务端部署完成。

<a href="images/2026-02-24-23-29-15.png" target="_blank"> <img src="images/2026-02-24-23-29-15.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

## 6. 客户端深度配置与联机实测

服务端配置圆满结束后，最后一步就是配置玩家手中的客户端。本方案使用的是 **UsbEAm LAN Party**，它小巧免安装，通过 TAP 虚拟网卡技术组建虚拟局域网，非常适合群星这种 P2P 联机游戏。

### 6.1. 下载与安装

我们需要准备客户端程序和虚拟网卡驱动。

#### 6.1.1. 获取软件

请前往原作者 Dogfight360 的博客下载最新版客户端（通常名为 UsbEAm_LAN_Party_V1.x.zip）：

> <https://www.dogfight360.com/blog/1590/>

<a href="images/2026-02-24-23-33-53.png" target="_blank"> <img src="images/2026-02-24-23-33-53.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

下载完成后解压，解压密码 dogfight360，解压后，您应该会看到以下三个核心文件：

- UsbEAm LAN Party V1.2.exe（客户端主程序）
- tap-windows-9.9.2_3.exe（虚拟网卡驱动安装包）
- customize.ini（节点配置文件）

<a href="images/2026-02-24-23-35-06.png" target="_blank"> <img src="images/2026-02-24-23-35-06.png" alt="image" style="max-width: 100%; width: 700px;"/> </a>

#### 6.1.2. 安装 TAP 驱动

如果是第一次使用该软件，必须安装 TAP 驱动，否则无法建立虚拟局域网。

1. 双击运行 tap-windows-9.9.2_3.exe。
2. 一路点击 Next（下一步）直到安装完成。
3. 注意：安装过程中无需更改任何默认设置。

<a href="images/2026-02-24-23-35-23.png" target="_blank"> <img src="images/2026-02-24-23-35-23.png" alt="image" style="max-width: 100%; width: 700px;"/> </a>

### 6.2. 配置节点信息

我们需要修改 customize.ini 文件，将我们服务器的信息填进去，让客户端知道去哪里连接。

#### 6.2.1. 编辑配置文件

双击选择用记事本打开 customize.ini，清空里面的内容，或者直接修改为以下标准格式：

<a href="images/2026-02-24-23-37-55.png" target="_blank"> <img src="images/2026-02-24-23-37-55.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

```ini
[usbeam]
Server_List=我的群星节点
Disable_rules=1
Broadcast_fix=1

[我的群星节点]
IP=203.0.113.1
TCP_Port=3075
UDP_Port=3074
USER=stellaris
PASS=123456
```

#### 6.2.2. 参数详解（请务必核对）

- **Server List**：这里填的名字会显示在软件下拉菜单里
- **[我的群星节点]**：中括号里的名字必须与 `Server List` 保持一致
- **IP**：改为您服务器的 **公网 IP**（示例中的 203.0.113.1 仅为占位）。若为共享型 VPS，只填 IP，不要带端口号。
- **TCP Port / UDP Port**：默认填写 `3075` 和 `3074`。**如果您使用的是共享型 VPS**，请填写您在服务商管理面板中配置的端口转发规则里对应的**外部端口号**（详见上方"特殊情况：共享型 VPS 的端口转发"一节）
- **USER**：修改为您在 `psw-file` 里设置的 **用户名**
- **PASS**：修改为您在 `psw-file` 里设置的 **密码**
- **Disable rules=1**：代表默认勾选「不使用安全规则」
- **Broadcast fix=1**：代表默认勾选「修正广播优先级」

修改完成后，保存并关闭文件。

### 6.3. 启动连接与测试

万事俱备，只欠东风。

#### 6.3.1. 启动客户端

双击运行 UsbEAm LAN Party V1.2.exe。

<a href="images/2026-02-24-23-39-01.png" target="_blank"> <img src="images/2026-02-24-23-39-01.png" alt="image" style="max-width: 100%; width: 1000px;"/> </a>

#### 6.3.2. 选择节点

在软件界面的下拉框中，找到我们刚才在配置文件里命名的节点（例如"我的群星节点"）。

<a href="images/2026-02-24-23-50-46.png" target="_blank"> <img src="images/2026-02-24-23-50-46.png" alt="image" style="max-width: 100%; width: 400px;"/> </a>

#### 6.3.3. 选择模式（关键！）

在连接按钮的左侧或下方，通常有模式选择。
⚠️ **请务必勾选 UDP 模式**。

> 💡 群星联机对延迟极其敏感，**UDP 模式去除了 TCP 的握手重传机制**，能显著降低延迟，是本教程的核心优势所在。

<a href="images/2026-02-24-23-51-04.png" target="_blank"> <img src="images/2026-02-24-23-51-04.png" alt="image" style="max-width: 100%; width: 400px;"/> </a>

#### 6.3.4. 点击连接

点击 **连接** 按钮。

- 观察软件底部的状态栏
- ✅ 如果显示 **「连接状态：正常 (xx ms)」**，恭喜您！节点搭建成功
- ❌ 如果一直卡在「正在连接」，请检查：
  - 防火墙端口是否正确开放（第一章）
  - 账号密码是否填写正确（上一章）
  - 服务端是否正常运行

当所有小伙伴都显示 **「连接状态：正常」** 后，大家实际上已经处于同一个虚拟局域网中。

<a href="images/2026-02-24-23-51-54.png" target="_blank"> <img src="images/2026-02-24-23-51-54.png" alt="image" style="max-width: 100%; width: 400px;"/> </a>

## 7. 总结

🎉 至此，您的专属群星联机加速节点已部署完毕！

**使用方法**：

1. 所有玩家启动 UsbEAm LAN Party 客户端
2. 连接到同一节点
3. 确认状态显示「正常」
4. 直接进入游戏，享受低延迟的联机体验！

祝各位征途愉快！🚀
