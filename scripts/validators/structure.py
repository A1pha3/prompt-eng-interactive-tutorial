"""文档结构一致性检查器"""

import re
from pathlib import Path
from typing import Dict
from .base import DocumentValidator


class DocumentStructureChecker(DocumentValidator):
    """文档结构一致性检查器"""
    
    def check(self) -> bool:
        """执行文档结构一致性检查"""
        self._check_structure_consistency()
        return self.print_report("文档结构一致性检查报告")
    
    def _check_structure_consistency(self):
        """检查同类文档的结构一致性"""
        categories = ["getting-started", "user-guide", "development", "advanced", "versions"]
        
        for category in categories:
            category_dir = self.root_dir / "docs" / "zh" / category
            if not category_dir.exists():
                continue
            
            docs = list(category_dir.glob("*.md"))
            if len(docs) < 2:
                continue  # 少于2个文档无需比较
            
            structures = {}
            for doc_path in docs:
                try:
                    content = doc_path.read_text(encoding='utf-8')
                    structure = self._extract_structure(content)
                    structures[doc_path.name] = structure
                except Exception as e:
                    self.add_error(f"读取文档失败 {doc_path}: {e}")
            
            self._compare_structures(category, structures)
    
    def _extract_structure(self, content: str) -> Dict[str, any]:
        """提取文档结构"""
        headings = re.findall(r'^(#+)\s+(.+)$', content, re.MULTILINE)
        
        structure = {
            'heading_levels': [len(h[0]) for h in headings],
            'heading_count': len(headings),
            'max_level': max([len(h[0]) for h in headings]) if headings else 0,
            'has_title': content.strip().startswith('#') if content.strip() else False,
        }
        
        return structure
    
    def _compare_structures(self, category: str, structures: Dict[str, Dict]):
        """比较文档结构"""
        if not structures:
            return
        
        # 检查是否所有文档都有标题
        docs_without_title = [
            name for name, struct in structures.items()
            if not struct['has_title']
        ]
        if docs_without_title:
            self.add_warning(
                f"类别 [{category}] 中以下文档缺少主标题: "
                f"{', '.join(docs_without_title)}"
            )
        
        # 检查标题层级是否一致
        max_levels = [struct['max_level'] for struct in structures.values()]
        if len(set(max_levels)) > 1:
            self.add_warning(
                f"类别 [{category}] 中文档的标题层级深度不一致: "
                f"{dict(zip(structures.keys(), max_levels))}"
            )
