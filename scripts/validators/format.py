"""Markdown 格式检查器"""

import re
from pathlib import Path
from .base import DocumentValidator


class MarkdownFormatChecker(DocumentValidator):
    """Markdown 格式检查器"""
    
    def check(self) -> bool:
        """执行 Markdown 格式检查"""
        self._check_markdown_format()
        return self.print_report("Markdown 格式检查报告")
    
    def _check_markdown_format(self):
        """检查所有文档的 Markdown 格式"""
        docs_dir = self.root_dir / "docs" / "zh"
        if not docs_dir.exists():
            return
        
        for doc_path in docs_dir.rglob("*.md"):
            try:
                content = doc_path.read_text(encoding='utf-8')
                self._validate_markdown(doc_path, content)
            except Exception as e:
                self.add_error(f"读取文档失败 {doc_path}: {e}")
    
    def _validate_markdown(self, doc_path: Path, content: str):
        """验证 Markdown 格式"""
        lines = content.split('\n')
        
        for i, line in enumerate(lines, 1):
            # 检查标题格式
            if line.startswith('#'):
                self._check_heading_format(doc_path, i, line)
            
            # 检查列表格式
            if re.match(r'^\s*[-*+]\s', line):
                self._check_list_format(doc_path, i, line)
        
        # 检查代码块配对
        self._check_code_block_pairing(doc_path, content)
    
    def _check_heading_format(self, doc_path: Path, line_num: int, line: str):
        """检查标题格式"""
        # 检查标题后是否有空格
        if not re.match(r'^#+\s+\S', line):
            self.add_warning(
                f"文档 {doc_path.relative_to(self.root_dir)} "
                f"行 {line_num}: 标题格式不规范（# 后应有空格）"
            )
        
        # 检查标题层级
        match = re.match(r'^(#+)', line)
        if match:
            level = len(match.group(1))
            if level > 6:
                self.add_error(
                    f"文档 {doc_path.relative_to(self.root_dir)} "
                    f"行 {line_num}: 标题层级过深（最多 6 级）"
                )
    
    def _check_list_format(self, doc_path: Path, line_num: int, line: str):
        """检查列表格式"""
        # 检查列表项后是否有空格
        if not re.match(r'^\s*[-*+]\s+\S', line):
            self.add_warning(
                f"文档 {doc_path.relative_to(self.root_dir)} "
                f"行 {line_num}: 列表格式不规范（标记后应有空格）"
            )
    
    def _check_code_block_pairing(self, doc_path: Path, content: str):
        """检查代码块是否配对"""
        backticks = re.findall(r'^```', content, re.MULTILINE)
        if len(backticks) % 2 != 0:
            self.add_error(
                f"文档 {doc_path.relative_to(self.root_dir)} "
                f"代码块未正确闭合（``` 数量不匹配）"
            )
