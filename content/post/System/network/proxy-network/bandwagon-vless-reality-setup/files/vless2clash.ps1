#requires -Version 5.1
<#
.SYNOPSIS
    把 vless:// 链接转换成 Clash Verge / Mihomo 完整 yaml 配置
    粘贴一个 vless:// 链接，生成对应配置文件
.EXAMPLE
    powershell -ExecutionPolicy Bypass -File .\vless2clash.ps1
.EXAMPLE
    .\vless2clash.ps1 -Link "vless://..." -Link "vless://..."
#>
param(
    [string[]]$Link
)

$ErrorActionPreference = "Stop"

function ConvertTo-ClashYaml {
    param([string]$RawLink)

    $RawLink = $RawLink.Trim()
    if (-not $RawLink.StartsWith("vless://")) {
        throw "只支持 vless:// 开头的链接：$($RawLink.Substring(0, [Math]::Min(40, $RawLink.Length)))..."
    }

    # 提取 #节点名
    $nodeName = ""
    $hashIdx = $RawLink.IndexOf("#")
    if ($hashIdx -ge 0) {
        $nodeName = [System.Uri]::UnescapeDataString($RawLink.Substring($hashIdx + 1))
        $RawLink = $RawLink.Substring(0, $hashIdx)
    }

    # 去掉 vless:// 前缀
    $rest = $RawLink.Substring("vless://".Length)

    # 拆 uuid@host:port
    $atIdx = $rest.LastIndexOf("@")
    if ($atIdx -lt 0) { throw "链接格式错误：缺少 @" }
    $uuid = $rest.Substring(0, $atIdx)
    $hostport = $rest.Substring($atIdx + 1)

    # 拆 query
    $query = @{}
    $qIdx = $hostport.IndexOf("?")
    if ($qIdx -ge 0) {
        $qs = $hostport.Substring($qIdx + 1)
        $hostport = $hostport.Substring(0, $qIdx)
        foreach ($pair in $qs.Split("&")) {
            if ([string]::IsNullOrEmpty($pair)) { continue }
            $kv = $pair.Split("=", 2)
            $k = [System.Uri]::UnescapeDataString($kv[0])
            $v = ""
            if ($kv.Length -gt 1) { $v = [System.Uri]::UnescapeDataString($kv[1]) }
            if (-not $query.ContainsKey($k)) { $query[$k] = $v }
        }
    }

    # 拆 host:port
    if ($hostport.StartsWith("[")) {
        $close = $hostport.IndexOf("]")
        if ($close -lt 0) { throw "链接格式错误：IPv6 地址缺少 ]" }
        $serverAddr = $hostport.Substring(1, $close - 1)
        $portStr = $hostport.Substring($close + 1).TrimStart(":")
    } else {
        $colonIdx = $hostport.LastIndexOf(":")
        if ($colonIdx -lt 0) { throw "链接格式错误：缺少端口" }
        $serverAddr = $hostport.Substring(0, $colonIdx)
        $portStr = $hostport.Substring($colonIdx + 1)
    }

    $port = 0
    if (-not [int]::TryParse($portStr, [ref]$port)) { throw "链接格式错误：端口不是数字 ($portStr)" }

    function Get-Q([string]$key, [string]$default = "") {
        if ($query.ContainsKey($key) -and $query[$key]) { return $query[$key] }
        return $default
    }

    if ([string]::IsNullOrWhiteSpace($nodeName)) { $nodeName = "Node-$serverAddr" }

    $security = Get-Q "security"
    $network  = Get-Q "type" "tcp"
    $flow     = Get-Q "flow"

    $proxy = [ordered]@{
        name    = $nodeName
        type    = "vless"
        server  = $serverAddr
        port    = $port
        uuid    = $uuid
        network = $network
        tls     = ($security -in @("reality", "tls", "xtls"))
        udp     = $true
    }
    if ($flow) { $proxy.flow = $flow }

    if ($security -eq "reality") {
        $pbk = Get-Q "pbk"
        if (-not $pbk) { throw "链接缺少 pbk（Reality 公钥）" }
        $proxy.servername = Get-Q "sni" $serverAddr
        $proxy."client-fingerprint" = Get-Q "fp" "chrome"
        $proxy."reality-opts" = [ordered]@{
            "public-key" = $pbk
            "short-id"   = Get-Q "sid"
        }
    } elseif ($security -eq "tls") {
        $proxy.servername = Get-Q "sni" $serverAddr
        $fp = Get-Q "fp"
        if ($fp) { $proxy."client-fingerprint" = $fp }
        $insecure = Get-Q "allowInsecure"
        if ($insecure -in @("1", "true")) { $proxy."skip-cert-verify" = $true }
    }

    switch ($network) {
        "ws" {
            $ws = [ordered]@{}
            $path = Get-Q "path"
            $hostH = Get-Q "host"
            if ($path) { $ws.path = $path }
            if ($hostH) { $ws.headers = [ordered]@{ Host = $hostH } }
            if ($ws.Count -gt 0) { $proxy."ws-opts" = $ws }
        }
        "grpc" {
            $svc = Get-Q "serviceName"
            if ($svc) { $proxy."grpc-opts" = [ordered]@{ "grpc-service-name" = $svc } }
        }
        "h2" {
            $p = Get-Q "path"
            if ($p) { $proxy."h2-opts" = [ordered]@{ path = $p } }
        }
        "httpupgrade" {
            $p = Get-Q "path"
            if ($p) { $proxy."httpupgrade-opts" = [ordered]@{ path = $p } }
        }
        "xhttp" {
            $xh = [ordered]@{}
            $p = Get-Q "path"
            $m = Get-Q "mode"
            if ($p) { $xh.path = $p }
            if ($m) { $xh.mode = $m }
            $dl = [ordered]@{}
            $dp = Get-Q "downloadPath"
            $ds = Get-Q "downloadServer"
            $dpt = Get-Q "downloadPort"
            $dsn = Get-Q "downloadServername"
            if ($dp) { $dl.path = $dp }
            if ($ds) { $dl.server = $ds }
            if ($dpt) { $dl.port = [int]$dpt }
            if ($dsn) { $dl.servername = $dsn }
            if ($dl.Count -gt 0) { $xh."download-settings" = $dl }
            if ($xh.Count -gt 0) { $proxy."xhttp-opts" = $xh }
        }
    }

    return $proxy
}

function Write-YamlLine {
    param($Sb, [string]$Prefix, [string]$Key, $Value)
    if ($null -eq $Value -or $Value -eq "") {
        [void]$Sb.AppendLine("$Prefix$Key`": `"`"")
    } elseif ($Value -is [bool]) {
        [void]$Sb.AppendLine("$Prefix$Key`: $($Value.ToString().ToLower())")
    } else {
        $s = [string]$Value
        $needsQuote = ($s -match '[:#{}[\]&*!|>%@`"''\s]')
        if ($needsQuote) {
            $esc = $s.Replace('"', '\"')
            [void]$Sb.AppendLine("$Prefix$Key`: `"$esc`"")
        } else {
            [void]$Sb.AppendLine("$Prefix$Key`: $s")
        }
    }
}

function Write-YamlObject {
    param($Sb, $Obj, [int]$Indent, [switch]$AsListItem)
    $i = 0
    foreach ($key in $Obj.Keys) {
        $val = $Obj[$key]
        if ($AsListItem -and $i -eq 0) {
            $pad = ("  " * $Indent) + "- "
            $keyLevel = $Indent
        } elseif ($AsListItem) {
            $pad = "  " * ($Indent + 1)
            $keyLevel = $Indent + 1
        } else {
            $pad = "  " * $Indent
            $keyLevel = $Indent
        }
        if ($val -is [System.Collections.IDictionary]) {
            [void]$Sb.AppendLine("$pad${key}:")
            Write-YamlObject -Sb $Sb -Obj $val -Indent ($keyLevel + 1)
        } else {
            Write-YamlLine -Sb $Sb -Prefix $pad -Key $key -Value $val
        }
        $i++
    }
}

function Build-FullYaml {
    param($Proxies)
    $sb = New-Object System.Text.StringBuilder
    [void]$sb.AppendLine("# ==================================================")
    [void]$sb.AppendLine("# 极简智能版 Clash Meta 配置 (vless2clash 生成)")
    [void]$sb.AppendLine("# 支持 VLESS + Reality / TLS / WS / gRPC 等")
    [void]$sb.AppendLine("# ==================================================")
    [void]$sb.AppendLine("port: 7890")
    [void]$sb.AppendLine("socks-port: 7891")
    [void]$sb.AppendLine("allow-lan: true")
    [void]$sb.AppendLine("mode: rule")
    [void]$sb.AppendLine("log-level: info")
    [void]$sb.AppendLine("external-controller: :9090")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("# 🧠 远程规则集（Loyalsoldier 维护，每天自动更新一次）")
    [void]$sb.AppendLine("rule-providers:")
    [void]$sb.AppendLine("  google:")
    [void]$sb.AppendLine("    type: http")
    [void]$sb.AppendLine("    behavior: domain")
    [void]$sb.AppendLine('    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/google.txt"')
    [void]$sb.AppendLine("    path: ./ruleset/google.yaml")
    [void]$sb.AppendLine("    interval: 86400")
    [void]$sb.AppendLine("  proxy:")
    [void]$sb.AppendLine("    type: http")
    [void]$sb.AppendLine("    behavior: domain")
    [void]$sb.AppendLine('    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/proxy.txt"')
    [void]$sb.AppendLine("    path: ./ruleset/proxy.yaml")
    [void]$sb.AppendLine("    interval: 86400")
    [void]$sb.AppendLine("  direct:")
    [void]$sb.AppendLine("    type: http")
    [void]$sb.AppendLine("    behavior: domain")
    [void]$sb.AppendLine('    url: "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/direct.txt"')
    [void]$sb.AppendLine("    path: ./ruleset/direct.yaml")
    [void]$sb.AppendLine("    interval: 86400")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("proxies:")
    foreach ($p in $Proxies) {
        Write-YamlObject -Sb $sb -Obj $p -Indent 1 -AsListItem
    }
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("proxy-groups:")
    [void]$sb.AppendLine('  - name: "节点选择"')
    [void]$sb.AppendLine("    type: select")
    [void]$sb.AppendLine("    proxies:")
    foreach ($p in $Proxies) {
        [void]$sb.AppendLine("      - `"$($p.name)`"")
    }
    [void]$sb.AppendLine("      - DIRECT")
    [void]$sb.AppendLine("")
    [void]$sb.AppendLine("# 🚦 规则优先级（从上到下匹配）")
    [void]$sb.AppendLine("rules:")
    [void]$sb.AppendLine('  - RULE-SET,google,节点选择 # 谷歌服务')
    [void]$sb.AppendLine('  - RULE-SET,proxy,节点选择 # 墙外常用')
    [void]$sb.AppendLine('  - RULE-SET,direct,DIRECT # 墙内常用')
    [void]$sb.AppendLine('  - GEOIP,CN,DIRECT # 中国 IP 直连')
    [void]$sb.AppendLine('  - MATCH,节点选择 # 剩下的全部走节点')
    return $sb.ToString()
}

# ===== 主流程 =====
Write-Host ("=" * 56)
Write-Host "  vless:// 链接 -> Clash Verge / Mihomo yaml 转换器"

Write-Host ("=" * 56)

$links = @()
if ($Link -and $Link.Count -gt 0 -and -not [string]::IsNullOrWhiteSpace($Link[0])) {
    $links = @($Link)
} else {
    Write-Host "请粘贴 vless:// 链接，然后按回车："
    $line = ""
    while ([string]::IsNullOrWhiteSpace($line)) {
        $line = Read-Host
    }
    $links = @($line.Trim())
}

if ($links.Count -eq 0) {
    Write-Host "[错误] 没有输入任何链接" -ForegroundColor Red
    exit 1
}

$proxies = @()
$used = @{}
foreach ($link in $links) {
    try {
        $proxy = ConvertTo-ClashYaml -RawLink $link
    } catch {
        Write-Host "[错误] 解析失败：$($_.Exception.Message)" -ForegroundColor Red
        exit 1
    }
    $name = $proxy.name
    if ($used.ContainsKey($name)) {
        $used[$name]++
        $proxy.name = "$name-$($used[$name])"
    } else {
        $used[$name] = 1
    }
    $proxies += $proxy
}

$yamlText = Build-FullYaml -Proxies $proxies

Write-Host ""
Write-Host ("=" * 56)
Write-Host "生成的配置（共 $($proxies.Count) 个节点）："
Write-Host ("=" * 56)
Write-Host $yamlText

if ($proxies.Count -eq 1) {
    $outName = $proxies[0].name -replace '[\\/:*?"<>|]', "_"
    if ([string]::IsNullOrWhiteSpace($outName)) { $outName = "MyVPN" }
} else {
    $outName = "clash-config"
}
$outFile = Join-Path (Get-Location) "$outName.yaml"
[System.IO.File]::WriteAllText($outFile, $yamlText, (New-Object System.Text.UTF8Encoding($false)))
Write-Host ""
Write-Host "[完成] 已保存到：$outFile" -ForegroundColor Green
