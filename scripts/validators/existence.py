"""文档存在性检查器"""

from .base import DocumentValidator


class DocumentExistenceChecker(DocumentValidator):
    """文档存在性检查器"""
    
    # 必需的文档文件
    REQUIRED_DOCS = {
        "getting-started": [
            "docs/zh/getting-started/installation.md",
            "docs/zh/getting-started/quickstart.md",
        ],
        "user-guide": [
            "docs/zh/user-guide/user-guide.md",
            "docs/zh/user-guide/api-reference.md",
            "docs/zh/user-guide/configuration.md",
            "docs/zh/user-guide/examples.md",
        ],
        "development": [
            "docs/zh/development/architecture.md",
            "docs/zh/development/development-guide.md",
            "docs/zh/development/contributing.md",
            "docs/zh/development/code-style.md",
        ],
        "advanced": [
            "docs/zh/advanced/design-principles.md",
            "docs/zh/advanced/performance.md",
            "docs/zh/advanced/troubleshooting.md",
            "docs/zh/advanced/faq.md",
        ],
        "versions": [
            "docs/zh/versions/comparison.md",
            "docs/zh/versions/anthropic-1p.md",
            "docs/zh/versions/bedrock-anthropic.md",
            "docs/zh/versions/bedrock-boto3.md",
        ],
        "root": [
            "README.md",
            "README_EN.md",
        ]
    }
    
    # 必需的目录结构
    REQUIRED_DIRS = [
        "docs/zh",
        "docs/zh/getting-started",
        "docs/zh/user-guide",
        "docs/zh/development",
        "docs/zh/advanced",
        "docs/zh/versions",
    ]
    
    def check(self) -> bool:
        """执行文档存在性检查"""
        self._check_directories()
        self._check_documents()
        return self.print_report("文档存在性检查报告")
    
    def _check_directories(self):
        """检查目录结构"""
        for dir_path in self.REQUIRED_DIRS:
            full_path = self.root_dir / dir_path
            if not full_path.exists():
                self.add_error(f"缺失目录: {dir_path}")
            elif not full_path.is_dir():
                self.add_error(f"路径不是目录: {dir_path}")
    
    def _check_documents(self):
        """检查文档文件"""
        for category, docs in self.REQUIRED_DOCS.items():
            for doc_path in docs:
                full_path = self.root_dir / doc_path
                if not full_path.exists():
                    self.add_error(f"缺失文档 [{category}]: {doc_path}")
                elif not full_path.is_file():
                    self.add_error(f"路径不是文件 [{category}]: {doc_path}")
                elif full_path.stat().st_size == 0:
                    self.add_warning(f"文档为空 [{category}]: {doc_path}")
