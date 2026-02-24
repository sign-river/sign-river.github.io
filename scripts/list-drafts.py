#!/usr/bin/env python3
"""列出所有 draft: true 的文章（标题 + 路径）。在项目根目录运行：python scripts/list-drafts.py"""

import re
import sys
from pathlib import Path

def main():
    script_dir = Path(__file__).resolve().parent
    content_dir = script_dir.parent / "content"
    if not content_dir.exists():
        print("未找到 content 目录。")
        sys.exit(1)

    base = script_dir.parent
    count = 0
    draft_re = re.compile(r"draft:\s*true")
    title_re = re.compile(r"^title:\s*(.+)$", re.MULTILINE)

    for md in content_dir.rglob("*.md"):
        try:
            text = md.read_text(encoding="utf-8")
        except Exception:
            continue
        if not draft_re.search(text):
            continue
        title = "(无 title)"
        m = title_re.search(text)
        if m:
            title = re.sub(r'^["\']|["\']\s*$', "", m.group(1).strip())
        try:
            rel = md.relative_to(base)
        except ValueError:
            rel = md
        print()
        print(title)
        print(" ", rel)
        print(" ", md.resolve())
        count += 1

    print()
    if count == 0:
        print("当前没有草稿（没有任何文章 front matter 里带 draft: true）。")
    else:
        print(f"共 {count} 篇草稿。")

if __name__ == "__main__":
    main()
