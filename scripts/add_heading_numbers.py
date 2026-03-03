#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
为 Hugo 博客文章自动添加标题序号的脚本
只处理 content/post 目录下的 Markdown 文件

功能分为两个阶段：
1. 清除所有标题行前的序号（直接在 ## 后面删除）
2. 按照技术规范格式重新添加序号（如 1., 2., 3., 2.1., 2.1.1.）

使用方法：
    python scripts/add_heading_numbers.py                    # 处理默认目录
    python scripts/add_heading_numbers.py --dry-run          # 预览模式（不修改文件）
    python scripts/add_heading_numbers.py --path ./custom   # 指定目录
    python scripts/add_heading_numbers.py file1.md file2.md  # 处理指定文件

支持的命令行参数：
    --dry-run, -d       预览模式，只显示会修改的内容，不实际写入文件
    --path, -p PATH     指定要处理的目录路径（默认：content/post）
    --help, -h          显示帮助信息
"""

import os
import re
import sys
import argparse
from pathlib import Path


def remove_existing_numbers(heading_text):
    """
    移除标题文本前的所有序号
    直接删除 ## 后面的序号部分
    
    支持的序号格式：
    - 技术规范格式：1.2.3., 2.1., 3.1.1. 等
    - 中文数字：一、二、三、(一)、(1) 等
    - 阿拉伯数字：1. 2. 3. 1、2、3、等
    - 罗马数字：I. II. III. 等
    
    返回清理后的文本
    """
    text = heading_text.strip()
    
    # 所有序号模式的综合列表（按优先级排序）
    patterns = [
        # 技术规范格式序号（优先级最高，如 1., 1.2., 1.2.3.）
        r'^\d+(\.\d+)*\.?[\s、.．]?',  # 匹配 1., 1.2., 1.2.3. 等
        
        # 中文数字序号
        r'^[一二三四五六七八九十百千万]+[、.．]',  # 一、二、三、
        r'^第 [一二三四五六七八九十百千万]+[章节条]',  # 第一章、第二节
        r'^[(（][一二三四五六七八九十百千万]+[)）]',  # (一)、(二)
        
        # 阿拉伯数字序号
        r'^\d+[.．、]',  # 1. 2. 3. 或 1、2、3、
        r'^[(（]?\d+[)）][.．、]?',  # (1). 1). (1)、
        r'^第 \d+[章节条]',  # 第 1 章、第 2 节
        
        # 罗马数字序号
        r'^[IVXivx]+[.．、]',  # I. II. III.
        r'^[(（][IVXivx]+[)）]',  # (I). (II)
        
        # Emoji 开头的标题（也移除）
        r'^[🐶🐱🐭🐹🐰🦊🐻🐼🐨🐯🦁🐮🐷🐸🐵🐔🐧🐦🐤🦆🦅🦉🦇🐺🐗🐴🦄🐝🐛🦋🐌🐞🐜🦟🦗🕷🕸🐢🐍🦎🦖🦕🐙🦑🦐🦞🦀🐡🐠🐟🐬🐳🦈🐊🐅🐆🦓🐒🦍🦧🐘🦛🦏🐪🐫🦒🦘🐃🐄🐂🐎🐖🐏🐑🦙🐐🦌🐕🐩🦮🐕‍🦺🐈🐈‍⬛🐓🦃🦚🦜🦢🦩🕊🐇🦝🦨🦡🦦🦥🐁🐀🐿🦔🐾🐉🐲]+[\s、.．]?',
        
        # 常见表情符号文字前缀
        r'^[💡🚀📖🔧🛠️🎮❓⚠️🎉💬📚📝✅⭐🔥❤️👍👎❌✅]+[\s、.．]?',
    ]
    
    for pattern in patterns:
        match = re.match(pattern, text)
        if match:
            # 移除匹配到的序号部分
            text = text[len(match.group(0)):].strip()
            # 清理可能残留的标点
            text = re.sub(r'^[、.．\s]+', '', text)
            break
    
    return text


def add_technical_numbers(content):
    """
    为文章内容添加技术规范格式的标题序号
    格式示例：1., 2., 3., 2.1., 2.1.1., 2.2., 4., 4.1. ...
    （注意：每一级后面都有点）
    
    返回处理后的内容
    """
    lines = content.split('\n')
    
    # 记录每个层级的当前序号（支持 6 级标题）
    heading_counters = {
        1: 0,  # # 
        2: 0,  # ##
        3: 0,  # ###
        4: 0,  # ####
        5: 0,  # #####
        6: 0,  # ######
    }
    
    processed_lines = []
    in_front_matter = False
    front_matter_processed = False  # 标记是否已经处理完 front matter
    in_code_block = False  # 标记是否在代码块内
    
    for line in lines:
        # 检测代码块（``` 开始和结束）
        stripped_line = line.strip()
        if stripped_line.startswith('```'):
            in_code_block = not in_code_block
            processed_lines.append(line)
            continue
        
        # 如果在代码块内，不处理
        if in_code_block:
            processed_lines.append(line)
            continue
        
        # 检测 front matter 区域（以 --- 开始和结束）
        # 注意：只有在文件开头附近的 --- 才是 front matter
        if stripped_line == '---' and not front_matter_processed:
            in_front_matter = not in_front_matter
            if not in_front_matter:
                front_matter_processed = True  # front matter 结束
            processed_lines.append(line)
            continue
        
        # 如果在 front matter 区域，不处理
        if in_front_matter:
            processed_lines.append(line)
            continue
        
        # 检测标题行（确保有空格分隔）
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            hashes = heading_match.group(1)
            heading_text = heading_match.group(2)
            level = len(hashes)
            
            # 先移除旧序号
            clean_text = remove_existing_numbers(heading_text)
            
            # 更新当前层级的计数器
            heading_counters[level] += 1
            
            # 重置所有下级标题的计数器
            for i in range(level + 1, 7):
                heading_counters[i] = 0
            
            # 生成技术规范格式的序号
            # 例如：level=3 时，生成 "1.2.3." 格式（注意最后有个点）
            number_parts = []
            for i in range(1, level + 1):
                # 只添加非零的计数器
                if heading_counters[i] > 0:
                    number_parts.append(str(heading_counters[i]))
            
            # 用点连接，最后再加一个点
            technical_number = '.'.join(number_parts) + '.'
            
            # 生成新标题
            new_heading = f"{technical_number} {clean_text}"
            new_line = f"{hashes} {new_heading}"
            processed_lines.append(new_line)
        else:
            processed_lines.append(line)
    
    return '\n'.join(processed_lines)


def process_file(file_path, dry_run=False):
    """
    处理单个文件：两阶段处理
    1. 清除所有序号
    2. 添加技术规范格式序号
    
    Args:
        file_path: 文件路径
        dry_run: 是否为预览模式（不实际写入文件）
    
    Returns:
        bool: 处理是否成功
    """
    try:
        # 尝试多种编码
        encodings = ['utf-8', 'gbk', 'gb2312']
        content = None
        used_encoding = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                    used_encoding = encoding
                    break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"警告：无法读取文件 {file_path}（编码问题）")
            return False
        
        # 两阶段处理
        new_content = add_technical_numbers(content)
        
        # 检查是否有实际修改
        if content == new_content:
            print(f"跳过：{file_path.relative_to(Path(__file__).parent.parent)}（无变化）")
            return True
        
        if dry_run:
            print(f"预览：{file_path.relative_to(Path(__file__).parent.parent)}")
            # 显示前几行差异（可选）
            return True
        else:
            # 写回文件
            with open(file_path, 'w', encoding=used_encoding) as f:
                f.write(new_content)
            return True
            
    except Exception as e:
        print(f"处理文件失败 {file_path}: {e}")
        return False


def process_directory(directory_path, dry_run=False):
    """
    处理指定目录下的所有 Markdown 文件
    
    Args:
        directory_path: 目录路径
        dry_run: 是否为预览模式
    
    Returns:
        tuple: (总文件数，成功处理数，失败数)
    """
    post_dir = Path(directory_path)
    
    if not post_dir.exists():
        print(f"错误：找不到目录 {post_dir}")
        return 0, 0, 0
    
    # 统计信息
    total_files = 0
    processed_files = 0
    failed_files = 0
    
    print(f"开始处理目录：{post_dir}")
    print("=" * 70)
    print("处理流程：")
    print("  阶段 1: 清除所有标题行前的序号（直接在 ## 后面删除）")
    print("  阶段 2: 按照技术规范格式添加序号（如 1., 2., 3., 2.1., 2.1.1.）")
    if dry_run:
        print("  模式：预览模式（不会修改文件）")
    print("=" * 70)
    
    # 遍历所有 .md 文件
    for md_file in post_dir.rglob('*.md'):
        # 跳过 README.md 等文件
        if md_file.name.upper() == 'README.MD':
            continue
        
        total_files += 1
        if process_file(md_file, dry_run):
            processed_files += 1
        else:
            failed_files += 1
    
    return total_files, processed_files, failed_files


def main():
    """
    主函数：支持命令行参数
    """
    parser = argparse.ArgumentParser(
        description="为 Hugo 博客文章自动添加标题序号",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例：
  python scripts/add_heading_numbers.py                    # 处理默认目录
  python scripts/add_heading_numbers.py --dry-run          # 预览模式
  python scripts/add_heading_numbers.py --path ./custom   # 指定目录
  python scripts/add_heading_numbers.py file1.md file2.md  # 处理指定文件
        """
    )
    
    parser.add_argument(
        '--dry-run', '-d',
        action='store_true',
        help='预览模式，只显示会修改的内容，不实际写入文件'
    )
    
    parser.add_argument(
        '--path', '-p',
        type=str,
        default='content/post',
        help='指定要处理的目录路径（默认：content/post）'
    )
    
    parser.add_argument(
        'files',
        nargs='*',
        help='可选：指定要处理的具体文件（如果提供，则忽略 --path 参数）'
    )
    
    args = parser.parse_args()
    
    # 获取项目根目录
    script_dir = Path(__file__).parent.parent
    
    if args.files:
        # 处理指定文件
        total_files = len(args.files)
        processed_files = 0
        failed_files = 0
        
        print(f"开始处理 {total_files} 个指定文件")
        print("=" * 70)
        
        for file_path in args.files:
            full_path = Path(file_path)
            if not full_path.exists():
                print(f"警告：文件不存在 {file_path}")
                failed_files += 1
                continue
                
            if process_file(full_path, args.dry_run):
                processed_files += 1
            else:
                failed_files += 1
    else:
        # 处理目录
        target_path = script_dir / args.path
        total_files, processed_files, failed_files = process_directory(target_path, args.dry_run)
    
    print("=" * 70)
    print(f"处理完成！")
    print(f"总文件数：{total_files}")
    print(f"成功处理：{processed_files}")
    print(f"处理失败：{failed_files}")
    print("=" * 70)


if __name__ == '__main__':
    main()