---
title: "Codex 对话无法归档的解决方法"
date: 2026-08-19
description: "解决 Windows 上 Codex 桌面端因本地线程路径记录异常而无法归档对话的问题。"
categories:
  - "开发"
tags:
  - "Codex"
  - "Codex Desktop"
  - "对话归档"
  - "问题排查"
  - "Windows"
  - "SQLite"
draft: false
slug: "codex-unable-to-archive-conversation"
related_group: "codex"
hidden: true
searchable: true
guide: "/p/codex-guide/"
guide_title: "Codex 使用指南"
---

本文适用于 Windows 上的 Codex 桌面端：点击 **归档** 后提示“无法归档对话”，日志中可能同时出现 `os error 2` 或“系统找不到指定的文件”。

## 问题

Codex 的对话内容文件可能仍然存在，但归档操作失败，且同一批对话反复无法归档。

## 原因

Codex 在本地使用 SQLite 保存线程索引，数据库中的 `threads.rollout_path` 用来指向对话内容文件。部分未归档线程被记录成带 Windows 扩展路径前缀的形式：

```text
\\?\C:\Users\<用户名>\.codex\sessions\...
```

归档流程未能正确处理这种路径表示，因而把实际存在的文件判定为不存在，最终报出 `os error 2`。

正确的记录应当是普通 Windows 路径：

```text
C:\Users\<用户名>\.codex\sessions\...
```

解决方法就是：在 Codex 完全退出后，备份本地线程数据库，并把符合条件的 `rollout_path` 规范化为普通路径。

## 正确解决方案

### 1. 完全退出 Codex

先从 Codex 菜单或系统托盘执行 **退出**。然后打开 PowerShell，执行：

```powershell
Get-Process codex -ErrorAction SilentlyContinue
```

没有任何输出才表示 Codex 已完全退出。若仍显示 `codex` 进程，请在任务管理器结束 `codex.exe` 后再继续。

> 不要在 Codex 运行时修改数据库；否则应用内存中的旧状态可能在之后重新写回，导致修复失效。

### 2. 运行修复脚本

新建文件 `fix_codex_archive.py`，将以下内容保存进去：

```python
import json
import shutil
import sqlite3
import subprocess
from datetime import datetime
from pathlib import Path

result = subprocess.run(
    ["tasklist", "/FI", "IMAGENAME eq codex.exe", "/FO", "CSV", "/NH"],
    capture_output=True,
    text=True,
    errors="replace",
    check=False,
)
if any(line.lstrip().startswith('"') for line in result.stdout.splitlines()):
    raise SystemExit("ERROR: codex.exe is still running. Exit Codex completely, then run again.")

codex_home = Path.home() / ".codex"
db_path = codex_home / "state_5.sqlite"
if not db_path.is_file():
    raise SystemExit(f"ERROR: database not found: {db_path}")

stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
backup_dir = codex_home / "repair-backups" / f"manual-normalize-rollout-paths-{stamp}"
backup_dir.mkdir(parents=True, exist_ok=False)

backup_db = backup_dir / "state_5.sqlite.before-repair"
with sqlite3.connect(db_path) as source, sqlite3.connect(backup_db) as destination:
    source.backup(destination)

for suffix in ("-wal", "-shm"):
    source_path = Path(str(db_path) + suffix)
    if source_path.exists():
        shutil.copy2(source_path, backup_dir / source_path.name)

prefix = "\\\\?\\"
with sqlite3.connect(db_path) as conn:
    conn.execute("PRAGMA busy_timeout = 10000")
    rows = conn.execute(
        "SELECT id, rollout_path FROM threads WHERE archived = 0"
    ).fetchall()

    fixes = []
    skipped = []
    for thread_id, old_path in rows:
        if not old_path or not old_path.startswith(prefix):
            continue

        new_path = old_path[len(prefix):]
        if Path(new_path).is_file():
            fixes.append((thread_id, old_path, new_path))
        else:
            skipped.append((thread_id, old_path))

    conn.execute("BEGIN IMMEDIATE")
    for thread_id, old_path, new_path in fixes:
        conn.execute(
            """
            UPDATE threads
            SET rollout_path = ?
            WHERE id = ?
              AND archived = 0
              AND rollout_path = ?
            """,
            (new_path, thread_id, old_path),
        )
    conn.commit()
    conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")

    remaining_rows = conn.execute(
        "SELECT rollout_path FROM threads WHERE archived = 0"
    ).fetchall()

remaining = sum(
    1
    for (path,) in remaining_rows
    if path and path.startswith(prefix)
)

report = {
    "updated_count": len(fixes),
    "skipped_missing_files": len(skipped),
    "remaining_prefixed_active_paths": remaining,
    "backup_dir": str(backup_dir),
}
(backup_dir / "result.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8",
)

print("Updated paths:", len(fixes))
print("Skipped missing files:", len(skipped))
print("Remaining active prefixed paths:", remaining)
print("Backup and report:", backup_dir)
```

在该文件所在目录打开 PowerShell，运行：

```powershell
python .\fix_codex_archive.py
```

脚本会自动备份数据库，只处理未归档、带 `\\?\` 前缀且内容文件真实存在的线程记录。

### 3. 确认结果并重新归档

脚本执行完成后，重点检查最后一行统计：

```text
Remaining active prefixed paths: 0
```

出现 `0` 表示这类异常路径已经全部清理。此时重新打开 Codex，再次对原对话执行 **归档** 即可。

脚本生成的备份和执行报告保存在：

```text
%USERPROFILE%\.codex\repair-backups\manual-normalize-rollout-paths-<时间戳>\
```

## 注意事项

- 不要删除 `%USERPROFILE%\.codex\sessions` 中的对话文件。
- 不要手动把数据库中的 `archived` 改为 `1`。
- 不要在未备份的情况下移动 `.jsonl` 文件。
- 如果脚本执行后 `Remaining active prefixed paths` 不是 `0`，或已经为 `0` 但仍无法归档，则不是本文处理的路径记录问题，应保留错误信息并进一步排查归档流程。
- 本文脚本只能修复当前已经写错的路径记录。修复后打开 Codex 应尽快完成归档；若继续使用一段时间后问题又出现，说明 Codex 又将某些线程写成了带 `\\?\` 前缀的路径。目前看更像是 Codex 自身的 Windows 路径处理问题，本文作为临时恢复方案使用。
