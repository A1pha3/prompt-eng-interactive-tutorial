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
