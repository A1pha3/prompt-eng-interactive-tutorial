#!/usr/bin/env python3
"""
综合质量保证脚本
运行所有文档验证检查并生成详细的质量报告
"""

import sys
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from validators import (
    DocumentExistenceChecker,
    DocumentContentChecker,
    CodeExampleValidator,
    MarkdownFormatChecker,
    DocumentStructureChecker,
    TerminologyChecker,
    LinkValidator,
)


class QualityAssuranceRunner:
    """质量保证运行器 - 执行所有验证并生成报告"""
    
    def __init__(self, root_dir: str = '.'):
        self.root_dir = Path(root_dir)
        self.results = {}
        self.start_time = None
        self.end_time = None
    
    def run_all_checks(self) -> bool:
        """运行所有质量检查"""
        self.start_time = datetime.now()
        
        print("=" * 80)
        print("文档质量保证检查")
        print("=" * 80)
        print(f"开始时间: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"项目根目录: {self.root_dir.absolute()}")
        print("=" * 80)
        print()
        
        all_success = True
        
        # 1. 文档存在性检查
        all_success &= self._run_check(
            "文档存在性",
            DocumentExistenceChecker,
            "检查所有必需文档是否存在"
        )
        
        # 2. 文档内容完整性检查
        all_success &= self._run_check(
            "内容完整性",
            DocumentContentChecker,
            "检查文档是否包含必需章节"
        )
        
        # 3. 代码示例验证
        all_success &= self._run_check(
            "代码示例",
            CodeExampleValidator,
            "验证代码示例的语法正确性"
        )
        
        # 4. Markdown 格式检查
        all_success &= self._run_check(
            "Markdown 格式",
            MarkdownFormatChecker,
            "检查 Markdown 格式规范"
        )
        
        # 5. 文档结构一致性检查
        all_success &= self._run_check(
            "结构一致性",
            DocumentStructureChecker,
            "检查同类文档的结构一致性"
        )
        
        # 6. 术语一致性检查
        all_success &= self._run_check(
            "术语一致性",
            TerminologyChecker,
            "检查术语使用的一致性"
        )
        
        # 7. 链接验证
        all_success &= self._run_check(
            "链接有效性",
            LinkValidator,
            "验证所有链接的有效性"
        )
        
        self.end_time = datetime.now()
        
        # 生成报告
        self._generate_summary_report(all_success)
        self._generate_detailed_report()
        
        return all_success
    
    def _run_check(self, name: str, checker_class, description: str) -> bool:
        """运行单个检查"""
        print(f"\n{'─' * 80}")
        print(f"检查 {len(self.results) + 1}/7: {name}")
        print(f"描述: {description}")
        print(f"{'─' * 80}")
        
        try:
            checker = checker_class(str(self.root_dir))
            success = checker.check()
            
            # 收集结果
            self.results[name] = {
                'success': success,
                'errors': getattr(checker, 'errors', []),
                'warnings': getattr(checker, 'warnings', []),
                'info': getattr(checker, 'info', []),
                'stats': getattr(checker, 'stats', {}),
            }
            
            # 打印结果摘要
            if success:
                print(f"\n✓ {name}检查通过")
            else:
                print(f"\n✗ {name}检查失败")
                print(f"  错误数: {len(self.results[name]['errors'])}")
                print(f"  警告数: {len(self.results[name]['warnings'])}")
            
            return success
            
        except Exception as e:
            print(f"\n✗ {name}检查执行失败: {e}")
            self.results[name] = {
                'success': False,
                'errors': [f"检查器执行失败: {str(e)}"],
                'warnings': [],
                'info': [],
                'stats': {},
            }
            return False
    
    def _generate_summary_report(self, all_success: bool):
        """生成摘要报告"""
        print(f"\n\n{'=' * 80}")
        print("质量保证检查摘要")
        print(f"{'=' * 80}")
        
        # 统计信息
        total_checks = len(self.results)
        passed_checks = sum(1 for r in self.results.values() if r['success'])
        failed_checks = total_checks - passed_checks
        
        total_errors = sum(len(r['errors']) for r in self.results.values())
        total_warnings = sum(len(r['warnings']) for r in self.results.values())
        
        print(f"\n检查统计:")
        print(f"  总检查数: {total_checks}")
        print(f"  通过: {passed_checks} ✓")
        print(f"  失败: {failed_checks} ✗")
        print(f"  通过率: {passed_checks / total_checks * 100:.1f}%")
        
        print(f"\n问题统计:")
        print(f"  错误: {total_errors}")
        print(f"  警告: {total_warnings}")
        
        # 执行时间
        duration = self.end_time - self.start_time
        print(f"\n执行时间: {duration.total_seconds():.2f} 秒")
        print(f"完成时间: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 详细结果
        print(f"\n{'─' * 80}")
        print("各项检查结果:")
        print(f"{'─' * 80}")
        
        for i, (name, result) in enumerate(self.results.items(), 1):
            status = "✓ 通过" if result['success'] else "✗ 失败"
            error_count = len(result['errors'])
            warning_count = len(result['warnings'])
            
            print(f"{i}. {name:20s} {status:10s} ", end="")
            if error_count > 0:
                print(f"错误: {error_count:3d} ", end="")
            if warning_count > 0:
                print(f"警告: {warning_count:3d}", end="")
            print()
        
        # 总体结果
        print(f"\n{'=' * 80}")
        if all_success:
            print("✓ 所有质量检查通过！文档质量良好。")
        else:
            print("✗ 部分质量检查失败，请查看详细报告并修复问题。")
        print(f"{'=' * 80}\n")
    
    def _generate_detailed_report(self):
        """生成详细报告文件"""
        report_dir = self.root_dir / "scripts" / "tests"
        report_dir.mkdir(parents=True, exist_ok=True)
        
        # Markdown 报告
        md_report_path = report_dir / "QUALITY_ASSURANCE_REPORT.md"
        self._write_markdown_report(md_report_path)
        
        # JSON 报告
        json_report_path = report_dir / "quality_assurance_report.json"
        self._write_json_report(json_report_path)
        
        print(f"详细报告已生成:")
        print(f"  Markdown: {md_report_path}")
        print(f"  JSON: {json_report_path}")
    
    def _write_markdown_report(self, path: Path):
        """写入 Markdown 格式的详细报告"""
        with open(path, 'w', encoding='utf-8') as f:
            f.write("# 文档质量保证报告\n\n")
            f.write(f"**生成时间**: {self.end_time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            f.write(f"**项目根目录**: `{self.root_dir.absolute()}`\n\n")
            
            # 摘要
            f.write("## 执行摘要\n\n")
            
            total_checks = len(self.results)
            passed_checks = sum(1 for r in self.results.values() if r['success'])
            failed_checks = total_checks - passed_checks
            total_errors = sum(len(r['errors']) for r in self.results.values())
            total_warnings = sum(len(r['warnings']) for r in self.results.values())
            
            f.write(f"- **总检查数**: {total_checks}\n")
            f.write(f"- **通过**: {passed_checks} ✓\n")
            f.write(f"- **失败**: {failed_checks} ✗\n")
            f.write(f"- **通过率**: {passed_checks / total_checks * 100:.1f}%\n")
            f.write(f"- **总错误数**: {total_errors}\n")
            f.write(f"- **总警告数**: {total_warnings}\n")
            
            duration = self.end_time - self.start_time
            f.write(f"- **执行时间**: {duration.total_seconds():.2f} 秒\n\n")
            
            # 各项检查详情
            f.write("## 检查详情\n\n")
            
            for i, (name, result) in enumerate(self.results.items(), 1):
                f.write(f"### {i}. {name}\n\n")
                
                status = "✓ 通过" if result['success'] else "✗ 失败"
                f.write(f"**状态**: {status}\n\n")
                
                # 统计信息
                if result['stats']:
                    f.write("**统计信息**:\n\n")
                    for key, value in result['stats'].items():
                        f.write(f"- {key}: {value}\n")
                    f.write("\n")
                
                # 错误
                if result['errors']:
                    f.write(f"**错误** ({len(result['errors'])}):\n\n")
                    for error in result['errors'][:20]:  # 最多显示20个
                        f.write(f"- {error}\n")
                    if len(result['errors']) > 20:
                        f.write(f"- ... 还有 {len(result['errors']) - 20} 个错误\n")
                    f.write("\n")
                
                # 警告
                if result['warnings']:
                    f.write(f"**警告** ({len(result['warnings'])}):\n\n")
                    for warning in result['warnings'][:20]:  # 最多显示20个
                        f.write(f"- {warning}\n")
                    if len(result['warnings']) > 20:
                        f.write(f"- ... 还有 {len(result['warnings']) - 20} 个警告\n")
                    f.write("\n")
                
                # 信息
                if result['info']:
                    f.write(f"**信息** ({len(result['info'])}):\n\n")
                    for info in result['info'][:10]:  # 最多显示10个
                        f.write(f"- {info}\n")
                    if len(result['info']) > 10:
                        f.write(f"- ... 还有 {len(result['info']) - 10} 条信息\n")
                    f.write("\n")
                
                f.write("---\n\n")
            
            # 建议
            f.write("## 改进建议\n\n")
            
            if total_errors > 0:
                f.write("### 需要修复的错误\n\n")
                f.write("请优先修复以下类型的错误:\n\n")
                
                for name, result in self.results.items():
                    if result['errors']:
                        f.write(f"- **{name}**: {len(result['errors'])} 个错误\n")
                f.write("\n")
            
            if total_warnings > 0:
                f.write("### 建议改进的警告\n\n")
                f.write("以下警告建议在时间允许时进行改进:\n\n")
                
                for name, result in self.results.items():
                    if result['warnings']:
                        f.write(f"- **{name}**: {len(result['warnings'])} 个警告\n")
                f.write("\n")
            
            if total_errors == 0 and total_warnings == 0:
                f.write("✓ 所有检查通过，文档质量优秀！\n\n")
            
            # 下一步
            f.write("## 下一步行动\n\n")
            
            if failed_checks > 0:
                f.write("1. 查看上述错误详情\n")
                f.write("2. 根据错误类型修复相应问题\n")
                f.write("3. 重新运行质量检查验证修复\n")
                f.write("4. 处理警告项（可选）\n")
            else:
                f.write("1. 文档已通过所有质量检查\n")
                f.write("2. 可以进行人工审查\n")
                f.write("3. 准备发布文档\n")
    
    def _write_json_report(self, path: Path):
        """写入 JSON 格式的详细报告"""
        report_data = {
            'metadata': {
                'generated_at': self.end_time.isoformat(),
                'root_dir': str(self.root_dir.absolute()),
                'duration_seconds': (self.end_time - self.start_time).total_seconds(),
            },
            'summary': {
                'total_checks': len(self.results),
                'passed_checks': sum(1 for r in self.results.values() if r['success']),
                'failed_checks': sum(1 for r in self.results.values() if not r['success']),
                'total_errors': sum(len(r['errors']) for r in self.results.values()),
                'total_warnings': sum(len(r['warnings']) for r in self.results.values()),
            },
            'results': self.results,
        }
        
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, ensure_ascii=False, indent=2)


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='运行文档质量保证检查并生成报告',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        '--root',
        default='.',
        help='项目根目录路径（默认: 当前目录）'
    )
    
    args = parser.parse_args()
    
    # 运行质量保证检查
    runner = QualityAssuranceRunner(args.root)
    success = runner.run_all_checks()
    
    # 返回适当的退出码
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
