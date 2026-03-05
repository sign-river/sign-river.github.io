#!/usr/bin/env python3
"""统计已发布文章（非草稿）：列出每篇标题、路径、字数，并输出总字数。
注意：统计逻辑与左侧边栏一致 - 仅统计 content/post/ 目录，使用 CJK 字符数统计。
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


def count_cjk_chars(text: str) -> int:
    """统计 CJK 字符数（模拟 Hugo 的 .WordCount 在 hasCJKLanguage=true 时的行为）。
    去除代码块、HTML 标签、链接等 markdown 语法后统计字符数。"""

    # 1. 移除代码块（```...```）
    text = re.sub(r'```[\s\S]*?```', '', text)

    # 2. 移除行内代码（`...`）
    text = re.sub(r'`[^`]+`', '', text)

    # 3. 移除 HTML 标签
    text = re.sub(r'<[^>]+>', '', text)

    # 4. 移除图片语法 ![alt](url)
    text = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', r'\1', text)

    # 5. 移除链接，保留文本 [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)

    # 6. 移除标题标记 # ## ###
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)

    # 7. 移除列表标记 - * +
    text = re.sub(r'^\s*[-*+]\s+', '', text, flags=re.MULTILINE)

    # 8. 移除有序列表标记 1. 2.
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)

    # 9. 移除引用标记 >
    text = re.sub(r'^\s*>\s+', '', text, flags=re.MULTILINE)

    # 10. 移除粗体/斜体标记 ** * __ _
    text = re.sub(r'\*\*([^\*]+)\*\*', r'\1', text)
    text = re.sub(r'\*([^\*]+)\*', r'\1', text)
    text = re.sub(r'__([^_]+)__', r'\1', text)
    text = re.sub(r'_([^_]+)_', r'\1', text)

    # 11. 移除删除线 ~~
    text = re.sub(r'~~([^~]+)~~', r'\1', text)

    # 12. 移除水平线 --- ***
    text = re.sub(r'^[-*_]{3,}$', '', text, flags=re.MULTILINE)

    # 13. 移除所有空白字符后统计
    non_whitespace = re.sub(r'\s', '', text)

    return len(non_whitespace)


def main():
    script_dir = Path(__file__).resolve().parent
    base = script_dir.parent

    # 只统计 content/post/ 目录，与 mainSections = ["post"] 保持一致
    post_dir = base / "content" / "post"
    if not post_dir.exists():
        print("未找到 content/post 目录。")
        sys.exit(1)

    items = []
    for md in sorted(post_dir.rglob("*.md")):
        try:
            text = md.read_text(encoding="utf-8")
        except Exception:
            continue
        if is_draft(text):
            continue
        title = extract_title(text)
        body = strip_front_matter(text)

        # 使用 CJK 字符数统计（模拟 Hugo 的 .WordCount）
        word_count = count_cjk_chars(body)

        try:
            rel = md.relative_to(base)
        except ValueError:
            rel = md
        items.append((title, rel, word_count))

    if not items:
        print("没有已发布的文章（所有文章均为 draft: true 或未找到 .md）。")
        return

    total_words = 0
    for title, rel, word_count in items:
        print(f"  {word_count:>8} 字  {title}")
        print(f"               {rel}")
        total_words += word_count

    print()
    print(f"共 {len(items)} 篇已发布文章")
    print(f"总字数：{total_words:>8} 字", end="")
    if total_words >= 10000:
        wan = total_words // 10000
        decimal = (total_words // 1000) % 10
        if decimal == 0:
            print(f" ({wan}万字)", end="")
        else:
            print(f" ({wan}.{decimal}万字)", end="")
    elif total_words >= 1000:
        k = total_words // 1000
        decimal = (total_words // 100) % 10
        if decimal == 0:
            print(f" ({k}k字)", end="")
        else:
            print(f" ({k}.{decimal}k字)", end="")
    print(" ← 与左侧边栏统计逻辑一致")


if __name__ == "__main__":
    main()
