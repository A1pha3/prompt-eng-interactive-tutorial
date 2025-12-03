"""文档内容完整性检查器"""

import re
from pathlib import Path
from typing import List
from .base import DocumentValidator


class DocumentContentChecker(DocumentValidator):
    """文档内容完整性检查器"""
    
    # 各类文档必需的章节
    REQUIRED_SECTIONS = {
        "getting-started": {
            "installation.md": ["概述", "前置条件", "安装步骤"],
            "quickstart.md": ["概述", "快速开始"],
        },
        "user-guide": {
            "user-guide.md": ["概述", "章节"],
            "api-reference.md": ["概述"],
            "configuration.md": ["概述", "配置"],
            "examples.md": ["概述", "示例"],
        },
        "development": {
            "architecture.md": ["概述", "架构"],
            "development-guide.md": ["概述", "开发环境"],
            "contributing.md": ["概述", "贡献"],
            "code-style.md": ["概述", "代码规范"],
        },
        "advanced": {
            "design-principles.md": ["概述", "设计原理"],
            "performance.md": ["概述", "性能"],
            "troubleshooting.md": ["概述", "问题"],
            "faq.md": ["概述", "问题"],
        },
        "versions": {
            "comparison.md": ["概述", "版本对比"],
            "anthropic-1p.md": ["概述", "特点"],
            "bedrock-anthropic.md": ["概述", "特点"],
            "bedrock-boto3.md": ["概述", "特点"],
        }
    }
    
    def check(self) -> bool:
        """执行文档内容完整性检查"""
        self._check_document_content()
        return self.print_report("文档内容完整性检查报告")
    
    def _check_document_content(self):
        """检查文档内容"""
        for category, docs in self.REQUIRED_SECTIONS.items():
            for doc_name, required_sections in docs.items():
                doc_path = self.root_dir / "docs" / "zh" / category / doc_name
                
                if not doc_path.exists():
                    continue  # 存在性检查会处理
                
                try:
                    content = doc_path.read_text(encoding='utf-8')
                    self._check_sections(doc_path, content, required_sections)
                    self._check_metadata(doc_path, content)
                except Exception as e:
                    self.add_error(f"读取文档失败 {doc_path}: {e}")
    
    def _check_sections(self, doc_path: Path, content: str, required_sections: List[str]):
        """检查必需章节"""
        # 提取所有标题
        headings = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        headings_lower = [h.lower() for h in headings]
        
        for section in required_sections:
            # 检查是否存在包含该关键词的标题
            found = any(section.lower() in heading for heading in headings_lower)
            if not found:
                self.add_warning(
                    f"文档 {doc_path.relative_to(self.root_dir)} "
                    f"可能缺少章节: {section}"
                )
    
    def _check_metadata(self, doc_path: Path, content: str):
        """检查文档元数据"""
        # 检查文档是否有标题
        if not content.strip():
            return
            
        lines = content.strip().split('\n')
        if not lines[0].startswith('#'):
            self.add_warning(
                f"文档 {doc_path.relative_to(self.root_dir)} "
                f"缺少主标题"
            )
        
        # 检查文档长度
        if len(content) < 100:
            self.add_warning(
                f"文档 {doc_path.relative_to(self.root_dir)} "
                f"内容过短 ({len(content)} 字符)"
            )
