#!/bin/bash
# frp-install.sh —— 下载并安装 frps/frpc（Linux amd64）
# 用法：bash frp-install.sh [版本号]   默认 0.63.0
set -e
VER=${1:-0.63.0}
cd /tmp
echo "下载 frp v${VER} ..."
curl -L --retry 10 --retry-all-errors --retry-delay 3 -o frp.tar.gz \
  "https://github.com/fatedier/frp/releases/download/v${VER}/frp_${VER}_linux_amd64.tar.gz"
gzip -t frp.tar.gz && echo "下载完整" || { echo "下载失败，请重试"; exit 1; }
tar -xzf frp.tar.gz
cp "frp_${VER}_linux_amd64/frps" /usr/local/bin/frps
cp "frp_${VER}_linux_amd64/frpc" /usr/local/bin/frpc
chmod +x /usr/local/bin/frps /usr/local/bin/frpc
mkdir -p /etc/frp
echo "安装完成："
frps -v
frpc -v