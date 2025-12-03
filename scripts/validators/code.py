"""代码示例验证器"""

import re
from pathlib import Path
from .base import DocumentValidator


class CodeExampleValidator(DocumentValidator):
    """代码示例验证器"""
    
    def check(self) -> bool:
        """执行代码示例验证"""
        self._check_code_examples()
        return self.print_report("代码示例验证报告")
    
    def _check_code_examples(self):
        """检查所有文档中的代码示例"""
        docs_dir = self.root_dir / "docs" / "zh"
        if not docs_dir.exists():
            return
        
        for doc_path in docs_dir.rglob("*.md"):
            try:
                content = doc_path.read_text(encoding='utf-8')
                self._validate_code_blocks(doc_path, content)
            except Exception as e:
                self.add_error(f"读取文档失败 {doc_path}: {e}")
    
    def _validate_code_blocks(self, doc_path: Path, content: str):
        """验证文档中的代码块"""
        # 提取代码块
        code_blocks = re.findall(
            r'```(\w+)?\n(.*?)```',
            content,
            re.DOTALL
        )
        
        for i, (language, code) in enumerate(code_blocks, 1):
            if not language:
                self.add_warning(
                    f"文档 {doc_path.relative_to(self.root_dir)} "
                    f"代码块 #{i} 未指定语言"
                )
                continue
            
            # 验证 Python 代码语法
            if language.lower() in ['python', 'py']:
                self._validate_python_syntax(doc_path, i, code)
            
            # 检查代码块是否为空
            if not code.strip():
                self.add_warning(
                    f"文档 {doc_path.relative_to(self.root_dir)} "
                    f"代码块 #{i} 为空"
                )
    
    def _validate_python_syntax(self, doc_path: Path, block_num: int, code: str):
        """验证 Python 代码语法"""
        try:
            compile(code, f"<{doc_path}>", 'exec')
        except SyntaxError as e:
            self.add_error(
                f"文档 {doc_path.relative_to(self.root_dir)} "
                f"代码块 #{block_num} 存在语法错误: {e.msg} (行 {e.lineno})"
            )
        except Exception as e:
            # 其他编译错误（如缩进问题）
            self.add_warning(
                f"文档 {doc_path.relative_to(self.root_dir)} "
                f"代码块 #{block_num} 可能存在问题: {e}"
            )
