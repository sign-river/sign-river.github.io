# -*- coding: utf-8 -*-
"""
遍历 Hugo 博客 content 目录下所有 index.md，
找出 images/ 文件夹中未被引用的图片并删除。

用法（在项目根目录执行）：
  python scripts/clean_unused_images.py           # 实际删除
  python scripts/clean_unused_images.py --dry-run # 试运行，只打印不删除
"""

import io
import os
import re
import sys
from pathlib import Path

# 强制 stdout 使用 UTF-8，避免 Windows 乱码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

# ── 可配置项 ──────────────────────────────────────────────
REPO_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = REPO_ROOT / "content"
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".ico"}
IMAGE_DIRS = {"images", "image"}
DRY_RUN = "--dry-run" in sys.argv
# ─────────────────────────────────────────────────────────

# Markdown 图片：![alt](path)
RE_MD_IMAGE = re.compile(r'!\[.*?\]\(([^)]+)\)')
# HTML src/href 属性：src="..." 或 src='...'
RE_HTML_ATTR = re.compile(r'(?:src|href)\s*=\s*["\']([^"\']+)["\']')
# YAML front matter 字段（image / thumbnail / cover 等常见封面字段）
RE_YAML_IMAGE = re.compile(
    r'^(?:image|thumbnail|cover|featured_image|banner)\s*:\s*(.+)$',
    re.MULTILINE | re.IGNORECASE,
)


def extract_referenced_images(md_text: str) -> set[str]:
    """从 md 文本中提取所有引用的图片文件名（仅文件名，不含路径）。"""
    refs: set[str] = set()

    # Markdown 语法
    for m in RE_MD_IMAGE.finditer(md_text):
        refs.add(Path(m.group(1).strip()).name)

    # HTML 属性
    for m in RE_HTML_ATTR.finditer(md_text):
        path = m.group(1).strip()
        if Path(path).suffix.lower() in IMAGE_EXTENSIONS:
            refs.add(Path(path).name)

    # YAML front matter 封面字段
    for m in RE_YAML_IMAGE.finditer(md_text):
        path = m.group(1).strip().strip('"\'')
        if path and not path.startswith('#'):
            refs.add(Path(path).name)

    return refs


def process_article(index_md: Path, dry_run: bool) -> tuple[int, int]:
    """处理单篇文章，返回 (检查图片数，删除图片数)。"""
    article_dir = index_md.parent
    md_text = index_md.read_text(encoding="utf-8", errors="ignore")
    referenced = extract_referenced_images(md_text)

    checked = deleted = 0
    for img_dir_name in IMAGE_DIRS:
        img_dir = article_dir / img_dir_name
        if not img_dir.is_dir():
            continue
        for img_file in sorted(img_dir.iterdir()):
            if not img_file.is_file():
                continue
            if img_file.suffix.lower() not in IMAGE_EXTENSIONS:
                continue
            checked += 1
            if img_file.name not in referenced:
                rel = img_file.relative_to(CONTENT_DIR.parent)
                if dry_run:
                    print(f"  [将删除] {rel}")
                else:
                    img_file.unlink()
                    print(f"  [已删除] {rel}")
                deleted += 1
    return checked, deleted


def main():
    if not CONTENT_DIR.is_dir():
        print(f"错误：找不到 content 目录：{CONTENT_DIR}")
        sys.exit(1)

    mode = "（试运行，不会实际删除）" if DRY_RUN else "（将实际删除文件）"
    print(f"=== Hugo 博客冗余图片清理工具 {mode} ===\n")

    total_articles = total_checked = total_deleted = 0

    for index_md in sorted(CONTENT_DIR.rglob("index.md")):
        checked, deleted = process_article(index_md, DRY_RUN)
        if checked > 0:
            rel = index_md.relative_to(CONTENT_DIR.parent)
            tag = f"删除 {deleted} 张" if deleted else "无冗余  "
            print(f"[{tag:^8}] {rel}  （共 {checked} 张）")
        total_articles += 1
        total_checked += checked
        total_deleted += deleted

    action = "将删除" if DRY_RUN else "已删除"
    print(
        f"\n扫描完毕：共 {total_articles} 篇文章，"
        f"检查 {total_checked} 张图片，"
        f"{action} {total_deleted} 张冗余图片。"
    )


if __name__ == "__main__":
    main()
