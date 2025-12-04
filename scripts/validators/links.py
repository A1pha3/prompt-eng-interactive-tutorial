"""链接验证器"""

import re
from pathlib import Path
from .base import DocumentValidator


class LinkValidator(DocumentValidator):
    """链接验证器"""
    
    def check(self) -> bool:
        """执行链接验证"""
        self._check_links()
        return self.print_report("链接验证报告")
    
    def _check_links(self):
        """检查所有文档中的链接"""
        docs_dir = self.root_dir / "docs" / "zh"
        if not docs_dir.exists():
            return
        
        # 同时检查根目录的 README
        all_docs = list(docs_dir.rglob("*.md"))
        readme = self.root_dir / "README.md"
        if readme.exists():
            all_docs.append(readme)
        
        for doc_path in all_docs:
            try:
                content = doc_path.read_text(encoding='utf-8')
                self._validate_links(doc_path, content)
            except Exception as e:
                self.add_error(f"读取文档失败 {doc_path}: {e}")
    
    def _validate_links(self, doc_path: Path, content: str):
        """验证文档中的链接"""
        # 跳过模板文件
        if 'template' in doc_path.name.lower() or 'templates' in str(doc_path):
            return
        
        # 提取 Markdown 链接 [text](url)
        md_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)
        
        for link_text, link_url in md_links:
            # 跳过锚点链接
            if link_url.startswith('#'):
                continue
            
            # 跳过 mailto 链接
            if link_url.startswith('mailto:'):
                continue
            
            # 跳过 ftp 链接
            if link_url.startswith('ftp://'):
                continue
            
            # 检查外部链接格式
            if link_url.startswith(('http://', 'https://')):
                # 外部链接 - 只检查格式
                if not re.match(r'https?://[^\s]+', link_url):
                    self.add_error(
                        f"文档 {doc_path.relative_to(self.root_dir)} "
                        f"包含格式错误的外部链接: {link_url}"
                    )
            else:
                # 内部链接 - 检查文件是否存在
                self._check_internal_link(doc_path, link_url)
    
    def _check_internal_link(self, doc_path: Path, link_url: str):
        """检查内部链接"""
        # 移除锚点
        link_path = link_url.split('#')[0]
        if not link_path:
            return
        
        # 解析相对路径
        if link_path.startswith('/'):
            # 绝对路径（相对于仓库根目录）
            target_path = self.root_dir / link_path.lstrip('/')
        else:
            # 相对路径
            target_path = (doc_path.parent / link_path).resolve()
        
        # 检查目标文件是否存在
        if not target_path.exists():
            self.add_error(
                f"文档 {doc_path.relative_to(self.root_dir)} "
                f"包含失效的内部链接: {link_url} "
                f"(目标不存在: {target_path})"
            )
