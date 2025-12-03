"""术语一致性检查器"""

import re
from pathlib import Path
from typing import Dict
from .base import DocumentValidator


class TerminologyChecker(DocumentValidator):
    """术语一致性检查器"""
    
    def __init__(self, root_dir: str = "."):
        super().__init__(root_dir)
        self.glossary = self._load_glossary()
    
    def _load_glossary(self) -> Dict[str, str]:
        """加载术语表"""
        glossary = {}
        
        # 从需求文档加载术语表
        req_path = self.root_dir / ".kiro/specs/comprehensive-chinese-documentation/requirements.md"
        if req_path.exists():
            try:
                content = req_path.read_text(encoding='utf-8')
                # 提取术语表部分
                match = re.search(r'## 术语表\n\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
                if match:
                    glossary_text = match.group(1)
                    # 解析术语定义
                    terms = re.findall(r'-\s+\*\*(.+?)（(.+?)）\*\*', glossary_text)
                    for zh_term, en_term in terms:
                        glossary[zh_term] = en_term
            except Exception as e:
                self.add_warning(f"加载术语表失败: {e}")
        
        return glossary
    
    def check(self) -> bool:
        """执行术语一致性检查"""
        if not self.glossary:
            self.add_warning("未找到术语表，跳过术语一致性检查")
            return self.print_report("术语一致性检查报告")
        
        self._check_terminology_usage()
        return self.print_report("术语一致性检查报告")
    
    def _check_terminology_usage(self):
        """检查术语使用一致性"""
        docs_dir = self.root_dir / "docs" / "zh"
        if not docs_dir.exists():
            return
        
        term_usage = {term: [] for term in self.glossary.keys()}
        
        for doc_path in docs_dir.rglob("*.md"):
            try:
                content = doc_path.read_text(encoding='utf-8')
                
                for term in self.glossary.keys():
                    # 统计术语出现次数
                    count = content.count(term)
                    if count > 0:
                        term_usage[term].append((doc_path, count))
                
            except Exception as e:
                self.add_error(f"读取文档失败 {doc_path}: {e}")
        
        # 报告术语使用情况
        for term, usage in term_usage.items():
            if not usage:
                self.add_warning(f"术语 '{term}' 在文档中未被使用")
