#!/usr/bin/env python3
"""
属性测试：文档验证器
使用 Hypothesis 进行基于属性的测试
"""

import re
import pytest
from hypothesis import given, strategies as st, settings
from pathlib import Path
from typing import Dict
from validators.existence import DocumentExistenceChecker


# 获取项目根目录（从 scripts/ 目录向上一级）
ROOT_DIR = Path(__file__).parent.parent


class TestDocumentExistence:
    """
    属性测试：必需文档存在性
    
    **Feature: comprehensive-chinese-documentation, Property 1: 必需文档存在性**
    **Validates: Requirements 1.2, 1.3, 2.1, 2.3, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 4.3, 4.4**
    
    属性：对于任何文档类别（入门、使用、开发、进阶），该类别下的所有必需文档文件
    都应该存在于正确的目录路径中。
    """
    
    @given(category=st.sampled_from([
        "getting-started",
        "user-guide", 
        "development",
        "advanced",
        "versions",
        "root"
    ]))
    @settings(max_examples=100)
    def test_required_documents_exist_for_all_categories(self, category):
        """
        属性测试：对于任何文档类别，所有必需文档都应该存在
        
        这个测试验证了对于每个文档类别，该类别下定义的所有必需文档
        都存在于文件系统中的正确位置。
        """
        required_docs = DocumentExistenceChecker.REQUIRED_DOCS[category]
        
        for doc_path in required_docs:
            full_path = ROOT_DIR / doc_path
            # 属性：文档文件必须存在
            assert full_path.exists(), (
                f"必需文档不存在 [{category}]: {doc_path}"
            )
            # 属性：路径必须是文件而不是目录
            assert full_path.is_file(), (
                f"路径不是文件 [{category}]: {doc_path}"
            )
            # 属性：文档不应该为空
            assert full_path.stat().st_size > 0, (
                f"文档为空 [{category}]: {doc_path}"
            )
    
    @given(dir_path=st.sampled_from([
        "docs/zh",
        "docs/zh/getting-started",
        "docs/zh/user-guide",
        "docs/zh/development",
        "docs/zh/advanced",
        "docs/zh/versions",
    ]))
    @settings(max_examples=100)
    def test_required_directories_exist(self, dir_path):
        """
        属性测试：对于任何必需的目录路径，该目录都应该存在
        
        这个测试验证了文档系统的目录结构完整性。
        """
        full_path = ROOT_DIR / dir_path
        
        # 属性：目录必须存在
        assert full_path.exists(), f"必需目录不存在: {dir_path}"
        # 属性：路径必须是目录而不是文件
        assert full_path.is_dir(), f"路径不是目录: {dir_path}"
    
    def test_all_categories_have_documents(self):
        """
        测试：所有文档类别都定义了必需文档
        
        这确保了 REQUIRED_DOCS 字典的完整性。
        """
        expected_categories = {
            "getting-started",
            "user-guide",
            "development", 
            "advanced",
            "versions",
            "root"
        }
        
        actual_categories = set(DocumentExistenceChecker.REQUIRED_DOCS.keys())
        
        assert actual_categories == expected_categories, (
            f"文档类别不匹配。期望: {expected_categories}, "
            f"实际: {actual_categories}"
        )
    
    def test_existence_checker_integration(self):
        """
        集成测试：文档存在性检查器应该正确报告所有问题
        
        这个测试运行完整的检查器并验证它能够检测到所有问题。
        """
        checker = DocumentExistenceChecker(str(ROOT_DIR))
        
        # 运行检查器
        success = checker.check()
        
        # 如果所有文档都存在，检查应该成功
        # 如果有缺失文档，检查应该失败并报告错误
        if not success:
            # 确保有错误被记录
            assert len(checker.errors) > 0, (
                "检查失败但没有记录错误"
            )
            # 打印错误以便调试
            print("\n检测到的错误:")
            for error in checker.errors:
                print(f"  - {error}")
        else:
            # 成功时不应该有错误
            assert len(checker.errors) == 0, (
                f"检查成功但有错误: {checker.errors}"
            )


class TestCodeExampleSynchronization:
    """
    属性测试：代码示例同步性
    
    **Feature: comprehensive-chinese-documentation, Property 3: 代码示例同步性**
    **Validates: Requirements 2.5, 5.2**
    
    属性：对于任何文档中的代码示例，它应该与当前代码库中的实际代码保持一致，
    并且可以成功执行。
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
    def test_code_examples_are_syntactically_valid(self, doc_path):
        """
        属性测试：对于任何文档，其中的代码示例应该是语法正确的
        
        这个测试验证了文档中的 Python 代码示例可以被成功编译，
        确保用户不会遇到语法错误。
        """
        full_path = ROOT_DIR / doc_path
        
        # 如果文档不存在，跳过测试
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        
        # 提取所有 Python 代码块
        import re
        code_blocks = self._extract_python_code_blocks(content)
        
        # 属性：所有 Python 代码块都应该是语法正确的
        for i, code in enumerate(code_blocks, 1):
            # 跳过明显的占位符代码
            if self._is_placeholder_code(code):
                continue
            
            # 跳过包含明显占位符的代码
            if any(placeholder in code for placeholder in [
                'your_api_key_here',
                'your-',
                '[',
                '...',
                '# 示例代码',
                '# 代码示例',
                '# 在这里',
                '# TODO',
            ]):
                continue
            
            # 跳过 XML/HTML 内容（可能被错误标记为 Python）
            if code.strip().startswith('<') and '>' in code:
                continue
            
            # 跳过不完整的函数签名（API 文档中常见）
            if self._is_incomplete_signature(code):
                continue
            
            # 跳过包含顶层 await 的代码片段（需要在 async 函数中）
            if self._has_top_level_await(code):
                continue
            
            # 跳过包含 IPython 魔法命令的代码
            if self._has_ipython_magic(code):
                continue
            
            try:
                compile(code, f"<{doc_path}:block-{i}>", 'exec')
            except SyntaxError as e:
                pytest.fail(
                    f"文档 {doc_path} 中的代码块 #{i} 存在语法错误:\n"
                    f"错误: {e.msg} (行 {e.lineno})\n"
                    f"代码:\n{code[:200]}"
                )
    
    def _extract_python_code_blocks(self, content: str) -> list:
        """提取 Python 代码块，处理嵌套的代码块"""
        import re
        
        code_blocks = []
        lines = content.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i]
            
            # 查找 Python 代码块的开始
            if re.match(r'^```(?:python|py)\s*$', line):
                code_lines = []
                i += 1
                
                # 收集代码行，直到找到结束标记
                while i < len(lines):
                    if lines[i].strip() == '```':
                        # 找到结束标记
                        code_blocks.append('\n'.join(code_lines))
                        break
                    else:
                        code_lines.append(lines[i])
                    i += 1
            
            i += 1
        
        return code_blocks
    
    def _has_ipython_magic(self, code: str) -> bool:
        """检查代码是否包含 IPython 魔法命令"""
        lines = code.strip().split('\n')
        for line in lines:
            stripped = line.strip()
            # IPython 魔法命令以 % 或 %% 开头
            if stripped.startswith('%') or stripped.startswith('%%'):
                return True
        return False
    
    def _has_top_level_await(self, code: str) -> bool:
        """检查代码是否包含顶层 await（这在代码片段中常见但不是有效的 Python）"""
        lines = code.strip().split('\n')
        for line in lines:
            stripped = line.strip()
            # 跳过注释
            if stripped.startswith('#'):
                continue
            # 检查是否有 await 但不在函数定义内
            if 'await ' in stripped and not any(
                line.strip().startswith(keyword) 
                for keyword in ['async def', 'def']
            ):
                # 检查这不是在函数内部（简单启发式：没有缩进或很少缩进）
                if len(line) - len(line.lstrip()) < 4:
                    return True
        return False
    
    def _is_incomplete_signature(self, code: str) -> bool:
        """检查代码是否是不完整的函数/类签名（常见于 API 文档）"""
        stripped = code.strip()
        lines = [line.strip() for line in stripped.split('\n') if line.strip()]
        
        # 只有一行且是函数或类定义
        if len(lines) == 1:
            line = lines[0]
            # 函数或类定义但没有冒号（不完整）
            if (line.startswith('def ') or line.startswith('class ')) and ':' not in line:
                return True
            # 函数签名有冒号但没有函数体（只有签名行）
            if (line.startswith('def ') or line.startswith('class ')) and line.endswith(':'):
                return True
        
        # 只有函数/类定义行，没有实现
        if len(lines) <= 2:
            first_line = lines[0]
            if first_line.startswith('def ') or first_line.startswith('class '):
                # 检查是否有实际的函数体（不只是 pass 或文档字符串）
                if len(lines) == 1:
                    return True
                if len(lines) == 2 and (lines[1] == 'pass' or lines[1].startswith('"""') or lines[1].startswith("'''")):
                    return True
        
        return False
    
    def _is_placeholder_code(self, code: str) -> bool:
        """检查代码是否是占位符"""
        stripped = code.strip()
        
        # 空代码块
        if not stripped:
            return True
        
        # 只有注释的代码块
        lines = [line.strip() for line in stripped.split('\n') if line.strip()]
        if all(line.startswith('#') for line in lines):
            return True
        
        # 非常短的代码块（可能是示例片段）
        if len(stripped) < 10:
            return True
        
        return False
    
    @given(doc_path=st.sampled_from([
        "docs/zh/getting-started/installation.md",
        "docs/zh/getting-started/quickstart.md",
        "docs/zh/user-guide/examples.md",
        "docs/zh/development/development-guide.md",
        "docs/zh/versions/bedrock-anthropic.md",
    ]))
    @settings(max_examples=100)
    def test_code_examples_have_proper_language_tags(self, doc_path):
        """
        属性测试：对于任何文档，代码块应该有适当的语言标签
        
        这确保代码块被正确标记，便于语法高亮和验证。
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        
        # 查找所有代码块
        import re
        all_code_blocks = re.findall(
            r'```(\w*)\n(.*?)```',
            content,
            re.DOTALL
        )
        
        # 属性：所有非空代码块都应该有语言标签
        for i, (language, code) in enumerate(all_code_blocks, 1):
            # 跳过空代码块
            if not code.strip():
                continue
            
            # 跳过明显的输出/错误消息（不是代码）
            if self._looks_like_output(code):
                continue
            
            # 跳过明显的非代码内容（如输出示例）
            if language.lower() in ['output', 'text', 'console', '']:
                # 如果没有语言标签，检查是否看起来像代码
                if not language and self._looks_like_code(code):
                    pytest.fail(
                        f"文档 {doc_path} 中的代码块 #{i} 缺少语言标签\n"
                        f"代码片段: {code[:100]}"
                    )
    
    def _looks_like_code(self, text: str) -> bool:
        """检查文本是否看起来像代码"""
        # 简单启发式：包含常见代码模式
        code_patterns = [
            'import ',
            'def ',
            'class ',
            'from ',
            '= ',
            '(',
            '{',
            'function',
            'const ',
            'let ',
            'var ',
        ]
        return any(pattern in text for pattern in code_patterns)
    
    def _looks_like_output(self, text: str) -> bool:
        """检查文本是否看起来像输出或错误消息"""
        # 常见的输出/错误模式
        output_patterns = [
            'Error:',
            'Exception',
            'Traceback',
            'An error occurred',
            '错误:',
            '异常',
            'WARNING:',
            'INFO:',
        ]
        
        stripped = text.strip()
        
        # 检查是否以错误/输出模式开头
        for pattern in output_patterns:
            if pattern in stripped[:100]:
                return True
        
        # 如果主要是中文文本且没有代码特征，可能是输出
        # 检查是否包含大量中文字符但没有代码模式
        chinese_chars = sum(1 for c in stripped if '\u4e00' <= c <= '\u9fff')
        total_chars = len(stripped.replace(' ', '').replace('\n', ''))
        
        if total_chars > 0 and chinese_chars / total_chars > 0.5:
            # 如果超过50%是中文且不包含明显的代码模式
            if not self._looks_like_code(stripped):
                return True
        
        return False
    
    def test_code_validator_integration(self):
        """
        集成测试：代码示例验证器应该正确检测所有问题
        
        这个测试运行完整的代码验证器并验证它能够检测到代码问题。
        """
        from validators.code import CodeExampleValidator
        
        validator = CodeExampleValidator(str(ROOT_DIR))
        
        # 运行验证器
        success = validator.check()
        
        # 验证器应该能够运行而不崩溃
        # 如果有错误，它们应该被正确记录
        if not success:
            assert len(validator.errors) > 0 or len(validator.warnings) > 0, (
                "验证失败但没有记录错误或警告"
            )


class TestDocumentFormatConsistency:
    """
    属性测试：文档格式一致性
    
    **Feature: comprehensive-chinese-documentation, Property 4: 文档格式一致性**
    **Validates: Requirements 5.5, 6.5**
    
    属性：对于任何文档文件，它应该遵循统一的 Markdown 格式规范，
    包括标题层级、代码块格式和列表格式。
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
    ]))
    @settings(max_examples=100)
    def test_heading_format_consistency(self, doc_path):
        """
        属性测试：对于任何文档，标题格式应该一致
        
        验证：
        - 标题后应有空格（# Title 而不是 #Title）
        - 标题层级不应超过 6 级
        - 标题应该有实际内容
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # 跟踪是否在代码块内
        in_code_block = False
        
        for i, line in enumerate(lines, 1):
            # 检查代码块边界
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            # 跳过代码块内的内容
            if in_code_block:
                continue
            
            if line.startswith('#'):
                # 属性：标题后应有空格
                assert re.match(r'^#+\s+\S', line), (
                    f"文档 {doc_path} 行 {i}: "
                    f"标题格式不规范（# 后应有空格）\n"
                    f"行内容: {line}"
                )
                
                # 属性：标题层级不应超过 6 级
                match = re.match(r'^(#+)', line)
                if match:
                    level = len(match.group(1))
                    assert level <= 6, (
                        f"文档 {doc_path} 行 {i}: "
                        f"标题层级过深（{level} 级，最多 6 级）\n"
                        f"行内容: {line}"
                    )
    
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
    ]))
    @settings(max_examples=100)
    def test_code_block_format_consistency(self, doc_path):
        """
        属性测试：对于任何文档，代码块格式应该一致
        
        验证：
        - 代码块应该正确配对（开始和结束的 ``` 数量相等）
        - 代码块应该有语言标识符（除非是纯文本输出）
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        
        # 属性：代码块应该正确配对
        backticks = re.findall(r'^```', content, re.MULTILINE)
        assert len(backticks) % 2 == 0, (
            f"文档 {doc_path}: "
            f"代码块未正确闭合（``` 数量为 {len(backticks)}，应为偶数）"
        )
    
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
    ]))
    @settings(max_examples=100)
    def test_list_format_consistency(self, doc_path):
        """
        属性测试：对于任何文档，列表格式应该一致
        
        验证：
        - 列表项标记后应有空格（- item 而不是 -item）
        - 列表项应该有实际内容
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        lines = content.split('\n')
        
        # 跟踪是否在代码块内
        in_code_block = False
        
        for i, line in enumerate(lines, 1):
            # 检查代码块边界
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            # 跳过代码块内的内容
            if in_code_block:
                continue
            
            # 检查无序列表格式
            if re.match(r'^\s*[-*+]\s', line):
                # 属性：列表项标记后应有空格
                assert re.match(r'^\s*[-*+]\s+\S', line), (
                    f"文档 {doc_path} 行 {i}: "
                    f"列表格式不规范（标记后应有空格）\n"
                    f"行内容: {line}"
                )
            
            # 检查有序列表格式
            if re.match(r'^\s*\d+\.\s', line):
                # 属性：有序列表项标记后应有空格
                assert re.match(r'^\s*\d+\.\s+\S', line), (
                    f"文档 {doc_path} 行 {i}: "
                    f"有序列表格式不规范（标记后应有空格）\n"
                    f"行内容: {line}"
                )
    
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
    ]))
    @settings(max_examples=100)
    def test_markdown_syntax_validity(self, doc_path):
        """
        属性测试：对于任何文档，Markdown 语法应该有效
        
        **Feature: comprehensive-chinese-documentation, Property 11: Markdown 语法有效性**
        **Validates: Requirements 6.5**
        
        属性：对于任何文档文件，它应该是有效的 Markdown 格式，
        能够被标准 Markdown 解析器正确解析。
        
        验证：
        - 文档应该可以被读取（UTF-8 编码）
        - 文档不应该为空
        - 文档应该包含有效的 Markdown 内容
        - 文档应该能够被标准 Markdown 解析器解析而不出错
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        # 属性：文档应该可以被读取为 UTF-8
        try:
            content = full_path.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            pytest.fail(
                f"文档 {doc_path} 编码错误: {e}\n"
                f"文档应该使用 UTF-8 编码"
            )
        
        # 属性：文档不应该为空
        assert len(content.strip()) > 0, (
            f"文档 {doc_path} 为空"
        )
        
        # 属性：文档应该包含至少一个标题或段落
        has_heading = bool(re.search(r'^#+\s+', content, re.MULTILINE))
        has_paragraph = bool(re.search(r'^[^#\s\-*+`]', content, re.MULTILINE))
        
        assert has_heading or has_paragraph, (
            f"文档 {doc_path} 似乎不包含有效的 Markdown 内容"
        )
        
        # 属性：文档应该能够被标准 Markdown 解析器解析
        try:
            import markdown
            md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
            html_output = md.convert(content)
            
            # 验证解析器产生了输出
            assert len(html_output.strip()) > 0, (
                f"文档 {doc_path} 解析后为空"
            )
        except ImportError:
            # 如果 markdown 库不可用，使用基本的语法检查
            self._validate_basic_markdown_syntax(doc_path, content)
        except Exception as e:
            pytest.fail(
                f"文档 {doc_path} Markdown 解析失败: {e}\n"
                f"这表明文档包含无效的 Markdown 语法"
            )
    
    def _validate_basic_markdown_syntax(self, doc_path: str, content: str):
        """
        基本的 Markdown 语法验证（当 markdown 库不可用时使用）
        
        检查常见的 Markdown 语法错误：
        - 代码块未闭合
        - 链接格式错误
        - 标题格式错误
        """
        lines = content.split('\n')
        
        # 检查代码块配对
        code_block_count = 0
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                code_block_count += 1
        
        assert code_block_count % 2 == 0, (
            f"文档 {doc_path} 代码块未正确闭合"
        )
        
        # 检查链接格式（基本检查）
        # 查找未闭合的 Markdown 链接（排除代码块内的内容）
        in_code_block = False
        unclosed_links = []
        
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block:
                continue
            
            # 在非代码块行中查找未闭合的链接
            # 匹配 [ 但没有对应的 ]
            open_brackets = line.count('[')
            close_brackets = line.count(']')
            
            # 简单检查：如果一行中 [ 多于 ]，可能有未闭合的链接
            # 但这只是启发式检查，不是完美的
            if open_brackets > close_brackets:
                # 检查是否是真正的 Markdown 链接语法
                # Markdown 链接格式: [text](url) 或 [text][ref]
                # 如果有 [ 但后面没有 ]( 或 ][ 在同一行或下一行，可能有问题
                if '](' not in line and '][' not in line:
                    # 检查下一行是否有闭合
                    if i < len(lines):
                        next_line = lines[i] if i < len(lines) else ''
                        if '](' not in next_line and '][' not in next_line and ']' not in next_line:
                            unclosed_links.append((i, line.strip()[:50]))
        
        # 只在有明显未闭合链接时报错
        if unclosed_links:
            # 进一步验证：检查是否真的是 Markdown 链接
            # 如果包含 Markdown 链接的开始模式但没有结束
            real_issues = []
            for line_num, line_content in unclosed_links:
                # 检查是否看起来像 Markdown 链接的开始
                if re.search(r'\[[^\]]{10,}', line_content):  # [ 后跟至少10个非 ] 字符
                    real_issues.append((line_num, line_content))
            
            if real_issues:
                assert False, (
                    f"文档 {doc_path} 可能包含未闭合的链接: "
                    f"{real_issues[:3]}"
                )
        
        # 检查标题格式
        in_code_block = False
        for i, line in enumerate(lines, 1):
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            if in_code_block:
                continue
            
            # 检查标题格式
            if line.startswith('#'):
                assert re.match(r'^#+\s+\S', line), (
                    f"文档 {doc_path} 行 {i}: 标题格式错误"
                )
    
    def test_format_checker_integration(self):
        """
        集成测试：格式检查器应该正确检测所有格式问题
        
        这个测试运行完整的格式检查器并验证它能够检测到格式问题。
        """
        from validators.format import MarkdownFormatChecker
        
        checker = MarkdownFormatChecker(str(ROOT_DIR))
        
        # 运行检查器
        success = checker.check()
        
        # 验证器应该能够运行而不崩溃
        # 如果有错误，它们应该被正确记录
        if not success:
            assert len(checker.errors) > 0 or len(checker.warnings) > 0, (
                "格式检查失败但没有记录错误或警告"
            )


class TestDocumentStructureConsistency:
    """
    属性测试：文档结构一致性
    
    **Feature: comprehensive-chinese-documentation, Property 5: 文档结构一致性**
    **Validates: Requirements 5.5, 6.4**
    
    属性：对于任何同类型的文档（如所有入门文档），它们应该遵循相同的章节结构和组织模式。
    """
    
    @given(category=st.sampled_from([
        "getting-started",
        "user-guide",
        "development",
        "advanced",
        "versions"
    ]))
    @settings(max_examples=100)
    def test_same_category_documents_have_consistent_structure(self, category):
        """
        属性测试：对于任何文档类别，该类别下的所有文档应该遵循一致的结构模式
        
        这个测试验证了同类文档的结构一致性，包括：
        - 所有文档都应该有主标题（# 标题）
        - 同类文档应该有相似的章节组织
        - 标题层级使用应该一致
        """
        category_dir = ROOT_DIR / "docs" / "zh" / category
        
        # 如果目录不存在，跳过测试
        if not category_dir.exists():
            pytest.skip(f"类别目录不存在: {category}")
        
        # 获取该类别下的所有 Markdown 文档
        docs = list(category_dir.glob("*.md"))
        
        # 如果文档少于2个，无需比较一致性
        if len(docs) < 2:
            pytest.skip(f"类别 {category} 中文档数量少于2个，无需比较一致性")
        
        structures = {}
        for doc_path in docs:
            try:
                content = doc_path.read_text(encoding='utf-8')
                structure = self._extract_document_structure(content)
                structures[doc_path.name] = structure
            except Exception as e:
                pytest.fail(f"读取文档失败 {doc_path}: {e}")
        
        # 属性 1：所有文档都应该有主标题
        docs_without_title = [
            name for name, struct in structures.items()
            if not struct['has_main_title']
        ]
        assert len(docs_without_title) == 0, (
            f"类别 [{category}] 中以下文档缺少主标题（# 标题）: "
            f"{', '.join(docs_without_title)}"
        )
        
        # 属性 2：同类文档应该有相似的顶级章节数量（允许一定差异）
        # 我们检查是否所有文档的顶级章节数量在合理范围内
        h2_counts = [struct['h2_count'] for struct in structures.values()]
        if len(h2_counts) > 1:
            avg_h2 = sum(h2_counts) / len(h2_counts)
            # 允许偏差：平均值的 ±50% 或至少 ±2
            tolerance = max(2, avg_h2 * 0.5)
            
            outliers = [
                (name, count) for name, struct in structures.items()
                for count in [struct['h2_count']]
                if abs(count - avg_h2) > tolerance
            ]
            
            # 如果有明显的异常值，发出警告（不是错误，因为某些文档可能确实需要不同结构）
            if outliers and len(outliers) < len(structures) / 2:  # 只有少数文档异常时才警告
                # 这是一个软检查，我们记录但不失败
                print(
                    f"\n注意：类别 [{category}] 中部分文档的章节数量与平均值差异较大:\n"
                    f"  平均 H2 章节数: {avg_h2:.1f}\n"
                    f"  异常文档: {outliers}"
                )
        
        # 属性 3：同类文档应该使用一致的标题层级深度
        max_levels = [struct['max_heading_level'] for struct in structures.values()]
        if len(set(max_levels)) > 1:
            # 检查是否差异过大（超过2级）
            level_range = max(max_levels) - min(max_levels)
            if level_range > 2:
                # 这表明文档结构差异很大
                level_distribution = dict(zip(structures.keys(), max_levels))
                print(
                    f"\n注意：类别 [{category}] 中文档的标题层级深度差异较大:\n"
                    f"  {level_distribution}"
                )
    
    @given(category=st.sampled_from([
        "getting-started",
        "user-guide",
        "development",
        "advanced",
        "versions"
    ]))
    @settings(max_examples=100)
    def test_documents_have_required_sections(self, category):
        """
        属性测试：对于任何类别的文档，应该包含该类别要求的标准章节
        
        这个测试验证文档包含了预期的标准章节，如"概述"、"目标读者"等。
        """
        category_dir = ROOT_DIR / "docs" / "zh" / category
        
        if not category_dir.exists():
            pytest.skip(f"类别目录不存在: {category}")
        
        docs = list(category_dir.glob("*.md"))
        
        if len(docs) == 0:
            pytest.skip(f"类别 {category} 中没有文档")
        
        # 定义每个类别期望的标准章节（这些是常见的章节）
        # 注意：不是所有文档都必须有所有章节，但大多数应该有
        expected_sections = {
            "getting-started": ["概述", "目标读者", "前置条件"],
            "user-guide": ["概述", "目标读者", "前置条件"],
            "development": ["概述"],
            "advanced": ["概述"],
            "versions": []  # 版本文档可能有不同的结构
        }
        
        required_sections = expected_sections.get(category, [])
        
        # 如果该类别没有定义必需章节，跳过
        if not required_sections:
            pytest.skip(f"类别 {category} 没有定义必需章节")
        
        for doc_path in docs:
            # 跳过 README 文件，它们通常有不同的结构
            if doc_path.name == "README.md":
                continue
            
            try:
                content = doc_path.read_text(encoding='utf-8')
                headings = self._extract_headings(content)
                heading_texts = [h['text'].strip() for h in headings]
                
                # 检查是否包含至少一个必需章节
                # 注意：我们不要求所有章节都存在，因为某些文档可能有特殊结构
                has_any_required = any(
                    section in heading_texts
                    for section in required_sections
                )
                
                # 如果文档足够长（超过100行），应该有标准章节
                line_count = len(content.split('\n'))
                if line_count > 100 and not has_any_required:
                    # 这是一个软检查 - 打印警告而不是失败
                    print(
                        f"\n注意：文档 {doc_path.name} 可能缺少标准章节。"
                        f"期望的章节: {required_sections}"
                    )
            except Exception as e:
                pytest.fail(f"处理文档失败 {doc_path}: {e}")
    
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
    ]))
    @settings(max_examples=100)
    def test_document_has_logical_heading_hierarchy(self, doc_path):
        """
        属性测试：对于任何文档，标题层级应该是逻辑连贯的
        
        验证：
        - 文档应该从 H1 开始
        - 标题层级不应该跳级（如从 H2 直接到 H4）
        - 每个文档只应该有一个 H1 标题
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        headings = self._extract_headings(content)
        
        if not headings:
            pytest.skip(f"文档没有标题: {doc_path}")
        
        # 属性 1：文档应该从 H1 开始
        first_heading = headings[0]
        assert first_heading['level'] == 1, (
            f"文档 {doc_path} 应该从 H1 标题开始，"
            f"但第一个标题是 H{first_heading['level']}: {first_heading['text']}"
        )
        
        # 属性 2：每个文档只应该有一个 H1 标题
        h1_count = sum(1 for h in headings if h['level'] == 1)
        assert h1_count == 1, (
            f"文档 {doc_path} 应该只有一个 H1 标题，"
            f"但发现 {h1_count} 个 H1 标题"
        )
        
        # 属性 3：标题层级不应该跳级
        for i in range(1, len(headings)):
            prev_level = headings[i-1]['level']
            curr_level = headings[i]['level']
            
            # 如果层级增加，不应该跳过中间层级
            if curr_level > prev_level:
                level_jump = curr_level - prev_level
                assert level_jump == 1, (
                    f"文档 {doc_path} 中标题层级跳跃:\n"
                    f"  从 H{prev_level} '{headings[i-1]['text']}'\n"
                    f"  跳到 H{curr_level} '{headings[i]['text']}'\n"
                    f"  标题层级不应该跳级（跳过了 {level_jump - 1} 级）"
                )
    
    def _extract_document_structure(self, content: str) -> dict:
        """提取文档结构信息"""
        headings = self._extract_headings(content)
        
        structure = {
            'has_main_title': False,
            'h1_count': 0,
            'h2_count': 0,
            'h3_count': 0,
            'total_headings': len(headings),
            'max_heading_level': 0,
            'heading_levels': [],
        }
        
        if not headings:
            return structure
        
        # 检查是否有主标题（H1）
        structure['has_main_title'] = headings[0]['level'] == 1
        
        # 统计各级标题数量
        for heading in headings:
            level = heading['level']
            structure['heading_levels'].append(level)
            
            if level == 1:
                structure['h1_count'] += 1
            elif level == 2:
                structure['h2_count'] += 1
            elif level == 3:
                structure['h3_count'] += 1
            
            structure['max_heading_level'] = max(
                structure['max_heading_level'],
                level
            )
        
        return structure
    
    def _extract_headings(self, content: str) -> list:
        """提取文档中的所有标题"""
        headings = []
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
            
            # 匹配标题
            match = re.match(r'^(#+)\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append({
                    'level': level,
                    'text': text
                })
        
        return headings
    
    def test_structure_checker_integration(self):
        """
        集成测试：文档结构检查器应该正确检测所有结构问题
        
        这个测试运行完整的结构检查器并验证它能够检测到结构问题。
        """
        from validators.structure import DocumentStructureChecker
        
        checker = DocumentStructureChecker(str(ROOT_DIR))
        
        # 运行检查器
        success = checker.check()
        
        # 验证器应该能够运行而不崩溃
        # 如果有错误，它们应该被正确记录
        if not success:
            assert len(checker.errors) > 0 or len(checker.warnings) > 0, (
                "结构检查失败但没有记录错误或警告"
            )


class TestTableOfContentsCompleteness:
    """
    属性测试：目录索引完整性
    
    **Feature: comprehensive-chinese-documentation, Property 12: 目录索引完整性**
    **Validates: Requirements 6.1**
    
    属性：对于任何包含多个章节的文档，它应该在文档开头包含完整的目录索引，
    列出所有主要章节。
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
    ]))
    @settings(max_examples=100)
    def test_documents_with_multiple_sections_have_toc(self, doc_path):
        """
        属性测试：对于任何包含多个章节的文档，应该有目录索引
        
        验证：
        - 文档如果有多个 H2 章节（3个或以上），应该包含目录
        - 目录应该在文档开头（前几个章节内）
        - 目录应该是一个 H2 章节，标题为"目录"
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        
        # 提取所有标题
        headings = self._extract_headings(content)
        
        if not headings:
            pytest.skip(f"文档没有标题: {doc_path}")
        
        # 统计 H2 章节数量（不包括目录本身）
        h2_headings = [h for h in headings if h['level'] == 2]
        h2_count = len(h2_headings)
        
        # 检查是否有"目录"章节
        has_toc = any(
            h['level'] == 2 and h['text'] in ['目录', 'Table of Contents', 'TOC']
            for h in headings
        )
        
        # 属性：如果文档有3个或以上的 H2 章节，应该有目录
        # 减1是因为目录本身也是一个 H2 章节
        effective_h2_count = h2_count - 1 if has_toc else h2_count
        
        if effective_h2_count >= 3:
            assert has_toc, (
                f"文档 {doc_path} 有 {effective_h2_count} 个主要章节，"
                f"应该包含目录索引\n"
                f"章节列表: {[h['text'] for h in h2_headings]}"
            )
            
            # 如果有目录，验证目录的位置
            if has_toc:
                toc_index = next(
                    i for i, h in enumerate(headings)
                    if h['level'] == 2 and h['text'] in ['目录', 'Table of Contents', 'TOC']
                )
                
                # 属性：目录应该在文档开头（前3个标题内，通常是 H1 标题后的第一个 H2）
                assert toc_index <= 2, (
                    f"文档 {doc_path} 的目录位置过晚（位于第 {toc_index + 1} 个标题），"
                    f"目录应该在文档开头"
                )
    
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
    def test_toc_entries_match_actual_headings(self, doc_path):
        """
        属性测试：对于任何有目录的文档，目录条目应该与实际章节匹配
        
        验证：
        - 目录中列出的每个章节都应该在文档中存在
        - 目录应该包含所有主要的 H2 章节（除了目录本身）
        - 目录链接格式应该正确（使用 Markdown 锚点）
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        
        # 提取所有标题
        headings = self._extract_headings(content)
        
        # 查找目录章节
        toc_section = self._extract_toc_section(content)
        
        if not toc_section:
            pytest.skip(f"文档没有目录: {doc_path}")
        
        # 从目录中提取链接
        toc_entries = self._extract_toc_entries(toc_section)
        
        if not toc_entries:
            pytest.skip(f"目录为空: {doc_path}")
        
        # 获取所有 H2 章节（不包括目录本身）
        h2_headings = [
            h['text'] for h in headings
            if h['level'] == 2 and h['text'] not in ['目录', 'Table of Contents', 'TOC']
        ]
        
        # 属性 1：目录中的每个条目都应该对应文档中的实际章节
        for toc_entry in toc_entries:
            entry_text = toc_entry['text']
            
            # 检查是否有匹配的标题
            # 注意：目录中的文本可能与实际标题略有不同（如空格、标点）
            matching_headings = [
                h for h in headings
                if self._normalize_heading_text(h['text']) == self._normalize_heading_text(entry_text)
            ]
            
            assert len(matching_headings) > 0, (
                f"文档 {doc_path} 的目录条目 '{entry_text}' "
                f"在文档中找不到对应的章节\n"
                f"可用章节: {[h['text'] for h in headings[:10]]}"
            )
        
        # 属性 2：所有主要的 H2 章节都应该在目录中列出
        # 注意：某些文档可能有特殊章节不在目录中，所以我们检查覆盖率而不是完全匹配
        toc_entry_texts = [self._normalize_heading_text(e['text']) for e in toc_entries]
        
        missing_in_toc = []
        for h2_heading in h2_headings:
            normalized = self._normalize_heading_text(h2_heading)
            if normalized not in toc_entry_texts:
                missing_in_toc.append(h2_heading)
        
        # 如果超过30%的主要章节不在目录中，这可能是个问题
        if len(h2_headings) > 0:
            coverage = 1 - (len(missing_in_toc) / len(h2_headings))
            assert coverage >= 0.7, (
                f"文档 {doc_path} 的目录覆盖率过低 ({coverage:.0%})，"
                f"以下章节未在目录中列出: {missing_in_toc[:5]}"
            )
    
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
    def test_toc_links_are_properly_formatted(self, doc_path):
        """
        属性测试：对于任何有目录的文档，目录链接应该格式正确
        
        验证：
        - 目录条目应该使用 Markdown 链接格式：[文本](#锚点)
        - 锚点应该正确对应章节标题
        - 链接格式应该一致
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        content = full_path.read_text(encoding='utf-8')
        
        # 查找目录章节
        toc_section = self._extract_toc_section(content)
        
        if not toc_section:
            pytest.skip(f"文档没有目录: {doc_path}")
        
        # 从目录中提取链接
        toc_entries = self._extract_toc_entries(toc_section)
        
        if not toc_entries:
            pytest.skip(f"目录为空: {doc_path}")
        
        # 属性：所有目录条目都应该是正确的 Markdown 链接格式
        for entry in toc_entries:
            # 检查是否有链接
            assert entry['has_link'], (
                f"文档 {doc_path} 的目录条目 '{entry['text']}' "
                f"不是有效的 Markdown 链接"
            )
            
            # 检查链接是否是锚点链接（以 # 开头）
            if entry['link']:
                assert entry['link'].startswith('#'), (
                    f"文档 {doc_path} 的目录条目 '{entry['text']}' "
                    f"的链接 '{entry['link']}' 不是有效的锚点链接（应该以 # 开头）"
                )
    
    def _extract_headings(self, content: str) -> list:
        """提取文档中的所有标题"""
        headings = []
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
            
            # 匹配标题
            match = re.match(r'^(#+)\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append({
                    'level': level,
                    'text': text
                })
        
        return headings
    
    def _extract_toc_section(self, content: str) -> str:
        """提取目录章节的内容"""
        lines = content.split('\n')
        in_toc = False
        toc_lines = []
        in_code_block = False
        
        for i, line in enumerate(lines):
            # 跟踪代码块
            if line.strip().startswith('```'):
                in_code_block = not in_code_block
                continue
            
            # 跳过代码块内的内容
            if in_code_block:
                continue
            
            # 检查是否是目录标题
            if re.match(r'^##\s+(目录|Table of Contents|TOC)\s*$', line):
                in_toc = True
                continue
            
            # 如果在目录中
            if in_toc:
                # 如果遇到下一个 H2 或更高级别的标题，目录结束
                if re.match(r'^##\s+', line):
                    break
                
                # 如果遇到分隔线，目录可能结束
                if line.strip() == '---':
                    break
                
                toc_lines.append(line)
        
        return '\n'.join(toc_lines)
    
    def _extract_toc_entries(self, toc_section: str) -> list:
        """从目录章节中提取条目"""
        entries = []
        
        # 匹配 Markdown 列表项，可能包含链接
        # 格式: - [文本](#锚点) 或 - 文本
        lines = toc_section.split('\n')
        
        for line in lines:
            line = line.strip()
            
            # 跳过空行
            if not line:
                continue
            
            # 匹配列表项
            if line.startswith('-') or line.startswith('*'):
                # 移除列表标记
                content = line[1:].strip()
                
                # 尝试匹配 Markdown 链接: [文本](#锚点)
                link_match = re.match(r'\[(.+?)\]\((.+?)\)', content)
                
                if link_match:
                    text = link_match.group(1)
                    link = link_match.group(2)
                    entries.append({
                        'text': text,
                        'link': link,
                        'has_link': True
                    })
                else:
                    # 没有链接的条目
                    entries.append({
                        'text': content,
                        'link': None,
                        'has_link': False
                    })
        
        return entries
    
    def _normalize_heading_text(self, text: str) -> str:
        """
        规范化标题文本以便比较
        
        移除多余的空格、标点符号等，使比较更加宽松
        """
        # 移除多余的空格
        text = ' '.join(text.split())
        
        # 转换为小写（对于英文）
        # 注意：中文不受大小写影响
        
        # 移除常见的标点符号
        text = text.replace('：', ':').replace('，', ',')
        
        return text.strip()


class TestTerminologyConsistency:
    """
    属性测试：术语使用一致性
    
    **Feature: comprehensive-chinese-documentation, Property 6: 术语使用一致性**
    **Validates: Requirements 5.5**
    
    属性：对于任何技术术语，它在所有文档中的使用应该保持一致，
    并且与术语表中的定义相符。
    """
    
    def _load_glossary(self) -> Dict[str, str]:
        """加载术语表"""
        glossary = {}
        
        # 从主术语表加载
        glossary_path = ROOT_DIR / "docs/zh/glossary.md"
        if glossary_path.exists():
            try:
                content = glossary_path.read_text(encoding='utf-8')
                # 提取术语定义
                # 格式: ### Term\n- **中文**：中文翻译\n- **说明**：...
                sections = re.split(r'\n### ', content)
                for section in sections[1:]:  # 跳过第一个（标题前的内容）
                    lines = section.split('\n')
                    if lines:
                        # 英文术语在第一行
                        en_term = lines[0].strip()
                        # 查找中文翻译
                        zh_term = None
                        for line in lines[1:]:
                            match = re.match(r'-\s+\*\*中文\*\*[：:]\s*(.+)', line)
                            if match:
                                zh_term = match.group(1).strip()
                                # 移除括号中的内容（如"保留英文"）
                                zh_term = re.sub(r'[（(].*?[）)]', '', zh_term).strip()
                                break
                        
                        if zh_term:
                            glossary[zh_term] = en_term
                            # 如果中文和英文相同（保留英文的情况），也记录英文
                            if zh_term == en_term:
                                glossary[en_term] = en_term
            except Exception as e:
                print(f"加载术语表失败: {e}")
        
        # 从需求文档加载术语表
        req_path = ROOT_DIR / ".kiro/specs/comprehensive-chinese-documentation/requirements.md"
        if req_path.exists():
            try:
                content = req_path.read_text(encoding='utf-8')
                # 提取术语表部分
                match = re.search(r'## 术语表\n\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
                if match:
                    glossary_text = match.group(1)
                    # 解析术语定义: - **中文术语（English Term）**：定义
                    terms = re.findall(r'-\s+\*\*(.+?)（(.+?)）\*\*', glossary_text)
                    for zh_term, en_term in terms:
                        glossary[zh_term] = en_term
            except Exception as e:
                print(f"加载需求文档术语表失败: {e}")
        
        return glossary
    
    @given(term=st.sampled_from([
        "文档系统", "用户", "贡献者", "Claude", "提示工程", "Bedrock",
        "Jupyter Notebook", "API", "提示词", "模型", "参数", "响应",
        "教程", "示例", "版本", "依赖项", "环境变量", "配置", "安装"
    ]))
    @settings(max_examples=100)
    def test_terminology_usage_is_consistent_across_documents(self, term):
        """
        属性测试：对于任何术语，它在所有文档中的使用应该一致
        
        这个测试验证了：
        1. 术语在文档中被使用
        2. 术语的使用方式一致（不会有多种不同的表述）
        3. 如果术语在术语表中定义，使用应该与定义一致
        """
        glossary = self._load_glossary()
        
        # 如果术语不在术语表中，跳过（可能是通用词汇）
        if term not in glossary:
            pytest.skip(f"术语 '{term}' 不在术语表中")
        
        docs_dir = ROOT_DIR / "docs" / "zh"
        if not docs_dir.exists():
            pytest.skip("文档目录不存在")
        
        # 收集术语在各文档中的使用情况
        term_occurrences = []
        
        for doc_path in docs_dir.rglob("*.md"):
            # 跳过术语表本身
            if doc_path.name == "glossary.md":
                continue
            
            try:
                content = doc_path.read_text(encoding='utf-8')
                
                # 统计术语出现次数
                count = content.count(term)
                if count > 0:
                    term_occurrences.append({
                        'doc': doc_path.relative_to(ROOT_DIR),
                        'count': count
                    })
                
                # 检查是否有常见的术语变体（可能表示不一致）
                # 例如："文档系统" vs "文档体系"
                if term == "文档系统":
                    variant_count = content.count("文档体系")
                    if variant_count > 0:
                        # 这可能是可接受的变体，但我们记录它
                        print(f"\n注意：文档 {doc_path.name} 中使用了 '文档体系' ({variant_count}次) "
                              f"而不是标准术语 '文档系统' ({count}次)")
                
            except Exception as e:
                pytest.fail(f"读取文档失败 {doc_path}: {e}")
        
        # 属性：如果术语在术语表中，它应该在至少一个文档中被使用
        # （除非是非常专业的术语）
        if not term_occurrences:
            # 某些术语可能确实没有在文档中使用，这不一定是错误
            # 我们只记录而不失败
            print(f"\n注意：术语 '{term}' 在术语表中定义但未在文档中使用")
    
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
    def test_document_uses_glossary_terms_consistently(self, doc_path):
        """
        属性测试：对于任何文档，它应该一致地使用术语表中定义的术语
        
        验证：
        - 文档中使用的技术术语应该与术语表中的定义一致
        - 不应该混用不同的术语表述同一概念
        """
        full_path = ROOT_DIR / doc_path
        
        if not full_path.exists():
            pytest.skip(f"文档不存在: {doc_path}")
        
        glossary = self._load_glossary()
        
        if not glossary:
            pytest.skip("术语表为空")
        
        content = full_path.read_text(encoding='utf-8')
        
        # 检查文档中是否使用了术语表中的术语
        used_terms = []
        for term in glossary.keys():
            if term in content:
                count = content.count(term)
                used_terms.append((term, count))
        
        # 属性：如果文档使用了术语，应该一致地使用标准术语
        # 我们检查是否有常见的不一致模式
        
        # 检查中英文混用的一致性
        # 例如：如果使用了 "Claude"，应该始终使用 "Claude" 而不是 "克劳德"
        if "Claude" in content:
            # Claude 应该保留英文
            chinese_variant = "克劳德"
            if chinese_variant in content:
                pytest.fail(
                    f"文档 {doc_path} 中术语使用不一致:\n"
                    f"  同时使用了 'Claude' 和 '{chinese_variant}'\n"
                    f"  应该统一使用 'Claude'（根据术语表）"
                )
        
        # 检查 "提示工程" vs "提示词工程"
        if "提示工程" in content and "提示词工程" in content:
            # 这可能表示术语使用不一致
            print(
                f"\n注意：文档 {doc_path} 中同时使用了 '提示工程' 和 '提示词工程'，"
                f"建议统一使用 '提示工程'"
            )
        
        # 检查 "API" 的使用
        if "API" in content:
            # 检查是否有不一致的中文翻译
            variants = ["应用程序接口", "应用编程接口", "应用程式介面"]
            found_variants = [v for v in variants if v in content]
            if len(found_variants) > 1:
                print(
                    f"\n注意：文档 {doc_path} 中 API 的中文翻译不一致:\n"
                    f"  发现多种翻译: {found_variants}\n"
                    f"  建议统一使用 '应用程序编程接口' 或直接使用 'API'"
                )
    
    def test_glossary_completeness(self):
        """
        测试：术语表应该包含项目中使用的主要技术术语
        
        这个测试验证术语表的完整性，确保主要的技术术语都有定义。
        """
        glossary = self._load_glossary()
        
        # 定义项目中应该包含的核心术语
        expected_core_terms = [
            "Claude",
            "Bedrock",
            "提示工程",
            "Jupyter Notebook",
        ]
        
        missing_terms = []
        for term in expected_core_terms:
            if term not in glossary:
                missing_terms.append(term)
        
        assert len(missing_terms) == 0, (
            f"术语表缺少核心术语: {missing_terms}\n"
            f"当前术语表包含: {list(glossary.keys())[:10]}..."
        )
    
    def test_terminology_checker_integration(self):
        """
        集成测试：术语一致性检查器应该正确检测术语使用问题
        
        这个测试运行完整的术语检查器并验证它能够检测到术语使用问题。
        """
        from validators.terminology import TerminologyChecker
        
        checker = TerminologyChecker(str(ROOT_DIR))
        
        # 运行检查器
        success = checker.check()
        
        # 验证器应该能够运行而不崩溃
        # 术语检查可能会产生警告但不一定是错误
        # 我们主要验证检查器能够正常工作
        assert checker.glossary is not None, "术语表应该被加载"
        assert len(checker.glossary) > 0, "术语表不应该为空"


class TestVersionDocumentationCompleteness:
    """
    属性测试：版本文档完整性
    
    **Feature: comprehensive-chinese-documentation, Property 9: 版本文档完整性**
    **Validates: Requirements 7.3**
    
    属性：对于任何项目版本（Anthropic 1P、Bedrock Anthropic、Bedrock Boto3），
    应该存在该版本的专门配置和使用说明文档。
    """
    
    # 定义项目中的所有版本
    VERSIONS = {
        "anthropic-1p": {
            "name": "Anthropic 1P",
            "directory": "Anthropic 1P",
            "doc_path": "docs/zh/versions/anthropic-1p.md",
            "readme_path": "Anthropic 1P/README_ZH.md",
        },
        "bedrock-anthropic": {
            "name": "Bedrock Anthropic SDK",
            "directory": "AmazonBedrock/anthropic",
            "doc_path": "docs/zh/versions/bedrock-anthropic.md",
            "readme_path": "AmazonBedrock/README_ZH.md",
        },
        "bedrock-boto3": {
            "name": "Bedrock Boto3",
            "directory": "AmazonBedrock/boto3",
            "doc_path": "docs/zh/versions/bedrock-boto3.md",
            "readme_path": "AmazonBedrock/README_ZH.md",
        },
    }
    
    @given(version_key=st.sampled_from([
        "anthropic-1p",
        "bedrock-anthropic",
        "bedrock-boto3"
    ]))
    @settings(max_examples=100)
    def test_each_version_has_dedicated_documentation(self, version_key):
        """
        属性测试：对于任何项目版本，应该存在专门的版本文档
        
        验证：
        - 版本文档文件存在于 docs/zh/versions/ 目录
        - 版本文档不为空
        - 版本文档是有效的 Markdown 文件
        """
        version_info = self.VERSIONS[version_key]
        doc_path = ROOT_DIR / version_info["doc_path"]
        
        # 属性 1：版本文档文件必须存在
        assert doc_path.exists(), (
            f"版本 '{version_info['name']}' 缺少专门的文档文件: {version_info['doc_path']}"
        )
        
        # 属性 2：版本文档必须是文件而不是目录
        assert doc_path.is_file(), (
            f"版本文档路径不是文件: {version_info['doc_path']}"
        )
        
        # 属性 3：版本文档不应该为空
        assert doc_path.stat().st_size > 0, (
            f"版本 '{version_info['name']}' 的文档为空: {version_info['doc_path']}"
        )
        
        # 属性 4：版本文档应该可以被读取为 UTF-8
        try:
            content = doc_path.read_text(encoding='utf-8')
        except UnicodeDecodeError as e:
            pytest.fail(
                f"版本文档 {version_info['doc_path']} 编码错误: {e}\n"
                f"文档应该使用 UTF-8 编码"
            )
        
        # 属性 5：版本文档应该包含有效的 Markdown 内容
        assert len(content.strip()) > 100, (
            f"版本 '{version_info['name']}' 的文档内容过少（少于100字符）: {version_info['doc_path']}"
        )
    
    @given(version_key=st.sampled_from([
        "anthropic-1p",
        "bedrock-anthropic",
        "bedrock-boto3"
    ]))
    @settings(max_examples=100)
    def test_each_version_has_configuration_instructions(self, version_key):
        """
        属性测试：对于任何项目版本，版本文档应该包含配置说明
        
        验证：
        - 版本文档包含配置相关的章节
        - 文档说明了如何配置该版本
        - 文档提供了版本特定的设置说明
        """
        version_info = self.VERSIONS[version_key]
        doc_path = ROOT_DIR / version_info["doc_path"]
        
        if not doc_path.exists():
            pytest.skip(f"版本文档不存在: {version_info['doc_path']}")
        
        content = doc_path.read_text(encoding='utf-8')
        
        # 属性：版本文档应该包含配置相关的内容
        # 检查是否包含配置相关的关键词
        config_keywords = [
            "配置", "安装", "设置", "环境", "依赖",
            "Configuration", "Setup", "Installation", "Environment"
        ]
        
        has_config_content = any(keyword in content for keyword in config_keywords)
        
        assert has_config_content, (
            f"版本 '{version_info['name']}' 的文档缺少配置说明\n"
            f"文档应该包含以下关键词之一: {config_keywords}"
        )
        
        # 属性：版本文档应该包含配置相关的章节标题
        # 提取所有标题
        headings = self._extract_headings(content)
        heading_texts = [h['text'] for h in headings]
        
        # 检查是否有配置相关的章节
        config_section_keywords = [
            "配置", "安装", "设置", "环境", "前置条件", "依赖",
            "Configuration", "Setup", "Installation", "Prerequisites"
        ]
        
        has_config_section = any(
            any(keyword in heading for keyword in config_section_keywords)
            for heading in heading_texts
        )
        
        assert has_config_section, (
            f"版本 '{version_info['name']}' 的文档缺少配置相关的章节\n"
            f"文档章节: {heading_texts[:10]}\n"
            f"应该包含配置、安装或设置相关的章节"
        )
    
    @given(version_key=st.sampled_from([
        "anthropic-1p",
        "bedrock-anthropic",
        "bedrock-boto3"
    ]))
    @settings(max_examples=100)
    def test_each_version_has_usage_instructions(self, version_key):
        """
        属性测试：对于任何项目版本，版本文档应该包含使用说明
        
        验证：
        - 版本文档包含使用说明章节
        - 文档说明了如何使用该版本
        - 文档提供了版本特定的使用示例或说明
        """
        version_info = self.VERSIONS[version_key]
        doc_path = ROOT_DIR / version_info["doc_path"]
        
        if not doc_path.exists():
            pytest.skip(f"版本文档不存在: {version_info['doc_path']}")
        
        content = doc_path.read_text(encoding='utf-8')
        
        # 属性：版本文档应该包含使用说明相关的内容
        usage_keywords = [
            "使用", "运行", "执行", "示例", "教程",
            "Usage", "Running", "Example", "Tutorial", "How to"
        ]
        
        has_usage_content = any(keyword in content for keyword in usage_keywords)
        
        assert has_usage_content, (
            f"版本 '{version_info['name']}' 的文档缺少使用说明\n"
            f"文档应该包含以下关键词之一: {usage_keywords}"
        )
        
        # 属性：版本文档应该包含使用说明相关的章节
        headings = self._extract_headings(content)
        heading_texts = [h['text'] for h in headings]
        
        usage_section_keywords = [
            "使用", "运行", "快速开始", "示例", "教程", "入门",
            "Usage", "Running", "Quick Start", "Example", "Tutorial", "Getting Started"
        ]
        
        has_usage_section = any(
            any(keyword in heading for keyword in usage_section_keywords)
            for heading in heading_texts
        )
        
        assert has_usage_section, (
            f"版本 '{version_info['name']}' 的文档缺少使用说明章节\n"
            f"文档章节: {heading_texts[:10]}\n"
            f"应该包含使用、运行或示例相关的章节"
        )
    
    @given(version_key=st.sampled_from([
        "anthropic-1p",
        "bedrock-anthropic",
        "bedrock-boto3"
    ]))
    @settings(max_examples=100)
    def test_each_version_directory_has_readme(self, version_key):
        """
        属性测试：对于任何项目版本，版本目录应该有中文 README
        
        验证：
        - 版本目录存在
        - 版本目录包含中文 README 文件
        - README 文件不为空
        """
        version_info = self.VERSIONS[version_key]
        readme_path = ROOT_DIR / version_info["readme_path"]
        
        # 属性 1：版本 README 文件必须存在
        assert readme_path.exists(), (
            f"版本 '{version_info['name']}' 缺少中文 README 文件: {version_info['readme_path']}"
        )
        
        # 属性 2：README 必须是文件
        assert readme_path.is_file(), (
            f"README 路径不是文件: {version_info['readme_path']}"
        )
        
        # 属性 3：README 不应该为空
        assert readme_path.stat().st_size > 0, (
            f"版本 '{version_info['name']}' 的 README 为空: {version_info['readme_path']}"
        )
        
        # 属性 4：README 应该包含版本特定的信息
        content = readme_path.read_text(encoding='utf-8')
        
        # 检查是否提到了版本名称或相关信息
        version_mentioned = (
            version_info['name'] in content or
            "Anthropic" in content or
            "Bedrock" in content or
            "Claude" in content
        )
        
        assert version_mentioned, (
            f"版本 '{version_info['name']}' 的 README 似乎没有提到版本相关信息"
        )
    
    @given(version_key=st.sampled_from([
        "anthropic-1p",
        "bedrock-anthropic",
        "bedrock-boto3"
    ]))
    @settings(max_examples=100)
    def test_version_documentation_describes_version_specifics(self, version_key):
        """
        属性测试：对于任何项目版本，版本文档应该描述版本特定的特性
        
        验证：
        - 版本文档明确说明了该版本的特点
        - 文档说明了该版本的适用场景
        - 文档提供了版本特定的信息（不只是通用信息）
        """
        version_info = self.VERSIONS[version_key]
        doc_path = ROOT_DIR / version_info["doc_path"]
        
        if not doc_path.exists():
            pytest.skip(f"版本文档不存在: {version_info['doc_path']}")
        
        content = doc_path.read_text(encoding='utf-8')
        
        # 属性：版本文档应该包含版本特定的描述
        # 检查是否包含"特点"、"特性"、"适用场景"等章节
        headings = self._extract_headings(content)
        heading_texts = [h['text'] for h in headings]
        
        version_specific_keywords = [
            "特点", "特性", "优势", "适用", "场景", "区别", "差异",
            "Features", "Characteristics", "Advantages", "Use Cases", "Differences"
        ]
        
        has_version_specific_section = any(
            any(keyword in heading for keyword in version_specific_keywords)
            for heading in heading_texts
        )
        
        # 如果没有专门的章节，至少应该在内容中描述版本特性
        if not has_version_specific_section:
            has_version_description = any(
                keyword in content for keyword in version_specific_keywords
            )
            
            assert has_version_description, (
                f"版本 '{version_info['name']}' 的文档缺少版本特性描述\n"
                f"文档应该说明该版本的特点、适用场景或与其他版本的区别"
            )
    
    def test_all_versions_are_documented(self):
        """
        测试：所有项目版本都应该有完整的文档
        
        这个测试验证了版本文档的完整性，确保每个版本都有必需的文档。
        """
        for version_key, version_info in self.VERSIONS.items():
            # 检查版本文档
            doc_path = ROOT_DIR / version_info["doc_path"]
            assert doc_path.exists(), (
                f"版本 '{version_info['name']}' 缺少文档: {version_info['doc_path']}"
            )
            
            # 检查版本 README
            readme_path = ROOT_DIR / version_info["readme_path"]
            assert readme_path.exists(), (
                f"版本 '{version_info['name']}' 缺少 README: {version_info['readme_path']}"
            )
    
    def test_version_comparison_document_exists(self):
        """
        测试：应该存在版本对比文档
        
        验证版本对比文档的存在性，该文档应该帮助用户选择合适的版本。
        """
        comparison_path = ROOT_DIR / "docs/zh/versions/comparison.md"
        
        # 属性：版本对比文档必须存在
        assert comparison_path.exists(), (
            "缺少版本对比文档: docs/zh/versions/comparison.md"
        )
        
        # 属性：对比文档不应该为空
        assert comparison_path.stat().st_size > 0, (
            "版本对比文档为空"
        )
        
        # 属性：对比文档应该提到所有版本
        content = comparison_path.read_text(encoding='utf-8')
        
        for version_key, version_info in self.VERSIONS.items():
            version_name = version_info['name']
            # 检查是否提到了该版本（可能是英文或中文名称）
            version_mentioned = (
                version_name in content or
                version_key in content or
                "Anthropic 1P" in content or
                "Bedrock" in content
            )
            
            assert version_mentioned, (
                f"版本对比文档应该提到版本 '{version_name}'"
            )
    
    def _extract_headings(self, content: str) -> list:
        """提取文档中的所有标题"""
        headings = []
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
            
            # 匹配标题
            match = re.match(r'^(#+)\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append({
                    'level': level,
                    'text': text
                })
        
        return headings


if __name__ == "__main__":
    # 运行测试，配置 Hypothesis 运行至少 100 次迭代
    pytest.main([
        __file__,
        "-v",
        "--hypothesis-show-statistics",
        "--tb=short"
    ])
