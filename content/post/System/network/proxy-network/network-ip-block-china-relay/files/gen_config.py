#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gen_config.py —— 从机场 Clash 订阅(yaml) 生成中转机 mihomo 配置
用法：
    python3 gen_config.py 订阅文件.yaml 输出文件.yaml
说明：
    只提取 vless + xhttp 节点（机场通常用 xhttp）；
    生成 url-test 自动选择 + PROXY 手动组；
    健康检查用 Cloudflare（比 gstatic 更中立）。
"""
import yaml, sys

HEALTH_URL = "https://cp.cloudflare.com/generate_204"
AUTH = "relay:CHANGE_ME_PASSWORD"   # ← 改成你自己的中转机密码

def quote(s):
    s = str(s)
    if any(ch in s for ch in ':#{}[]&*!|>%@`"\'') or s != s.strip():
        return '"' + s.replace('"', '\\"') + '"'
    return s

def main():
    if len(sys.argv) < 3:
        print("用法: python3 gen_config.py <订阅yaml> <输出yaml>")
        sys.exit(1)
    sub_path, out_path = sys.argv[1], sys.argv[2]
    with open(sub_path, encoding='utf-8') as f:
        data = yaml.safe_load(f)

    nodes = []
    for p in data.get('proxies', []):
        if p.get('type') != 'vless' or p.get('network') != 'xhttp':
            continue
        server = str(p.get('server', ''))
        if server.startswith('0.0.0.0'):
            continue
        xo = p.get('xhttp-opts', {}) or {}
        dl = xo.get('download-settings') or {}
        nodes.append({
            'name': p.get('name', server),
            'server': server,
            'port': int(p.get('port', 443)),
            'uuid': p.get('uuid', ''),
            'servername': p.get('servername', 'update.microsoft.com'),
            'path': xo.get('path', '/path'),
            'mode': xo.get('mode', 'stream-up'),
            'dl_path': dl.get('path', '/path'),
            'dl_server': dl.get('server', server),
            'dl_port': int(dl.get('port', 443)),
            'dl_servername': dl.get('servername', 'update.microsoft.com'),
        })

    lines = []
    lines.append('mixed-port: 7890')
    lines.append('allow-lan: true')
    lines.append("bind-address: '*'")
    lines.append('mode: rule')
    lines.append('log-level: info')
    lines.append('authentication:')
    lines.append('  - %s' % quote(AUTH))
    lines.append('proxies:')
    for n in nodes:
        lines.append('  - name: %s' % quote(n['name']))
        lines.append('    type: vless')
        lines.append('    server: %s' % n['server'])
        lines.append('    port: %s' % n['port'])
        lines.append('    uuid: %s' % n['uuid'])
        lines.append('    network: xhttp')
        lines.append('    tls: true')
        lines.append('    udp: true')
        lines.append('    skip-cert-verify: true')
        lines.append('    servername: %s' % n['servername'])
        lines.append('    xhttp-opts:')
        lines.append('      path: %s' % quote(n['path']))
        lines.append('      mode: %s' % quote(n['mode']))
        lines.append('      download-settings:')
        lines.append('        path: %s' % quote(n['dl_path']))
        lines.append('        server: %s' % n['dl_server'])
        lines.append('        port: %s' % n['dl_port'])
        lines.append('        servername: %s' % n['dl_servername'])
    lines.append('proxy-groups:')
    lines.append('  - name: "自动选择"')
    lines.append('    type: url-test')
    lines.append('    url: %s' % HEALTH_URL)
    lines.append('    interval: 300')
    lines.append('    proxies:')
    for n in nodes:
        lines.append('      - %s' % quote(n['name']))
    lines.append('  - name: "PROXY"')
    lines.append('    type: select')
    lines.append('    proxies:')
    lines.append('      - "自动选择"')
    lines.append('      - DIRECT')
    lines.append('rules:')
    lines.append('  - MATCH,PROXY')

    with open(out_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(lines))
    print('生成节点数:', len(nodes))
    print('输出:', out_path)

if __name__ == '__main__':
    main()