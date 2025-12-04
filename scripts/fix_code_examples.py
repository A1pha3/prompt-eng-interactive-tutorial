#!/usr/bin/env python3
"""
修复文档中的代码示例错误
"""

import re
import ast
from pathlib import Path
from typing import List, Tuple, Dict

def extract_code_blocks(content: str) -> List[Tuple[int, str, str]]:
    """提取文档中的所有代码块"""
    blocks = []
    lines = content.split('\n')
    in_block = False
    block_start = 0
    block_lang = ''
    block_lines = []
    
    for i, line in enumerate(lines, 1):
        if line.strip().startswith('```'):
            if not in_block:
                # 开始代码块
                in_block = True
                block_start = i
                block_lang = line.strip()[3:].strip()
                block_lines = []
            else:
                # 结束代码块
                in_block = False
                blocks.append((block_start, block_lang, '\n'.join(block_lines)))
        elif in_block:
            block_lines.append(line)
    
    return blocks

def check_python_syntax(code: str) -> Tuple[bool, str]:
    """检查 Python 代码语法"""
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"{e.msg} (行 {e.lineno})"

def find_errors_in_file(file_path: Path) -> List[Dict]:
    """查找文件中的代码错误"""
    content = file_path.read_text(encoding='utf-8')
    blocks = extract_code_blocks(content)
    errors = []
    
    for idx, (line_num, lang, code) in enumerate(blocks, 1):
        # 检查 Python 代码
        if lang.lower() in ['python', 'py', ''] and code.strip():
            is_valid, error_msg = check_python_syntax(code)
            if not is_valid:
                errors.append({
                    'file': str(file_path),
                    'block_num': idx,
                    'line_num': line_num,
                    'lang': lang,
                    'error': error_msg,
                    'code': code
                })
    
    return errors

def main():
    """主函数"""
    docs_dir = Path('docs/zh')
    all_errors = []
    
    # 查找所有 markdown 文件
    for md_file in docs_dir.rglob('*.md'):
        errors = find_errors_in_file(md_file)
        all_errors.extend(errors)
    
    # 打印错误
    print(f"找到 {len(all_errors)} 个代码语法错误：\n")
    for i, error in enumerate(all_errors, 1):
        print(f"{i}. 文件: {error['file']}")
        print(f"   代码块 #{error['block_num']} (行 {error['line_num']})")
        print(f"   语言: {error['lang'] or '未指定'}")
        print(f"   错误: {error['error']}")
        print(f"   代码预览:")
        for line in error['code'].split('\n')[:5]:
            print(f"     {line}")
        print()

if __name__ == '__main__':
    main()
