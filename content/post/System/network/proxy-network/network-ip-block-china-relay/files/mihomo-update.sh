#!/bin/bash
# mihomo-update.sh —— 自动拉取机场订阅并更新中转机 mihomo 配置
# 配合 crontab 使用：0 */6 * * * /etc/mihomo/mihomo-update.sh
# 修改成你自己的机场订阅链接
URL="https://sub3.smallstrawberry.com/api/v1/client/subscribe?token=YOUR_TOKEN"

# 用 Clash 的 UA 拉取，机场才会返回 yaml（mihomo UA 会返回 base64）
curl -s -A "clash-verge-rev/v2.5.1" --max-time 30 -o /tmp/sub.yaml "$URL"

python3 /etc/mihomo/gen_config.py /tmp/sub.yaml /etc/mihomo/config.yaml.new

if [ -s /etc/mihomo/config.yaml.new ]; then
  if ! diff -q /etc/mihomo/config.yaml /etc/mihomo/config.yaml.new >/dev/null 2>&1; then
    mv /etc/mihomo/config.yaml.new /etc/mihomo/config.yaml
    systemctl restart mihomo
  fi
fi