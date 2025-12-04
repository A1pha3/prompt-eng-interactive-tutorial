#!/usr/bin/env python3
"""查找所有代码块错误"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent))

from validators.code import CodeValidator

validator = CodeValidator()
docs_dir = Path('docs/zh')

all_errors = []
for md_file in sorted(docs_dir.rglob('*.md')):
    result = validator.validate(md_file)
    if result['errors']:
        all_errors.extend(result['errors'])

print(f"找到 {len(all_errors)} 个错误:\n")
for i, error in enumerate(all_errors, 1):
    print(f"{i}. {error}")
