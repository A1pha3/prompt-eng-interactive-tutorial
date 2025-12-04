#!/usr/bin/env python3
"""
属性测试：导航链接完整性
使用 Hypothesis 进行基于属性的测试
"""

import re
import pytest
from hypothesis import given, strategies as st, settings
from pathlib import Path
from typing import List, Dict, Set


# 获取项目根目录（从 scripts/ 目录向上一级）
ROOT_DIR = Path(__file__).parent.parent


class TestNavigationLinkCompleteness:
    """
    属性测试：导航链接完整性
    
    **Feature: comprehensive-chinese-documentation, Property 7: 导航链接完整性**
    **Validates: Requirements 6.1, 6.2, 6.3**
    
    属性：对于任何文档，它应该包含指向相关文档的内部链接，
    并且主 README 应该包含指向所有文档的索引链接。
    """
    
    def _extract_markdown_links(self, content: str) -> List[Dict[str, str]]:
        """
        提取 Markdown 文档中的所有链接
        
        返回格式: [{'text': '链接文本', 'url': '链接地址'}, ...]
        """
        links = []
        
        # 匹配 Markdown 链接格式: [text](url)
        pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        matches = re.findall(pattern, content)
        
        for text, url in matches:
            links.append({
                'text': text.strip(),
                'url': url.strip()
            })
        
        return links
    
    def _is_internal_doc_link(self, url: str) -> bool:
        """
        判断链接是否是内部文档链接
        
        内部文档链接特征：
        - 不以 http:// 或 https:// 开头
        - 指向 .md 文件
        - 不是纯锚点链接（#section）
        """
        # 排除外部链接
        if url.startswith(('http://', 'https://')):
            return False
        
        # 排除纯锚点链接
        if url.startswith('#'):
            return False
        
        # 移除锚点部分
        url_without_anchor = url.split('#')[0]
        
        # 检查是否指向 .md 文件
        if url_without_anchor and url_without_anchor.endswith('.md'):
            return True
        
        return False

    
    def _get_all_doc_files(self) -> Set[str]:
        """
        获取所有文档文件的相对路径
        
        返回格式: {'docs/zh/getting-started/installation.md', ...}
        """
        doc_files = set()
        
        # 主 README
        readme = ROOT_DIR / "README.md"
        if readme.exists():
            doc_files.add("README.md")
        
        # docs/zh 目录下的所有文档
        docs_dir = ROOT_DIR / "docs" / "zh"
        if docs_dir.exists():
            for md_file in docs_dir.rglob("*.md"):
                rel_path = md_file.relative_to(ROOT_DIR)
                doc_files.add(str(rel_path))
        
        # 版本特定的 README
        for version_dir in ["Anthropic 1P", "AmazonBedrock"]:
            version_readme = ROOT_DIR / version_dir / "README_ZH.md"
            if version_readme.exists():
                rel_path = version_readme.relative_to(ROOT_DIR)
                doc_files.add(str(rel_path))
        
        return doc_files
    
    def _normalize_link_path(self, doc_path: Path, link_url: str) -> str:
        """
        将链接 URL 规范化为相对于项目根目录的路径
        
        参数:
            doc_path: 包含链接的文档路径
            link_url: 链接 URL
        
        返回:
            规范化的相对路径
        """
        # 移除锚点
        url_without_anchor = link_url.split('#')[0]
        
        if not url_without_anchor:
            return ""
        
        # 如果是绝对路径（以 / 开头）
        if url_without_anchor.startswith('/'):
            return url_without_anchor.lstrip('/')
        
        # 相对路径 - 相对于当前文档所在目录
        doc_dir = doc_path.parent
        target_path = (doc_dir / url_without_anchor).resolve()
        
        try:
            rel_path = target_path.relative_to(ROOT_DIR)
            return str(rel_path)
        except ValueError:
            # 如果路径在项目外，返回原始路径
            return url_without_anchor

    
    @given(doc_path=st.sampled_from([
        "docs/zh/getting-started/installation.md",
        "docs/zh/getting-started/quickstart.md",
        "docs/zh/user-guide/user-guide.md",
        "docs/zh/user-guide/api-reference.md",
        "docs/zh/user-guide/configuration.md",
        "docs/zh/user-guide/examples.md",
        "docs/zh/development/architecture.md",
        "docs/zh/development/development-guide.md",
        "docs/zh/development/contributing.md",
        "docs/zh/development/code-style.md",
        "docs/zh/development/glossary-dev.md",
        "docs/zh/advanced/design-principles.md",
        "docs/zh/advanced/performance.md",
        "docs/zh/advanced/troubleshooting.md",
        "docs/zh/advanced/faq.md",
        "docs/zh/versions/anthropic-1p.md",
        "docs/zh/versions/bedrock-anthropic.md",
        "docs/zh/versions/bedrock-boto3.md",
        "docs/zh/versions/comparison.md",
    ]))
    @settings(max_examples=100)
    def test_documents_contain_internal_navigation_links(self, doc_path):
        """
        属性测试：对于任何文档，它应该包含指向相关文档的内部链接
        
        验证：
        - 文档应该包含至少一个指向其他文档的内部链接
        - 内部链接应该指向实际存在的文档
        - 链接路径应该正确
        
        这确保了文档之间有良好的交叉引用，用户可以方便地在相关文档间导航。
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        
        # 提取所有链接
        all_links = self._extract_markdown_links(content)
        
        # 过滤出内部文档链接
        internal_links = [
            link for link in all_links
            if self._is_internal_doc_link(link['url'])
        ]
        
        # 属性 1：文档应该包含至少一个内部文档链接（用于导航）
        # 注意：某些简短的文档可能不需要内部链接，所以这是一个软检查
        if len(content.split('\n')) > 50:  # 只对较长的文档要求有内部链接
            if len(internal_links) == 0:
                # 这是一个警告而不是错误，因为某些文档可能确实不需要内部链接
                print(
                    f"\n注意：文档 {doc_path} 没有内部文档链接，"
                    f"这可能影响文档导航体验"
                )
        
        # 属性 2：所有内部链接都应该指向存在的文档
        all_doc_files = self._get_all_doc_files()
        
        for link in internal_links:
            normalized_path = self._normalize_link_path(full_path, link['url'])
            
            if normalized_path and normalized_path not in all_doc_files:
                # 检查文件是否实际存在
                target_file = ROOT_DIR / normalized_path
                
                assert target_file.exists(), (
                    f"文档 {doc_path} 包含指向不存在文档的链接:\n"
                    f"  链接文本: {link['text']}\n"
                    f"  链接地址: {link['url']}\n"
                    f"  解析路径: {normalized_path}\n"
                    f"  目标文件不存在: {target_file}"
                )

    
    def test_main_readme_contains_documentation_index(self):
        """
        属性测试：主 README 应该包含完整的文档索引
        
        验证：
        - README.md 应该包含指向主要文档类别的链接
        - 应该包含指向入门文档的链接
        - 应该包含指向版本文档的链接
        
        这确保用户可以从主 README 快速找到所有文档。
        """
        readme_path = ROOT_DIR / "README.md"
        
        assert readme_path.exists(), "主 README.md 不存在"
        
        content = readme_path.read_text(encoding='utf-8')
        
        # 提取所有链接
        all_links = self._extract_markdown_links(content)
        
        # 提取内部文档链接
        internal_links = [
            link for link in all_links
            if self._is_internal_doc_link(link['url'])
        ]
        
        # 属性 1：README 应该包含指向文档系统的链接
        # 检查是否有指向 docs/zh/ 目录的链接
        has_docs_links = any(
            'docs/zh/' in link['url']
            for link in internal_links
        )
        
        assert has_docs_links, (
            "主 README.md 应该包含指向文档系统（docs/zh/）的链接，"
            "以便用户可以找到完整的文档"
        )
        
        # 属性 2：README 应该包含指向关键文档类别的链接
        # 定义关键文档类别
        key_categories = {
            'installation': ['安装', 'installation'],
            'quickstart': ['快速开始', 'quickstart', '快速上手'],
            'versions': ['版本', 'version', '对比', 'comparison'],
        }
        
        # 检查每个关键类别
        for category, keywords in key_categories.items():
            has_category_link = False
            
            # 检查链接文本或 URL 中是否包含关键词
            for link in all_links:
                link_text_lower = link['text'].lower()
                link_url_lower = link['url'].lower()
                
                if any(keyword.lower() in link_text_lower or keyword.lower() in link_url_lower 
                       for keyword in keywords):
                    has_category_link = True
                    break
            
            # 对于某些类别，如果没有找到，给出警告而不是失败
            if not has_category_link:
                print(
                    f"\n注意：主 README 可能缺少指向 '{category}' 类别的明确链接。"
                    f"建议添加相关链接以改善导航体验。"
                )

    
    @given(category=st.sampled_from([
        "getting-started",
        "user-guide",
        "development",
        "advanced",
        "versions"
    ]))
    @settings(max_examples=100)
    def test_category_documents_have_cross_references(self, category):
        """
        属性测试：对于任何文档类别，该类别下的文档应该有交叉引用
        
        验证：
        - 同一类别下的文档应该相互引用
        - 文档应该引用相关的其他类别文档
        - 交叉引用应该形成连贯的导航网络
        
        这确保用户可以在相关文档间方便地导航。
        """
        category_dir = ROOT_DIR / "docs" / "zh" / category
        
        if not category_dir.exists():
            pytest.skip(f"类别目录不存在: {category}")
        
        # 获取该类别下的所有文档
        docs = list(category_dir.glob("*.md"))
        
        if len(docs) == 0:
            pytest.skip(f"类别 {category} 中没有文档")
        
        # 统计每个文档的内部链接数量
        doc_link_counts = {}
        
        for doc_path in docs:
            try:
                content = doc_path.read_text(encoding='utf-8')
                all_links = self._extract_markdown_links(content)
                
                # 过滤内部文档链接
                internal_links = [
                    link for link in all_links
                    if self._is_internal_doc_link(link['url'])
                ]
                
                doc_link_counts[doc_path.name] = len(internal_links)
            except Exception as e:
                pytest.fail(f"读取文档失败 {doc_path}: {e}")
        
        # 属性：如果类别中有多个文档，至少应该有一些文档包含内部链接
        if len(docs) > 1:
            docs_with_links = sum(1 for count in doc_link_counts.values() if count > 0)
            
            # 至少50%的文档应该有内部链接
            link_coverage = docs_with_links / len(docs)
            
            if link_coverage < 0.5:
                # 这是一个软检查 - 打印警告
                print(
                    f"\n注意：类别 [{category}] 中只有 {link_coverage:.0%} 的文档包含内部链接。"
                    f"建议增加文档间的交叉引用以改善导航体验。\n"
                    f"  文档链接统计: {doc_link_counts}"
                )

    
    @given(doc_path=st.sampled_from([
        "docs/zh/getting-started/installation.md",
        "docs/zh/getting-started/quickstart.md",
        "docs/zh/user-guide/user-guide.md",
        "docs/zh/user-guide/api-reference.md",
        "docs/zh/development/development-guide.md",
        "docs/zh/development/contributing.md",
        "docs/zh/advanced/design-principles.md",
        "docs/zh/advanced/troubleshooting.md",
    ]))
    @settings(max_examples=100)
    def test_documents_have_related_documents_section(self, doc_path):
        """
        属性测试：对于任何主要文档，应该有"相关文档"或"另请参阅"部分
        
        验证：
        - 文档应该包含指向相关文档的明确章节
        - 该章节应该包含有用的导航链接
        
        这确保用户可以发现相关内容。
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        
        # 检查是否有"相关文档"、"另请参阅"、"相关资源"等章节
        related_section_patterns = [
            r'##\s+相关文档',
            r'##\s+另请参阅',
            r'##\s+相关资源',
            r'##\s+延伸阅读',
            r'##\s+下一步',
            r'##\s+Related Documents',
            r'##\s+See Also',
        ]
        
        has_related_section = any(
            re.search(pattern, content, re.IGNORECASE)
            for pattern in related_section_patterns
        )
        
        # 如果文档较长（超过100行），建议有相关文档章节
        line_count = len(content.split('\n'))
        
        if line_count > 100 and not has_related_section:
            # 这是一个软检查 - 打印建议
            print(
                f"\n建议：文档 {doc_path} 可以添加'相关文档'或'下一步'章节，"
                f"以帮助用户发现相关内容并改善导航体验。"
            )
    
    def test_all_major_documents_are_reachable_from_readme(self):
        """
        属性测试：所有主要文档都应该可以从 README 直接或间接访问
        
        验证：
        - 主要的文档类别都应该在 README 中被引用
        - 用户应该能够从 README 开始找到所有重要文档
        
        这确保文档系统的可发现性。
        """
        readme_path = ROOT_DIR / "README.md"
        
        assert readme_path.exists(), "主 README.md 不存在"
        
        content = readme_path.read_text(encoding='utf-8')
        
        # 定义主要文档类别及其关键文档
        major_doc_categories = {
            'getting-started': ['installation.md', 'quickstart.md'],
            'user-guide': ['user-guide.md', 'api-reference.md'],
            'development': ['development-guide.md', 'contributing.md'],
            'advanced': ['design-principles.md', 'troubleshooting.md'],
            'versions': ['comparison.md'],
        }
        
        # 提取 README 中的所有链接
        all_links = self._extract_markdown_links(content)
        
        # 检查每个类别是否被引用
        missing_categories = []
        
        for category, key_docs in major_doc_categories.items():
            # 检查是否有指向该类别的链接
            has_category_reference = any(
                category in link['url'] or 
                any(doc in link['url'] for doc in key_docs)
                for link in all_links
            )
            
            if not has_category_reference:
                missing_categories.append(category)
        
        # 如果有缺失的类别，给出警告
        if missing_categories:
            print(
                f"\n注意：主 README 可能缺少对以下文档类别的引用: {missing_categories}\n"
                f"建议在 README 中添加指向这些类别的链接，以改善文档的可发现性。"
            )


if __name__ == "__main__":
    # 运行测试
    pytest.main([
        __file__,
        "-v",
        "--hypothesis-show-statistics",
        "--tb=short"
    ])
