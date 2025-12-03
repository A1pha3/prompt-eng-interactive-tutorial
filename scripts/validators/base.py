"""文档验证基类"""

from pathlib import Path
from typing import List


class DocumentValidator:
    """文档验证基类"""
    
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir)
        self.errors: List[str] = []
        self.warnings: List[str] = []
        
    def add_error(self, message: str):
        """添加错误信息"""
        self.errors.append(message)
        
    def add_warning(self, message: str):
        """添加警告信息"""
        self.warnings.append(message)
        
    def print_report(self, title: str) -> bool:
        """打印验证报告"""
        print(f"\n{'='*60}")
        print(f"{title}")
        print(f"{'='*60}\n")
        
        if not self.errors and not self.warnings:
            print("✓ 所有检查通过！")
            return True
        
        if self.errors:
            print(f"❌ 发现 {len(self.errors)} 个错误：")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
            print()
            
        if self.warnings:
            print(f"⚠️  发现 {len(self.warnings)} 个警告：")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
            print()
            
        return len(self.errors) == 0
