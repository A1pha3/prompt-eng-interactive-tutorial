# 代码规范文档

## 目录

- [概述](#概述)
- [Python 代码规范](#python-代码规范)
- [Jupyter Notebook 规范](#jupyter-notebook-规范)
- [文档编写规范](#文档编写规范)
- [Git 提交规范](#git-提交规范)
- [代码审查检查清单](#代码审查检查清单)
- [工具配置](#工具配置)
- [相关资源](#相关资源)

## 概述

本文档定义了 Anthropic Claude 提示工程交互式教程项目的代码风格规范。遵循统一的代码规范有助于：

- 提高代码可读性和可维护性
- 减少代码审查时间
- 避免常见错误
- 促进团队协作

### 规范原则

1. **一致性优先**：保持代码风格的一致性
2. **可读性第一**：代码应该易于理解
3. **简洁明了**：避免过度复杂的实现
4. **文档完善**：提供清晰的注释和文档

## Python 代码规范

### 基础规范

本项目遵循 [PEP 8](https://pep8.org/) Python 代码风格指南。

#### 缩进

- 使用 **4 个空格**进行缩进
- 不使用制表符（Tab）

```python
# 正确
def example_function():
    if True:
        print("使用 4 个空格缩进")

# 错误
def example_function():
  if True:
    print("不要使用 2 个空格")
```

#### 行长度

- 每行最多 **88 个字符**（遵循 Black 格式化器标准）
- 对于文档字符串和注释，建议不超过 **72 个字符**

```python
# 正确
def short_function_name(
    parameter_one, parameter_two, parameter_three
):
    """简短的文档字符串。"""
    pass

# 错误 - 行太长
def short_function_name(parameter_one, parameter_two, parameter_three, parameter_four, parameter_five):
    pass
```

#### 空行

- 顶层函数和类定义之间使用 **2 个空行**
- 类中的方法定义之间使用 **1 个空行**
- 函数内部使用空行分隔逻辑段落

```python
# 正确
class ExampleClass:
    """示例类。"""

    def method_one(self):
        """第一个方法。"""
        pass

    def method_two(self):
        """第二个方法。"""
        pass


def standalone_function():
    """独立函数。"""
    pass
```

### 命名规范

#### 变量和函数

- 使用 **小写字母** 和 **下划线**（snake_case）
- 名称应该具有描述性

```python
# 正确
user_name = "Alice"
api_key = "sk-..."
max_tokens = 1024

def get_user_prompt():
    pass

def send_api_request():
    pass

# 错误
userName = "Alice"  # 不要使用驼峰命名
apikey = "sk-..."   # 缺少下划线
mt = 1024           # 名称不够描述性

def getUserPrompt():  # 不要使用驼峰命名
    pass
```

#### 类名

- 使用 **驼峰命名**（PascalCase）

```python
# 正确
class PromptTemplate:
    pass

class APIClient:
    pass

# 错误
class prompt_template:  # 应该使用驼峰命名
    pass
```

#### 常量

- 使用 **全大写字母** 和 **下划线**

```python
# 正确
MAX_RETRIES = 3
DEFAULT_MODEL = "claude-3-haiku-20240307"
API_TIMEOUT = 30

# 错误
max_retries = 3  # 常量应该全大写
```

#### 私有变量和方法

- 使用 **单下划线前缀** 表示内部使用

```python
class APIClient:
    def __init__(self):
        self._api_key = None  # 私有属性
    
    def _validate_key(self):  # 私有方法
        pass
    
    def send_request(self):   # 公共方法
        pass
```

### 导入规范

#### 导入顺序

1. 标准库导入
2. 第三方库导入
3. 本地应用/库导入

每组之间用空行分隔。

```python
# 正确
import os
import sys
from typing import Dict, List

import anthropic
import boto3

from utils.helpers import format_prompt
from utils.validators import validate_response

# 错误 - 顺序混乱
import anthropic
import os
from utils.helpers import format_prompt
import sys
```

#### 导入格式

- 每个导入独占一行
- 使用绝对导入
- 避免使用 `import *`

```python
# 正确
import os
import sys
from anthropic import Anthropic

# 错误
import os, sys  # 不要在一行导入多个模块
from anthropic import *  # 不要使用通配符导入
```

### 类型注解

使用类型注解提高代码可读性和类型安全性。

```python
from typing import Dict, List, Optional

def get_prompt_template(
    template_name: str,
    variables: Dict[str, str]
) -> str:
    """获取格式化的提示词模板。
    
    Args:
        template_name: 模板名称
        variables: 模板变量字典
        
    Returns:
        格式化后的提示词字符串
    """
    pass

def process_response(
    response: dict,
    max_length: Optional[int] = None
) -> List[str]:
    """处理 API 响应。"""
    pass
```

### 文档字符串

使用 Google 风格的文档字符串。

#### 函数文档字符串

```python
def send_message(
    client: Anthropic,
    prompt: str,
    model: str = "claude-3-haiku-20240307",
    max_tokens: int = 1024
) -> dict:
    """发送消息到 Claude API。
    
    这个函数封装了 Anthropic API 调用，提供了统一的接口
    和错误处理。
    
    Args:
        client: Anthropic 客户端实例
        prompt: 用户提示词
        model: 使用的模型 ID，默认为 Haiku
        max_tokens: 最大生成 token 数
        
    Returns:
        包含响应内容的字典，格式为：
        {
            'content': str,
            'model': str,
            'usage': dict
        }
        
    Raises:
        APIError: 当 API 调用失败时
        ValueError: 当参数无效时
        
    Example:
        >>> client = Anthropic(api_key="sk-...")
        >>> response = send_message(client, "Hello, Claude")
        >>> print(response['content'])
        Hello! How can I help you today?
    """
    pass
```

#### 类文档字符串

```python
class PromptTemplate:
    """提示词模板管理器。
    
    这个类提供了创建、管理和格式化提示词模板的功能。
    支持变量替换和模板验证。
    
    Attributes:
        templates: 存储所有模板的字典
        default_template: 默认模板名称
        
    Example:
        >>> manager = PromptTemplate()
        >>> manager.add_template("greeting", "Hello, {name}!")
        >>> prompt = manager.format("greeting", name="Alice")
        >>> print(prompt)
        Hello, Alice!
    """
    
    def __init__(self):
        """初始化模板管理器。"""
        self.templates: Dict[str, str] = {}
        self.default_template: Optional[str] = None
```

### 错误处理

#### 异常处理

```python
# 正确 - 捕获具体的异常
try:
    response = client.messages.create(...)
except anthropic.APIError as e:
    print(f"API 错误: {e}")
except anthropic.AuthenticationError as e:
    print(f"认证失败: {e}")
except Exception as e:
    print(f"未知错误: {e}")

# 错误 - 捕获所有异常
try:
    response = client.messages.create(...)
except:  # 不要使用裸 except
    print("出错了")
```

#### 自定义异常

```python
class PromptValidationError(Exception):
    """提示词验证错误。"""
    pass

class TemplateNotFoundError(Exception):
    """模板未找到错误。"""
    pass

def validate_prompt(prompt: str) -> None:
    """验证提示词。"""
    if not prompt.strip():
        raise PromptValidationError("提示词不能为空")
```

### 代码组织

#### 函数长度

- 单个函数不超过 **50 行**
- 复杂逻辑拆分成多个小函数

```python
# 正确 - 拆分成小函数
def process_user_input(user_input: str) -> dict:
    """处理用户输入。"""
    validated_input = _validate_input(user_input)
    formatted_prompt = _format_prompt(validated_input)
    response = _send_to_api(formatted_prompt)
    return _parse_response(response)

def _validate_input(input_str: str) -> str:
    """验证输入。"""
    pass

def _format_prompt(input_str: str) -> str:
    """格式化提示词。"""
    pass
```

#### 避免魔法数字

```python
# 正确 - 使用常量
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30
DEFAULT_MAX_TOKENS = 1024

def send_request():
    for attempt in range(MAX_RETRIES):
        try:
            response = client.messages.create(
                max_tokens=DEFAULT_MAX_TOKENS,
                timeout=TIMEOUT_SECONDS
            )
        except Exception:
            continue

# 错误 - 使用魔法数字
def send_request():
    for attempt in range(3):  # 3 是什么？
        try:
            response = client.messages.create(
                max_tokens=1024,  # 为什么是 1024？
                timeout=30
            )
        except Exception:
            continue
```
## Jupyter Notebook 规范

### Notebook 结构

每个教程 Notebook 应遵循统一的结构：

```
1. 标题和简介
2. 学习目标
3. 前置知识
4. 概念介绍
5. 示例演示
6. 最佳实践
7. 常见错误
8. 示例练习场
9. 练习题
10. 总结和下一步
```

### 单元格组织

#### Markdown 单元格

- 使用清晰的标题层级（# ## ### ####）
- 每个概念用独立的单元格说明
- 使用列表、代码块和强调来提高可读性

```markdown
# 第 1 章：基本提示词结构

## 学习目标

完成本章后，您将能够：
- 理解提示词的基本组成部分
- 编写结构清晰的提示词
- 识别常见的提示词问题

## 概念介绍

提示词是与 Claude 交互的核心...
```

#### 代码单元格

- 每个单元格只包含一个完整的逻辑单元
- 添加注释说明关键步骤
- 确保单元格可以独立运行（除非有明确的依赖）

```python
# 设置 API 客户端
from anthropic import Anthropic

client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
print("✓ 客户端初始化成功")
```

```python
# 发送第一个提示词
message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Hello, Claude!"}
    ]
)

# 显示响应
print(message.content[0].text)
```

### 代码风格

#### 导入语句

- 在 Notebook 开头集中导入
- 使用单独的单元格进行导入

```python
# 导入必需的库
import os
import json
from typing import Dict, List

from anthropic import Anthropic
```

#### 变量命名

- 使用描述性的变量名
- 避免使用单字母变量（除了循环计数器）

```python
# 正确
user_prompt = "请解释量子计算"
max_tokens = 1024
model_name = "claude-3-haiku-20240307"

# 错误
p = "请解释量子计算"
m = 1024
n = "claude-3-haiku-20240307"
```

#### 输出格式化

- 使用清晰的输出格式
- 添加分隔符和标签

```python
# 正确 - 清晰的输出
print("=" * 50)
print("提示词:")
print(prompt)
print("\n" + "=" * 50)
print("响应:")
print(response.content[0].text)
print("=" * 50)

# 错误 - 混乱的输出
print(prompt)
print(response.content[0].text)
```

### 注释规范

#### 单元格说明

在代码单元格前添加 Markdown 单元格说明：

```markdown
### 示例 1：基本提示词

下面的代码演示如何发送一个简单的提示词：
```

#### 代码注释

```python
# 构建提示词 - 使用清晰的指令
prompt = """
请用简单的语言解释以下概念：
- 机器学习
- 深度学习
- 神经网络
"""

# 发送请求到 Claude
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

# 提取并显示文本响应
text_response = response.content[0].text
print(text_response)
```

### 错误处理

在 Notebook 中包含适当的错误处理：

```python
try:
    response = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    print("✓ 请求成功")
    print(response.content[0].text)
except Exception as e:
    print(f"✗ 错误: {e}")
    print("请检查您的 API 密钥和网络连接")
```

### 练习题格式

```python
# 练习 1: 编写一个提示词，让 Claude 扮演历史老师
# 
# 提示：使用角色定义和清晰的指令
# 
# 在下面编写您的代码：

# 您的代码
prompt = """
# 在这里编写您的提示词
"""

# 测试您的提示词
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
)

print(response.content[0].text)
```

### Notebook 元数据

在 Notebook 开头包含元数据：

```markdown
# 第 X 章：章节标题

**作者**: Anthropic  
**最后更新**: 2024-12-02  
**预计时间**: 30 分钟  
**难度**: 初级/中级/高级

---
```

## 文档编写规范

### Markdown 格式

#### 标题层级

- 使用清晰的标题层级
- 不跳过层级（不要从 # 直接跳到 ###）

```markdown
# 一级标题 - 文档标题
## 二级标题 - 主要章节
### 三级标题 - 子章节
#### 四级标题 - 详细说明
```

#### 列表

- 使用 `-` 作为无序列表标记
- 使用 `1.` 作为有序列表标记
- 保持列表项的一致性

```markdown
## 功能特性

- 交互式学习
- 实时反馈
- 多版本支持

## 安装步骤

1. 克隆仓库
2. 安装依赖
3. 配置环境
4. 启动 Jupyter
```

#### 代码块

- 指定语言以启用语法高亮
- 使用描述性的注释

````markdown
```python
# Python 代码示例
def hello_world():
    print("Hello, World!")
```

```bash
# Bash 命令示例
pip install anthropic
```
````

#### 链接

- 使用描述性的链接文本
- 内部链接使用相对路径

```markdown
# 正确
查看[安装指南](../getting-started/installation.md)了解详情。
访问 [Anthropic 官方文档](https://docs.anthropic.com/)。

# 错误
点击[这里](../getting-started/installation.md)。
访问 https://docs.anthropic.com/。
```

#### 强调

- 使用 `**粗体**` 强调重要内容
- 使用 `*斜体*` 表示术语或引用
- 使用 `` `代码` `` 标记代码、命令、文件名

```markdown
**重要**：请确保已设置 API 密钥。

*提示工程*（Prompt Engineering）是一门艺术。

运行 `jupyter notebook` 启动服务器。
```

### 中文写作规范

#### 标点符号

- 中文内容使用中文标点：`，。！？：；""''（）`
- 英文内容使用英文标点：`, . ! ? : ; "" '' ()`
- 代码和命令使用英文标点

```markdown
# 正确
这是一个示例。使用 `pip install` 命令安装。

# 错误
这是一个示例.使用 `pip install` 命令安装.
```

#### 中英文混排

- 中英文之间添加空格
- 中文与数字之间添加空格
- 专有名词保持原文

```markdown
# 正确
使用 Claude 3 Haiku 模型进行测试。
项目包含 9 个章节和 50 个练习。

# 错误
使用Claude 3 Haiku模型进行测试。
项目包含9个章节和50个练习。
```

#### 术语使用

- 首次出现时提供英文原文
- 使用术语表中的标准译名
- 保持术语使用的一致性

```markdown
# 正确
提示工程（Prompt Engineering）是设计和优化提示词的技术。
后续章节将深入探讨提示工程的最佳实践。

# 错误
提示工程（Prompt Engineering）是设计和优化提示词的技术。
后续章节将深入探讨 Prompt Engineering 的最佳实践。
```

### 文档结构

每个文档应包含：

1. **标题**：清晰的文档标题
2. **目录**：主要章节的链接
3. **概述**：文档目的和内容简介
4. **主体内容**：详细的说明和示例
5. **相关资源**：相关文档的链接
6. **元数据**：最后更新时间、维护者

```markdown
# 文档标题

## 目录

- [章节 1](#章节-1)
- [章节 2](#章节-2)

## 概述

本文档介绍...

## 章节 1

内容...

## 相关资源

- [开发指南](./development-guide.md)
- [贡献指南](./contributing.md)
- [架构设计](./architecture.md)

---

**最后更新**：2024-12-02  
**维护者**：项目团队
```

## Git 提交规范

### 提交信息格式

```
<类型>: <简短描述>

[可选的详细描述]

[可选的关联 Issue]
```

### 提交类型

- `feat`: 新功能
- `fix`: Bug 修复
- `docs`: 文档更新
- `style`: 代码格式调整（不影响功能）
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关
- `perf`: 性能优化

### 提交示例

```bash
# 新功能
git commit -m "feat: 添加第 10 章 - 高级提示技巧"

# Bug 修复
git commit -m "fix: 修复 API 密钥验证逻辑错误"

# 文档更新
git commit -m "docs: 更新安装指南的 Windows 说明"

# 代码重构
git commit -m "refactor: 重构提示词模板管理器"

# 详细描述
git commit -m "feat: 添加批量处理功能

- 支持批量发送提示词
- 添加进度显示
- 实现错误重试机制

关闭 #123"
```

### 提交最佳实践

1. **原子性提交**：每次提交只包含一个逻辑变更
2. **清晰描述**：简短但描述性的提交信息
3. **现在时态**：使用现在时态（"添加"而不是"添加了"）
4. **小写开头**：描述部分使用小写字母开头
5. **不超过 50 字符**：简短描述不超过 50 个字符
## 代码审查检查清单

### 提交前自查

在提交代码前，请检查以下项目：

#### Python 代码

- [ ] 代码遵循 PEP 8 规范
- [ ] 使用了类型注解
- [ ] 函数和类有完整的文档字符串
- [ ] 变量命名清晰且具有描述性
- [ ] 没有未使用的导入
- [ ] 没有调试代码（print、pdb 等）
- [ ] 错误处理适当
- [ ] 没有硬编码的敏感信息

#### Jupyter Notebook

- [ ] 单元格按逻辑顺序组织
- [ ] 所有单元格都能成功运行
- [ ] 输出已清理（如果需要）
- [ ] 包含适当的说明和注释
- [ ] 练习题格式统一
- [ ] 没有敏感信息（API 密钥等）

#### 文档

- [ ] Markdown 格式正确
- [ ] 链接有效
- [ ] 中英文混排规范
- [ ] 术语使用一致
- [ ] 代码示例可执行
- [ ] 包含目录和元数据

#### Git

- [ ] 提交信息格式正确
- [ ] 提交是原子性的
- [ ] 分支命名规范
- [ ] 没有提交敏感信息

### 代码审查者检查清单

审查他人代码时，关注以下方面：

#### 功能性

- [ ] 代码实现了预期功能
- [ ] 边界情况处理正确
- [ ] 错误处理完善
- [ ] 没有明显的 bug

#### 代码质量

- [ ] 代码清晰易读
- [ ] 逻辑合理
- [ ] 没有重复代码
- [ ] 函数和类职责单一
- [ ] 复杂度适中

#### 规范遵循

- [ ] 遵循项目代码规范
- [ ] 命名规范一致
- [ ] 注释和文档完整
- [ ] 测试充分

#### 性能和安全

- [ ] 没有明显的性能问题
- [ ] 没有安全隐患
- [ ] 资源使用合理

## 工具配置

### Black - 代码格式化

安装和配置 Black：

```bash
# 安装
pip install black

# 格式化单个文件
black your_file.py

# 格式化整个目录
black .

# 检查但不修改
black --check .
```

配置文件 `pyproject.toml`：

```toml
[tool.black]
line-length = 88
target-version = ['py37', 'py38', 'py39']
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
)/
'''
```

### isort - 导入排序

安装和配置 isort：

```bash
# 安装
pip install isort

# 排序单个文件
isort your_file.py

# 排序整个目录
isort .

# 检查但不修改
isort --check-only .
```

配置文件 `.isort.cfg`：

```ini
[settings]
profile = black
line_length = 88
multi_line_output = 3
include_trailing_comma = True
force_grid_wrap = 0
use_parentheses = True
ensure_newline_before_comments = True
```

### Pylint - 代码检查

安装和配置 Pylint：

```bash
# 安装
pip install pylint

# 检查单个文件
pylint your_file.py

# 检查整个目录
pylint your_package/

# 生成配置文件
pylint --generate-rcfile > .pylintrc
```

配置文件 `.pylintrc`（部分）：

```ini
[MASTER]
ignore=.git,__pycache__,.venv

[MESSAGES CONTROL]
disable=C0111,  # missing-docstring
        C0103,  # invalid-name
        R0913   # too-many-arguments

[FORMAT]
max-line-length=88
indent-string='    '

[BASIC]
good-names=i,j,k,ex,_,id
```

### Flake8 - 风格检查

安装和配置 Flake8：

```bash
# 安装
pip install flake8

# 检查代码
flake8 .

# 检查特定文件
flake8 your_file.py
```

配置文件 `.flake8`：

```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503
exclude =
    .git,
    __pycache__,
    .venv,
    build,
    dist
```

### mypy - 类型检查

安装和配置 mypy：

```bash
# 安装
pip install mypy

# 类型检查
mypy your_file.py

# 检查整个包
mypy your_package/
```

配置文件 `mypy.ini`：

```ini
[mypy]
python_version = 3.9
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True

[mypy-anthropic.*]
ignore_missing_imports = True

[mypy-boto3.*]
ignore_missing_imports = True
```

### Pre-commit Hooks

使用 pre-commit 自动运行检查：

```bash
# 安装
pip install pre-commit

# 安装 git hooks
pre-commit install
```

配置文件 `.pre-commit-config.yaml`：

```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.3.0
    hooks:
      - id: black
        language_version: python3.9

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/pycqa/flake8
    rev: 6.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
```

### VS Code 配置

`.vscode/settings.json`：

```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.linting.flake8Enabled": true,
  "python.formatting.provider": "black",
  "python.formatting.blackArgs": ["--line-length", "88"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "python.linting.pylintArgs": [
    "--disable=C0111,C0103"
  ],
  "[python]": {
    "editor.rulers": [88],
    "editor.tabSize": 4
  },
  "[markdown]": {
    "editor.wordWrap": "on",
    "editor.quickSuggestions": false
  },
  "jupyter.askForKernelRestart": false,
  "notebook.output.textLineLimit": 30
}
```

### Makefile 快捷命令

创建 `Makefile` 简化常用命令：

```makefile
.PHONY: format lint test clean

# 格式化代码
format:
	black .
	isort .

# 代码检查
lint:
	flake8 .
	pylint your_package/
	mypy your_package/

# 运行测试
test:
	pytest tests/

# 清理临时文件
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +

# 安装开发依赖
dev-install:
	pip install -r requirements-dev.txt
	pre-commit install

# 运行所有检查
check: format lint test
	@echo "所有检查通过！"
```

使用方式：

```bash
# 格式化代码
make format

# 运行检查
make lint

# 运行测试
make test

# 运行所有检查
make check
```

## 相关资源

### Python 规范

- [PEP 8 - Python 代码风格指南](https://pep8.org/)
- [PEP 257 - 文档字符串规范](https://www.python.org/dev/peps/pep-0257/)
- [Google Python 风格指南](https://google.github.io/styleguide/pyguide.html)
- [Python 类型注解](https://docs.python.org/3/library/typing.html)

### Jupyter Notebook

- [Jupyter Notebook 最佳实践](https://jupyter-notebook.readthedocs.io/)
- [数据科学 Notebook 规范](https://github.com/jupyter/jupyter/wiki/Jupyter-Notebook-Best-Practices)

### Markdown

- [Markdown 指南](https://www.markdownguide.org/)
- [GitHub Flavored Markdown](https://github.github.com/gfm/)
- [中文文案排版指北](https://github.com/sparanoid/chinese-copywriting-guidelines)

### Git

- [Git 提交信息规范](https://www.conventionalcommits.org/)
- [如何编写 Git 提交信息](https://chris.beams.io/posts/git-commit/)

### 工具文档

- [Black 文档](https://black.readthedocs.io/)
- [isort 文档](https://pycqa.github.io/isort/)
- [Pylint 文档](https://pylint.pycqa.org/)
- [Flake8 文档](https://flake8.pycqa.org/)
- [mypy 文档](https://mypy.readthedocs.io/)
- [pre-commit 文档](https://pre-commit.com/)

### 项目文档

- [架构设计](architecture.md) - 了解项目架构
- [开发指南](development-guide.md) - 环境搭建和开发流程
- [贡献指南](contributing.md) - 如何为项目做贡献
- [开发术语表](glossary-dev.md) - 开发相关术语中英文对照
- [完整术语表](../glossary.md) - 项目完整术语表

---

**最后更新**：2024-12-02  
**维护者**：项目团队

**注意**：本规范是指导性的，不是强制性的。在特殊情况下，可以根据实际需求灵活调整，但应保持整体一致性。
