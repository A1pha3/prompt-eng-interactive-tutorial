#!/usr/bin/env python3
"""显示剩余的代码块错误"""

from pathlib import Path

def get_code_block(file_path: str, block_num: int):
    """获取指定的代码块"""
    content = Path(file_path).read_text(encoding='utf-8')
    blocks = []
    lines = content.split('\n')
    in_block = False
    block_start_line = 0
    block_lang = ''
    block_lines = []
    
    for i, line in enumerate(lines):
        if line.strip().startswith('```'):
            if not in_block:
                in_block = True
                block_start_line = i + 1
                block_lang = line.strip()[3:].strip()
                block_lines = []
            else:
                in_block = False
                blocks.append({
                    'start_line': block_start_line,
                    'lang': block_lang,
                    'code': '\n'.join(block_lines)
                })
        elif in_block:
            block_lines.append(line)
    
    if block_num <= len(blocks):
        return blocks[block_num - 1]
    return None

# 剩余错误列表
errors = [
    ('docs/zh/advanced/performance.md', 46),
    ('docs/zh/user-guide/configuration.md', 20),
]

for file_path, block_num in errors:  # 查看所有
    print(f"\n{'='*80}")
    print(f"文件: {file_path}")
    print(f"代码块 #{block_num}")
    print('='*80)
    
    block = get_code_block(file_path, block_num)
    if block:
        print(f"起始行: {block['start_line']}")
        print(f"语言: {block['lang'] or '未指定'}")
        print(f"\n代码内容:")
        print('-'*80)
        for i, line in enumerate(block['code'].split('\n'), 1):
            print(f"{i:3}: {line}")
        print('-'*80)
