#!/usr/bin/env python3
"""统计已发布文章（非草稿）：列出每篇标题、路径、字数，并输出总字数。
注意：为了与 Hugo 保持一致，统计的是 UTF-8 字节数，而不是字符数。
在项目根目录运行：python scripts/word_count_published.py"""

import re
import sys
from pathlib import Path


def is_draft(text: str) -> bool:
    """front matter 中 draft: true 视为草稿。无 draft 或 draft: false 视为已发布。"""
    return bool(re.search(r"draft:\s*true", text))


def extract_title(text: str) -> str:
    m = re.search(r"^title:\s*(.+)$", text, re.MULTILINE)
    if not m:
        return "(无 title)"
    return re.sub(r'^["\']|["\']\s*$', "", m.group(1).strip())


def strip_front_matter(text: str) -> str:
    """去掉 YAML front matter，返回正文。"""
    if not text.strip().startswith("---"):
        return text
    lines = text.split('\n')
    if lines[0].strip() == '---':
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                return '\n'.join(lines[i+1:])
    return text


def main():
    script_dir = Path(__file__).resolve().parent
    base = script_dir.parent
    content_dir = base / "content"
    if not content_dir.exists():
        print("未找到 content 目录。")
        sys.exit(1)

    items = []
    for md in sorted(content_dir.rglob("*.md")):
        try:
            text = md.read_text(encoding="utf-8")
        except Exception:
            continue
        if is_draft(text):
            continue
        title = extract_title(text)
        body = strip_front_matter(text)
        
        # Hugo 使用 len .RawContent 统计的是 UTF-8 字节数，而不是字符数
        byte_count = len(body.encode('utf-8'))
        char_count = len(body)
        
        try:
            rel = md.relative_to(base)
        except ValueError:
            rel = md
        items.append((title, rel, byte_count, char_count))

    if not items:
        print("没有已发布的文章（所有文章均为 draft: true 或未找到 .md）。")
        return

    total_bytes = 0
    total_chars = 0
    for title, rel, byte_count, char_count in items:
        print(f"  {byte_count:>8} 字节  {title}")
        print(f"           ({char_count:>8} 字符)  {rel}")
        total_bytes += byte_count
        total_chars += char_count

    print()
    print(f"共 {len(items)} 篇已发布文章")
    print(f"总字节数：{total_bytes:>8} 字节 ({total_bytes/10000:.2f} 万字节) ← 与 Hugo 统计一致")
    print(f"总字符数：{total_chars:>8} 字符 ({total_chars/10000:.2f} 万字符)")


if __name__ == "__main__":
    main()
