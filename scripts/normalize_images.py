# -*- coding: utf-8 -*-
"""将 content/post 下文章中的图片统一为：<a href="..."><img ... style=\"max-width: 100%; width: 1000px;\"/></a>"""
import re
import os
from pathlib import Path

CONTENT_POST = Path(__file__).resolve().parent.parent / "content" / "post"
TARGET_FORMAT = '<a href="{path}" target="_blank"> <img src="{path}" alt="{alt}" style="max-width: 100%; width: 1000px;"/> </a>'

def normalize_path(path: str) -> str:
    return path.replace("\\", "/")

def process_text(text: str) -> str:
    # 1) 已是标准格式但可能多行或反斜杠：统一成单行 + 正斜杠
    def replace_wrapped(m):
        path = normalize_path(m.group(1))
        src = normalize_path(m.group(2))
        alt = m.group(3) or "image"
        return TARGET_FORMAT.format(path=path, alt=alt)

    text = re.sub(
        r'<a\s+href="(images[^"]+)"\s+target="_blank">\s*<img\s+src="([^"]+)"\s+alt="([^"]*)"[^>]*/?>\s*</a>',
        replace_wrapped,
        text,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # 2) 裸 <img src="images/..." alt="..." width="数字"> 或 width="数字" />
    def replace_standalone(m):
        path = normalize_path(m.group(1))
        alt = m.group(2) or "image"
        return TARGET_FORMAT.format(path=path, alt=alt)

    text = re.sub(
        r'<img\s+src="(images[^"]+)"\s+alt="([^"]*)"\s+width="\d+"\s*/?>',
        replace_standalone,
        text,
        flags=re.IGNORECASE,
    )

    # 3) Markdown 图片 ![alt](images/xxx.png)（仅限 images/ 开头的路径）
    def replace_md(m):
        alt = m.group(1) or "image"
        path = normalize_path(m.group(2))
        return TARGET_FORMAT.format(path=path, alt=alt)

    text = re.sub(
        r'!\[([^\]]*)\]\((images/[^)]+)\)',
        replace_md,
        text,
    )

    return text

def extract_code_blocks(content: str):
    """按 ``` 分割，返回 (非代码段列表，代码段列表) 交错表示：0=普通 1=代码"""
    parts = []
    current = []
    in_fence = False
    fence = None
    for line in content.split("\n"):
        if line.strip().startswith("```"):
            prefix = line[: line.index("```")]
            rest = line.strip()[3:].strip()
            if not in_fence:
                if current:
                    parts.append((0, "\n".join(current)))
                    current = []
                in_fence = True
                fence = "```"
                if rest:
                    current = [line]
                else:
                    current = [line]
            else:
                current.append(line)
                parts.append((1, "\n".join(current)))
                current = []
                in_fence = False
            continue
        current.append(line)
    if current:
        parts.append((1 if in_fence else 0, "\n".join(current)))
    return parts

def process_file(path: Path) -> bool:
    raw = path.read_text(encoding="utf-8")
    parts = extract_code_blocks(raw)
    changed = False
    new_parts = []
    for is_code, block in parts:
        if is_code:
            new_parts.append(block)
        else:
            new_block = process_text(block)
            if new_block != block:
                changed = True
            new_parts.append(new_block)
    if changed:
        out = "\n".join(new_parts)
        path.write_text(out, encoding="utf-8")
    return changed

def main():
    # 不处理语法指南里的“示例”（代码块内的不处理已由 extract_code_blocks 保证）
    skip_dirs = set()
    changed_files = []
    for root, dirs, files in os.walk(CONTENT_POST):
        for f in files:
            if f != "index.md":
                continue
            path = Path(root) / f
            if path.is_file():
                try:
                    if process_file(path):
                        changed_files.append(path.relative_to(CONTENT_POST))
                except Exception as e:
                    print(f"Error {path}: {e}")
    for p in changed_files:
        print("Updated:", p)

if __name__ == "__main__":
    main()
