#!/usr/bin/env python3
"""
文档验证工具集
用于验证文档的存在性、完整性、格式和一致性
"""

import sys
import argparse
from validators import (
    DocumentExistenceChecker,
    DocumentContentChecker,
    CodeExampleValidator,
    MarkdownFormatChecker,
    DocumentStructureChecker,
    TerminologyChecker,
    LinkValidator,
)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(
        description='文档验证工具集',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 运行所有检查
  python scripts/validate_docs.py --all
  
  # 运行特定检查
  python scripts/validate_docs.py --existence --content
  
  # 指定项目根目录
  python scripts/validate_docs.py --all --root /path/to/project
        """
    )
    
    parser.add_argument('--root', default='.', help='项目根目录路径')
    parser.add_argument('--all', action='store_true', help='运行所有检查')
    parser.add_argument('--existence', action='store_true', help='检查文档存在性')
    parser.add_argument('--content', action='store_true', help='检查文档内容完整性')
    parser.add_argument('--code', action='store_true', help='验证代码示例')
    parser.add_argument('--format', action='store_true', help='检查 Markdown 格式')
    parser.add_argument('--structure', action='store_true', help='检查文档结构一致性')
    parser.add_argument('--terminology', action='store_true', help='检查术语一致性')
    parser.add_argument('--links', action='store_true', help='验证链接')
    
    args = parser.parse_args()
    
    # 如果没有指定任何检查，默认运行所有检查
    if not any([args.all, args.existence, args.content, args.code, 
                args.format, args.structure, args.terminology, args.links]):
        args.all = True
    
    root_dir = args.root
    all_success = True
    
    # 运行选定的检查
    if args.all or args.existence:
        checker = DocumentExistenceChecker(root_dir)
        success = checker.check()
        all_success = all_success and success
    
    if args.all or args.content:
        checker = DocumentContentChecker(root_dir)
        success = checker.check()
        all_success = all_success and success
    
    if args.all or args.code:
        checker = CodeExampleValidator(root_dir)
        success = checker.check()
        all_success = all_success and success
    
    if args.all or args.format:
        checker = MarkdownFormatChecker(root_dir)
        success = checker.check()
        all_success = all_success and success
    
    if args.all or args.structure:
        checker = DocumentStructureChecker(root_dir)
        success = checker.check()
        all_success = all_success and success
    
    if args.all or args.terminology:
        checker = TerminologyChecker(root_dir)
        success = checker.check()
        all_success = all_success and success
    
    if args.all or args.links:
        checker = LinkValidator(root_dir)
        success = checker.check()
        all_success = all_success and success
    
    # 打印总结
    print(f"\n{'='*60}")
    if all_success:
        print("✓ 所有验证检查通过！")
    else:
        print("❌ 部分验证检查失败，请查看上述报告")
    print(f"{'='*60}\n")
    
    sys.exit(0 if all_success else 1)


if __name__ == "__main__":
    main()
