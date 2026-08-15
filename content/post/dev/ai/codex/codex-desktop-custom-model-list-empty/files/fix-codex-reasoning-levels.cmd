@echo off
chcp 65001 >nul
title Codex 推理档位一键修复
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$self=[IO.File]::ReadAllText('%~f0',[Text.Encoding]::UTF8); $marker='__CODEX_POWERSHELL_PAYLOAD__'; $script=$self.Substring($self.LastIndexOf($marker)+$marker.Length).TrimStart([char]13,[char]10); $params=@{Preset='Standard';DefaultEffort='medium';NoRestartPrompt=$true}; if($env:CODEX_REASONING_CONFIG_PATH){$params.ConfigPath=$env:CODEX_REASONING_CONFIG_PATH}; & ([ScriptBlock]::Create($script)) @params"
set "RESULT=%ERRORLEVEL%"
echo.
if not "%RESULT%"=="0" (
  echo 修复失败，请查看上方错误信息。
) else (
  echo 操作已完成。请完全退出 Codex Desktop 后重新启动。
)
echo.
pause
exit /b %RESULT%

__CODEX_POWERSHELL_PAYLOAD__
[CmdletBinding(SupportsShouldProcess = $true)]
param(
    [ValidateSet('Standard', 'Extended', 'Binary')]
    [string]$Preset = 'Standard',

    [ValidateSet('low', 'medium', 'high', 'xhigh', 'max', 'ultra')]
    [string]$DefaultEffort = 'medium',

    [string]$ConfigPath = (Join-Path $HOME '.codex\config.toml'),

    [switch]$LockCatalog,
    [switch]$UnlockCatalog,
    [switch]$UnlockOnly,
    [switch]$NoConfigUpdate,
    [switch]$NoRestartPrompt
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function Write-Step([string]$Message) {
    Write-Host "[Codex 推理档位修复] $Message" -ForegroundColor Cyan
}

function Resolve-FullPath([string]$Path, [string]$BaseDirectory) {
    if ([System.IO.Path]::IsPathRooted($Path)) {
        return [System.IO.Path]::GetFullPath($Path)
    }
    return [System.IO.Path]::GetFullPath((Join-Path $BaseDirectory $Path))
}

function Get-CatalogPath([string]$TomlPath) {
    if (-not (Test-Path -LiteralPath $TomlPath -PathType Leaf)) {
        throw "找不到 Codex 配置文件：$TomlPath"
    }

    $toml = [System.IO.File]::ReadAllText($TomlPath, [System.Text.Encoding]::UTF8)
    $match = [regex]::Match(
        $toml,
        '(?m)^\s*model_catalog_json\s*=\s*["''](?<path>[^"'']+)["'']\s*(?:#.*)?$'
    )

    if (-not $match.Success) {
        throw "在 $TomlPath 中没有找到 model_catalog_json 配置。请先让 ccSwitch 写入集成官方路由配置。"
    }

    return Resolve-FullPath -Path $match.Groups['path'].Value -BaseDirectory (Split-Path -Parent $TomlPath)
}

function Get-ReasoningLevels([string]$Name) {
    switch ($Name) {
        'Binary' {
            return @(
                [ordered]@{ description = 'Disable reasoning'; effort = 'none' },
                [ordered]@{ description = 'Enable reasoning'; effort = 'high' }
            )
        }
        'Extended' {
            return @(
                [ordered]@{ description = 'Fast responses with lighter reasoning'; effort = 'low' },
                [ordered]@{ description = 'Balanced speed and reasoning depth'; effort = 'medium' },
                [ordered]@{ description = 'Greater reasoning depth for complex tasks'; effort = 'high' },
                [ordered]@{ description = 'Extra-high reasoning depth'; effort = 'xhigh' },
                [ordered]@{ description = 'Maximum reasoning depth'; effort = 'max' },
                [ordered]@{ description = 'Maximum reasoning with automatic delegation'; effort = 'ultra' }
            )
        }
        default {
            return @(
                [ordered]@{ description = 'Fast responses with lighter reasoning'; effort = 'low' },
                [ordered]@{ description = 'Balanced speed and reasoning depth'; effort = 'medium' },
                [ordered]@{ description = 'Greater reasoning depth for complex tasks'; effort = 'high' },
                [ordered]@{ description = 'Extra-high reasoning depth'; effort = 'xhigh' },
                [ordered]@{ description = 'Maximum reasoning depth'; effort = 'max' },
                [ordered]@{ description = 'Maximum reasoning with automatic delegation'; effort = 'ultra' }
            )
        }
    }
}

function Set-JsonProperty($Object, [string]$Name, $Value) {
    $property = $Object.PSObject.Properties[$Name]
    if ($null -eq $property) {
        $Object | Add-Member -NotePropertyName $Name -NotePropertyValue $Value
    } else {
        $Object.$Name = $Value
    }
}

function Set-ConfigEffort([string]$TomlPath, [string]$Effort) {
    $content = [System.IO.File]::ReadAllText($TomlPath, [System.Text.Encoding]::UTF8)
    $pattern = '(?m)^\s*model_reasoning_effort\s*=\s*["''][^"'']*["'']\s*(?:#.*)?$'
    $replacement = 'model_reasoning_effort = "' + $Effort + '"'

    if ([regex]::IsMatch($content, $pattern)) {
        $updated = [regex]::Replace($content, $pattern, $replacement, 1)
    } else {
        $updated = $replacement + [Environment]::NewLine + $content
    }

    [System.IO.File]::WriteAllText($TomlPath, $updated, [System.Text.UTF8Encoding]::new($false))
}

$ConfigPath = [System.IO.Path]::GetFullPath($ConfigPath)
$catalogPath = Get-CatalogPath -TomlPath $ConfigPath

Write-Step "配置文件：$ConfigPath"
Write-Step "已自动定位模型目录：$catalogPath"

if (-not (Test-Path -LiteralPath $catalogPath -PathType Leaf)) {
    throw "model_catalog_json 指向的文件不存在：$catalogPath"
}

if ($UnlockCatalog -or $UnlockOnly) {
    Set-ItemProperty -LiteralPath $catalogPath -Name IsReadOnly -Value $false
    Write-Step '已解除模型目录文件的只读保护。'
    if ($UnlockOnly) {
        Write-Host "文件位置：$catalogPath" -ForegroundColor Green
        return
    }
}

$fileInfo = Get-Item -LiteralPath $catalogPath
if ($fileInfo.IsReadOnly) {
    throw "模型目录当前是只读状态：$catalogPath`n请先运行：.\Fix-Codex-ReasoningLevels.ps1 -UnlockCatalog"
}

$allowedByPreset = switch ($Preset) {
    'Binary'   { @('none', 'high') }
    'Extended' { @('low', 'medium', 'high', 'xhigh', 'max', 'ultra') }
    default    { @('low', 'medium', 'high', 'xhigh', 'max', 'ultra') }
}

if ($DefaultEffort -notin $allowedByPreset) {
    throw "默认档位 '$DefaultEffort' 不属于预设 '$Preset'。允许值：$($allowedByPreset -join ', ')"
}

$timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$catalogBackup = "$catalogPath.bak-$timestamp"
$configBackup = "$ConfigPath.bak-reasoning-$timestamp"

if ($PSCmdlet.ShouldProcess($catalogPath, "备份并将全部模型推理档位替换为 $Preset")) {
    Copy-Item -LiteralPath $catalogPath -Destination $catalogBackup -Force
    if (-not $NoConfigUpdate) {
        Copy-Item -LiteralPath $ConfigPath -Destination $configBackup -Force
    }

    try {
        $catalogText = [System.IO.File]::ReadAllText($catalogPath, [System.Text.Encoding]::UTF8)
        $catalog = $catalogText | ConvertFrom-Json
    } catch {
        throw "模型目录不是有效 JSON：$catalogPath`n$($_.Exception.Message)"
    }

    if ($null -eq $catalog.models -or @($catalog.models).Count -eq 0) {
        throw "模型目录中没有 models 数组或数组为空：$catalogPath"
    }

    $levels = Get-ReasoningLevels -Name $Preset
    $changed = 0
    foreach ($model in @($catalog.models)) {
        # 每个模型都使用独立数组，避免对象引用带来的意外修改。
        $modelLevels = @($levels | ForEach-Object { [pscustomobject]$_ })
        Set-JsonProperty -Object $model -Name 'supported_reasoning_levels' -Value $modelLevels
        Set-JsonProperty -Object $model -Name 'default_reasoning_level' -Value $DefaultEffort
        $changed++
    }

    $json = $catalog | ConvertTo-Json -Depth 100
    [System.IO.File]::WriteAllText($catalogPath, $json + [Environment]::NewLine, [System.Text.UTF8Encoding]::new($false))

    # 写回后重新解析，确保生成的 JSON 有效。
    $verifyText = [System.IO.File]::ReadAllText($catalogPath, [System.Text.Encoding]::UTF8)
    $verify = $verifyText | ConvertFrom-Json
    foreach ($model in @($verify.models)) {
        $actual = @($model.supported_reasoning_levels | ForEach-Object { $_.effort })
        if (($actual -join ',') -ne ($allowedByPreset -join ',')) {
            throw "验证失败：模型 '$($model.slug)' 的推理档位没有正确写入。"
        }
        if ($model.default_reasoning_level -ne $DefaultEffort) {
            throw "验证失败：模型 '$($model.slug)' 的默认档位没有正确写入。"
        }
    }

    if (-not $NoConfigUpdate) {
        Set-ConfigEffort -TomlPath $ConfigPath -Effort $DefaultEffort
    }

    if ($LockCatalog) {
        Set-ItemProperty -LiteralPath $catalogPath -Name IsReadOnly -Value $true
        Write-Step '已将模型目录设置为只读，防止 ccSwitch 覆盖。'
    }

    Write-Host ''
    Write-Host '修复完成。' -ForegroundColor Green
    Write-Host "已修改模型数：$changed"
    Write-Host "推理档位：$($allowedByPreset -join ', ')"
    Write-Host "默认档位：$DefaultEffort"
    Write-Host "模型目录备份：$catalogBackup"
    if (-not $NoConfigUpdate) {
        Write-Host "Codex 配置备份：$configBackup"
    }
    Write-Host ''
    Write-Host '请完全退出 Codex Desktop（包括托盘进程）后重新启动。' -ForegroundColor Yellow
    if ($LockCatalog) {
        Write-Host '以后若需让 ccSwitch 更新此文件，请先用 -UnlockCatalog 解锁。' -ForegroundColor Yellow
    }
}

if (-not $NoRestartPrompt -and $Host.Name -match 'ConsoleHost') {
    Write-Host ''
    Read-Host '按 Enter 退出' | Out-Null
}
