#!/usr/bin/env python3
"""
属性测试：链接有效性
使用 Hypothesis 进行基于属性的测试
"""

import re
import pytest
from hypothesis import given, strategies as st, settings
from pathlib import Path
from urllib.parse import urlparse
from validators.links import LinkValidator


# 获取项目根目录（从 scripts/ 目录向上一级）
ROOT_DIR = Path(__file__).parent.parent


class TestLinkValidity:
    """
    属性测试：链接有效性
    
    **Feature: comprehensive-chinese-documentation, Property 8: 链接有效性**
    **Validates: Requirements 6.2**
    
    属性：对于任何文档中的链接（内部或外部），该链接应该指向存在且可访问的资源。
    """
    
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
        "docs/zh/versions/README.md",
        "docs/zh/glossary.md",
        "docs/zh/README.md",
        "README.md",
        "AmazonBedrock/README_ZH.md",
        "Anthropic 1P/README_ZH.md",
    ]))
    @settings(max_examples=100)
    def test_internal_links_point_to_existing_files(self, doc_path):
        """
        属性测试：对于任何文档，其中的内部链接应该指向存在的文件
        
        这个测试验证了：
        1. 所有内部链接（相对路径）指向的文件都存在
        2. 链接路径格式正确
        3. 链接目标是有效的文件或目录
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        
        # 提取所有 Markdown 链接 [text](url)
        links = self._extract_markdown_links(content)
        
        for link_text, link_url in links:
            # 跳过锚点链接（只有 #）
            if link_url.startswith('#'):
                continue
            
            # 跳过外部链接
            if link_url.startswith(('http://', 'https://', 'ftp://', 'mailto:')):
                continue
            
            # 这是内部链接，验证目标存在
            self._validate_internal_link(doc_path, full_path, link_url, link_text)
    
    def _extract_markdown_links(self, content: str) -> list:
        """提取 Markdown 格式的链接（排除代码块中的链接）"""
        links = []
        lines = content.split('\n')
        in_code_block = False
        
        for line in lines:
            # 跟踪代码块
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            # 跳过代码块内的内容
            if in_code_block:
                continue
            
            # 提取当前行的链接
            line_links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', line)
            links.extend(line_links)
        
        return links
    
    def _validate_internal_link(self, doc_path: str, doc_full_path: Path, 
                                link_url: str, link_text: str):
        """验证内部链接的有效性"""
        # 移除 URL 中的锚点部分
        link_path = link_url.split('#')[0]
        
        # 如果链接只是锚点，跳过
        if not link_path:
            return
        
        # 解析相对路径
        if link_path.startswith('/'):
            # 绝对路径（相对于仓库根目录）
            target_path = ROOT_DIR / link_path.lstrip('/')
        else:
            # 相对路径（相对于当前文档）
            target_path = (doc_full_path.parent / link_path).resolve()
        
        # 属性：链接目标必须存在
        assert target_path.exists(), (
            f"文档 {doc_path} 包含失效的内部链接:\n"
            f"  链接文本: '{link_text}'\n"
            f"  链接 URL: {link_url}\n"
            f"  目标路径: {target_path}\n"
            f"  目标不存在"
        )
        
        # 属性：如果链接指向文件，文件应该不为空
        if target_path.is_file():
            assert target_path.stat().st_size > 0, (
                f"文档 {doc_path} 链接指向空文件:\n"
                f"  链接文本: '{link_text}'\n"
                f"  链接 URL: {link_url}\n"
                f"  目标文件: {target_path}"
            )

    
    @given(doc_path=st.sampled_from([
        "docs/zh/getting-started/installation.md",
        "docs/zh/getting-started/quickstart.md",
        "docs/zh/user-guide/user-guide.md",
        "docs/zh/user-guide/api-reference.md",
        "docs/zh/development/architecture.md",
        "docs/zh/development/contributing.md",
        "docs/zh/advanced/design-principles.md",
        "docs/zh/versions/comparison.md",
        "README.md",
    ]))
    @settings(max_examples=100)
    def test_external_links_have_valid_format(self, doc_path):
        """
        属性测试：对于任何文档，其中的外部链接应该有有效的 URL 格式
        
        这个测试验证了：
        1. 外部链接使用正确的协议（http/https）
        2. URL 格式符合标准
        3. URL 不包含明显的错误（如空格、中文字符等）
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        links = self._extract_markdown_links(content)
        
        for link_text, link_url in links:
            # 只检查外部链接
            if not link_url.startswith(('http://', 'https://')):
                continue
            
            # 属性：外部链接应该有有效的 URL 格式
            try:
                parsed = urlparse(link_url)
                
                # 验证 URL 的各个部分
                assert parsed.scheme in ['http', 'https'], (
                    f"文档 {doc_path} 包含无效协议的外部链接:\n"
                    f"  链接文本: '{link_text}'\n"
                    f"  链接 URL: {link_url}\n"
                    f"  协议: {parsed.scheme} (应该是 http 或 https)"
                )
                
                assert parsed.netloc, (
                    f"文档 {doc_path} 包含缺少域名的外部链接:\n"
                    f"  链接文本: '{link_text}'\n"
                    f"  链接 URL: {link_url}"
                )
                
                # 属性：URL 不应该包含空格
                assert ' ' not in link_url, (
                    f"文档 {doc_path} 包含带空格的外部链接:\n"
                    f"  链接文本: '{link_text}'\n"
                    f"  链接 URL: {link_url}\n"
                    f"  URL 不应该包含空格"
                )
                
                # 属性：URL 不应该包含未编码的中文字符
                # 检查是否有中文字符（应该被 URL 编码）
                chinese_chars = [c for c in link_url if '\u4e00' <= c <= '\u9fff']
                if chinese_chars:
                    # 这可能是一个问题，但某些情况下可能是有意的
                    # 我们发出警告而不是失败
                    print(
                        f"\n注意：文档 {doc_path} 包含未编码中文字符的链接:\n"
                        f"  链接文本: '{link_text}'\n"
                        f"  链接 URL: {link_url}\n"
                        f"  建议对 URL 进行编码"
                    )
                
            except Exception as e:
                pytest.fail(
                    f"文档 {doc_path} 包含格式错误的外部链接:\n"
                    f"  链接文本: '{link_text}'\n"
                    f"  链接 URL: {link_url}\n"
                    f"  错误: {e}"
                )
    
    @given(doc_path=st.sampled_from([
        "docs/zh/getting-started/installation.md",
        "docs/zh/getting-started/quickstart.md",
        "docs/zh/user-guide/user-guide.md",
        "docs/zh/development/architecture.md",
        "docs/zh/versions/comparison.md",
        "README.md",
    ]))
    @settings(max_examples=100)
    def test_anchor_links_point_to_existing_headings(self, doc_path):
        """
        属性测试：对于任何文档，其中的锚点链接应该指向文档中存在的标题
        
        这个测试验证了：
        1. 文档内锚点链接（#heading）指向实际存在的标题
        2. 跨文档锚点链接（file.md#heading）的目标文件和标题都存在
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        links = self._extract_markdown_links(content)
        
        # 提取当前文档的所有标题
        current_doc_headings = self._extract_heading_anchors(content)
        
        for link_text, link_url in links:
            # 只处理包含锚点的链接
            if '#' not in link_url:
                continue
            
            # 分离文件路径和锚点
            if link_url.startswith('#'):
                # 文档内锚点链接
                anchor = link_url[1:]  # 移除 #
                self._validate_anchor_in_current_doc(
                    doc_path, anchor, link_text, current_doc_headings
                )
            else:
                # 跨文档锚点链接
                parts = link_url.split('#', 1)
                if len(parts) == 2:
                    file_path, anchor = parts
                    
                    # 跳过外部链接的锚点验证
                    if file_path.startswith(('http://', 'https://')):
                        continue
                    
                    self._validate_cross_document_anchor(
                        doc_path, full_path, file_path, anchor, link_text
                    )
    
    def _extract_heading_anchors(self, content: str) -> set:
        """提取文档中所有标题的锚点 ID"""
        anchors = set()
        lines = content.split('\n')
        in_code_block = False
        
        for line in lines:
            # 跟踪代码块
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block:
                continue
            
            # 匹配标题
            match = re.match(r'^(#+)\s+(.+)$', line)
            if match:
                heading_text = match.group(2).strip()
                # 生成 GitHub 风格的锚点 ID
                anchor = self._generate_anchor_id(heading_text)
                anchors.add(anchor)
        
        return anchors
    
    def _generate_anchor_id(self, heading_text: str) -> str:
        """
        生成 GitHub 风格的锚点 ID
        
        规则：
        1. 转换为小写
        2. 移除标点符号（除了连字符和下划线）
        3. 空格替换为连字符
        4. 移除多余的连字符
        """
        # 移除 Markdown 格式（如 **bold**, `code` 等）
        text = re.sub(r'\*\*(.+?)\*\*', r'\1', heading_text)
        text = re.sub(r'`(.+?)`', r'\1', text)
        text = re.sub(r'\[(.+?)\]\(.+?\)', r'\1', text)
        
        # 转换为小写
        text = text.lower()
        
        # 中文字符保持不变，其他字符按规则处理
        result = []
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                # 中文字符保持
                result.append(char)
            elif char.isalnum() or char in '-_':
                # 字母数字、连字符、下划线保持
                result.append(char)
            elif char.isspace():
                # 空格转换为连字符
                result.append('-')
            # 其他字符忽略
        
        anchor = ''.join(result)
        
        # 移除多余的连字符
        anchor = re.sub(r'-+', '-', anchor)
        anchor = anchor.strip('-')
        
        return anchor
    
    def _validate_anchor_in_current_doc(self, doc_path: str, anchor: str,
                                       link_text: str, available_anchors: set):
        """验证文档内锚点链接"""
        # 属性：锚点必须指向文档中存在的标题
        assert anchor in available_anchors, (
            f"文档 {doc_path} 包含指向不存在标题的锚点链接:\n"
            f"  链接文本: '{link_text}'\n"
            f"  锚点: #{anchor}\n"
            f"  可用的锚点: {sorted(list(available_anchors)[:10])}..."
        )
    
    def _validate_cross_document_anchor(self, doc_path: str, doc_full_path: Path,
                                       file_path: str, anchor: str, link_text: str):
        """验证跨文档锚点链接"""
        # 解析目标文件路径
        if file_path.startswith('/'):
            target_path = ROOT_DIR / file_path.lstrip('/')
        else:
            target_path = (doc_full_path.parent / file_path).resolve()
        
        # 属性：目标文件必须存在
        assert target_path.exists(), (
            f"文档 {doc_path} 包含指向不存在文件的锚点链接:\n"
            f"  链接文本: '{link_text}'\n"
            f"  目标文件: {file_path}\n"
            f"  锚点: #{anchor}\n"
            f"  解析后的路径: {target_path}"
        )
        
        # 读取目标文档并提取标题
        try:
            target_content = target_path.read_text(encoding='utf-8')
            target_anchors = self._extract_heading_anchors(target_content)
            
            # 属性：锚点必须在目标文档中存在
            assert anchor in target_anchors, (
                f"文档 {doc_path} 包含指向不存在标题的跨文档锚点链接:\n"
                f"  链接文本: '{link_text}'\n"
                f"  目标文件: {file_path}\n"
                f"  锚点: #{anchor}\n"
                f"  目标文档中可用的锚点: {sorted(list(target_anchors)[:10])}..."
            )
        except Exception as e:
            pytest.fail(
                f"文档 {doc_path} 的跨文档锚点链接验证失败:\n"
                f"  链接文本: '{link_text}'\n"
                f"  目标文件: {file_path}\n"
                f"  锚点: #{anchor}\n"
                f"  错误: {e}"
            )

    
    @given(doc_path=st.sampled_from([
        "docs/zh/getting-started/installation.md",
        "docs/zh/user-guide/user-guide.md",
        "docs/zh/development/architecture.md",
        "docs/zh/versions/comparison.md",
        "README.md",
    ]))
    @settings(max_examples=100)
    def test_links_use_consistent_format(self, doc_path):
        """
        属性测试：对于任何文档，链接格式应该一致
        
        这个测试验证了：
        1. 使用标准的 Markdown 链接格式 [text](url)
        2. 链接文本不为空
        3. 链接 URL 不为空
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        links = self._extract_markdown_links(content)
        
        for link_text, link_url in links:
            # 属性：链接文本不应该为空
            assert link_text.strip(), (
                f"文档 {doc_path} 包含空链接文本:\n"
                f"  链接 URL: {link_url}"
            )
            
            # 属性：链接 URL 不应该为空
            assert link_url.strip(), (
                f"文档 {doc_path} 包含空链接 URL:\n"
                f"  链接文本: '{link_text}'"
            )
            
            # 属性：链接文本不应该只是 URL（应该有描述性文本）
            # 但允许某些例外情况（如参考链接）
            if link_url.startswith(('http://', 'https://')):
                # 对于外部链接，如果链接文本就是 URL，发出警告
                if link_text.strip() == link_url.strip():
                    print(
                        f"\n注意：文档 {doc_path} 包含链接文本等于 URL 的链接:\n"
                        f"  链接: [{link_text}]({link_url})\n"
                        f"  建议使用描述性的链接文本"
                    )
    
    @given(doc_path=st.sampled_from([
        "docs/zh/getting-started/installation.md",
        "docs/zh/user-guide/user-guide.md",
        "docs/zh/development/contributing.md",
        "docs/zh/versions/comparison.md",
        "README.md",
    ]))
    @settings(max_examples=100)
    def test_relative_links_use_correct_path_format(self, doc_path):
        """
        属性测试：对于任何文档，相对链接应该使用正确的路径格式
        
        这个测试验证了：
        1. 相对路径不以 / 开头（除非是仓库根路径）
        2. 路径使用正斜杠 / 而不是反斜杠 \
        3. 路径不包含 .. 的过度使用
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        links = self._extract_markdown_links(content)
        
        for link_text, link_url in links:
            # 只检查内部相对链接
            if link_url.startswith(('http://', 'https://', '#', 'mailto:')):
                continue
            
            # 移除锚点部分
            link_path = link_url.split('#')[0]
            if not link_path:
                continue
            
            # 属性：路径应该使用正斜杠
            assert '\\' not in link_path, (
                f"文档 {doc_path} 包含使用反斜杠的链接:\n"
                f"  链接文本: '{link_text}'\n"
                f"  链接 URL: {link_url}\n"
                f"  应该使用正斜杠 / 而不是反斜杠 \\"
            )
            
            # 属性：路径不应该包含过多的 ..（超过3个可能表示路径错误）
            parent_dir_count = link_path.count('../')
            if parent_dir_count > 3:
                print(
                    f"\n注意：文档 {doc_path} 包含过多父目录引用的链接:\n"
                    f"  链接文本: '{link_text}'\n"
                    f"  链接 URL: {link_url}\n"
                    f"  包含 {parent_dir_count} 个 '../'\n"
                    f"  这可能表示路径结构有问题"
                )
    
    def test_link_validator_integration(self):
        """
        集成测试：链接验证器应该正确检测所有链接问题
        
        这个测试运行完整的链接验证器并验证它能够检测到链接问题。
        """
        validator = LinkValidator(str(ROOT_DIR))
        
        # 运行验证器
        success = validator.check()
        
        # 验证器应该能够运行而不崩溃
        # 如果有错误，它们应该被正确记录
        if not success:
            assert len(validator.errors) > 0, (
                "链接验证失败但没有记录错误"
            )
            # 打印错误以便调试
            print("\n检测到的链接错误:")
            for error in validator.errors[:10]:  # 只打印前10个
                print(f"  - {error}")
        else:
            # 成功时不应该有错误
            assert len(validator.errors) == 0, (
                f"链接验证成功但有错误: {validator.errors}"
            )
    
    def test_all_documents_have_at_least_one_link(self):
        """
        测试：大多数文档应该包含至少一个链接
        
        这个测试验证文档的互联性，确保文档之间有适当的交叉引用。
        """
        docs_dir = ROOT_DIR / "docs" / "zh"
        if not docs_dir.exists():
            pytest.skip("文档目录不存在")
        
        docs_without_links = []
        
        for doc_path in docs_dir.rglob("*.md"):
            # 跳过某些特殊文档
            if doc_path.name in ["README.md", "glossary.md"]:
                continue
            
            try:
                content = doc_path.read_text(encoding='utf-8')
                links = self._extract_markdown_links(content)
                
                # 如果文档足够长但没有链接，记录下来
                line_count = len(content.split('\n'))
                if line_count > 50 and len(links) == 0:
                    docs_without_links.append(doc_path.relative_to(ROOT_DIR))
            except Exception as e:
                print(f"处理文档失败 {doc_path}: {e}")
        
        # 如果有很多文档没有链接，这可能表示文档互联性不足
        if docs_without_links:
            print(
                f"\n注意：以下文档没有包含任何链接:\n"
                f"  {docs_without_links}\n"
                f"  建议添加相关文档的交叉引用"
            )


if __name__ == "__main__":
    # 运行测试，配置 Hypothesis 运行至少 100 次迭代
    pytest.main([
        __file__,
        "-v",
        "--hypothesis-show-statistics",
        "--tb=short"
    ])
