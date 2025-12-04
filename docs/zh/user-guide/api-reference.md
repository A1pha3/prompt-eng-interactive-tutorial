# API 参考文档

## 目录

- [概述](#概述)
- [Anthropic Python SDK](#anthropic-python-sdk)
- [Messages API](#messages-api)
- [辅助函数](#辅助函数)
- [参数详解](#参数详解)
- [错误处理](#错误处理)
- [最佳实践](#最佳实践)

---

## 概述

本文档提供 Claude API 的完整参考，包括所有可用的方法、参数和返回值。本教程主要使用 Anthropic Python SDK 和 Messages API。

### 版本信息

- **SDK 版本**：anthropic >= 0.18.0
- **Python 版本**：>= 3.7
- **API 版本**：2023-06-01

### 安装

```bash
pip install anthropic
```

---

## Anthropic Python SDK

### 客户端初始化

#### `anthropic.Anthropic()`

创建 Anthropic API 客户端实例。

**参数**：
- `api_key` (str, 必需): Anthropic API 密钥
- `base_url` (str, 可选): API 基础 URL，默认为 `https://api.anthropic.com`
- `timeout` (float, 可选): 请求超时时间（秒），默认为 600
- `max_retries` (int, 可选): 最大重试次数，默认为 2

**返回值**：
- `Anthropic`: 客户端实例

**示例**：
```python
import anthropic

# 基本初始化
client = anthropic.Anthropic(
    api_key="your_api_key_here"
)

# 自定义配置
client = anthropic.Anthropic(
    api_key="your_api_key_here",
    timeout=300,
    max_retries=3
)
```

**注意事项**：
- API 密钥应该从环境变量或安全存储中读取，不要硬编码
- 可以设置环境变量 `ANTHROPIC_API_KEY` 来避免显式传递

---

## Messages API

### `client.messages.create()`

创建一个新的消息，这是与 Claude 交互的主要方法。

#### 必需参数

**`model`** (str, 必需)
- 要使用的模型名称
- 可选值：
  - `claude-3-opus-20240229` - 最强大的模型
  - `claude-3-sonnet-20240229` - 平衡性能和成本
  - `claude-3-haiku-20240307` - 最快速的模型
  - `claude-2.1` - 上一代模型
  - `claude-2.0` - 上一代模型

**示例**：
```python
model="claude-3-haiku-20240307"
```

**`max_tokens`** (int, 必需)
- 生成的最大 token 数量
- 范围：1 到模型的最大上下文长度
- 这是一个硬性限制，可能导致输出截断

**示例**：
```python
max_tokens=1024  # 生成最多 1024 个 tokens
```

**`messages`** (list, 必需)
- 对话消息数组
- 每条消息必须包含 `role` 和 `content`
- 必须以 `user` 角色开始
- `user` 和 `assistant` 角色必须交替

**格式**：
```python
messages=[
    {
        "role": "user",
        "content": "你好！"
    },
    {
        "role": "assistant",
        "content": "你好！有什么可以帮助你的吗？"
    },
    {
        "role": "user",
        "content": "请介绍一下你自己。"
    }
]
```

#### 可选参数

**`system`** (str, 可选)
- 系统提示，用于设定 Claude 的行为和上下文
- 在消息数组之外单独指定

**示例**：
```python
system="你是一位专业的 Python 编程导师，擅长用简单的语言解释复杂概念。"
```

**`temperature`** (float, 可选)
- 控制输出的随机性
- 范围：0.0 到 1.0
- 默认值：1.0
- 较低的值（如 0.0）产生更确定性的输出
- 较高的值产生更多样化的输出

**示例**：
```python
temperature=0.0  # 最确定性的输出
temperature=0.7  # 平衡创造性和一致性
temperature=1.0  # 最大创造性
```

**`top_p`** (float, 可选)
- 核采样参数
- 范围：0.0 到 1.0
- 与 temperature 一起控制输出多样性
- 不建议同时调整 temperature 和 top_p

**`top_k`** (int, 可选)
- 只从概率最高的 k 个 token 中采样
- 用于控制输出的多样性

**`metadata`** (dict, 可选)
- 附加元数据，用于跟踪和分析
- 包含 `user_id` 等信息

**示例**：
```python
metadata={
    "user_id": "user_123"
}
```

**`stop_sequences`** (list, 可选)
- 自定义停止序列
- 当生成这些序列时，模型将停止生成

**示例**：
```python
stop_sequences=["\n\nHuman:", "\n\nAssistant:"]
```

**`stream`** (bool, 可选)
- 是否使用流式响应
- 默认值：False

#### 完整示例

```python
import anthropic

client = anthropic.Anthropic(api_key="your_api_key")

message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=1024,
    temperature=0.0,
    system="你是一位有帮助的助手。",
    messages=[
        {
            "role": "user",
            "content": "解释什么是机器学习。"
        }
    ]
)

print(message.content[0].text)
```

#### 返回值

返回一个 `Message` 对象，包含以下字段：

**`id`** (str)
- 消息的唯一标识符

**`type`** (str)
- 固定值："message"

**`role`** (str)
- 固定值："assistant"

**`content`** (list)
- 内容块数组
- 每个块包含 `type` 和 `text`

**`model`** (str)
- 使用的模型名称

**`stop_reason`** (str)
- 停止原因：
  - `end_turn` - 自然结束
  - `max_tokens` - 达到最大 token 限制
  - `stop_sequence` - 遇到停止序列

**`usage`** (dict)
- Token 使用统计
  - `input_tokens` - 输入 token 数
  - `output_tokens` - 输出 token 数

**示例响应**：
```python
{
    "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
    "type": "message",
    "role": "assistant",
    "content": [
        {
            "type": "text",
            "text": "机器学习是人工智能的一个分支..."
        }
    ],
    "model": "claude-3-haiku-20240307",
    "stop_reason": "end_turn",
    "usage": {
        "input_tokens": 15,
        "output_tokens": 120
    }
}
```

---

## 辅助函数

本教程中使用的辅助函数，简化 API 调用。

### `get_completion()`

基本的完成函数，用于简单的单轮对话。

**函数签名**：
```python
def get_completion(prompt: str, system_prompt: str = "") -> str
```

**参数**：
- `prompt` (str, 必需): 用户提示
- `system_prompt` (str, 可选): 系统提示，默认为空字符串

**返回值**：
- `str`: Claude 的响应文本

**实现**：
```python
import anthropic

client = anthropic.Anthropic(api_key=API_KEY)

def get_completion(prompt: str, system_prompt: str = "") -> str:
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        system=system_prompt,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text
```

**使用示例**：
```python
# 基本使用
response = get_completion("你好，Claude！")
print(response)

# 使用系统提示
response = get_completion(
    prompt="解释量子计算",
    system_prompt="你是一位物理学教授，用简单的语言解释复杂概念。"
)
print(response)
```

### 变体函数

#### `get_completion_with_history()`

支持多轮对话的完成函数。

```python
def get_completion_with_history(
    messages: list,
    system_prompt: str = "",
    model: str = "claude-3-haiku-20240307",
    max_tokens: int = 2000,
    temperature: float = 0.0
) -> str:
    """
    使用对话历史获取完成。
    
    参数:
        messages: 消息历史数组
        system_prompt: 系统提示
        model: 模型名称
        max_tokens: 最大 token 数
        temperature: 温度参数
    
    返回:
        Claude 的响应文本
    """
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=messages
    )
    return message.content[0].text
```

**使用示例**：
```python
conversation = [
    {"role": "user", "content": "什么是 Python？"},
    {"role": "assistant", "content": "Python 是一种高级编程语言..."},
    {"role": "user", "content": "它有什么优点？"}
]

response = get_completion_with_history(conversation)
print(response)
```

#### `get_completion_streaming()`

流式响应函数，实时获取生成的内容。

```python
def get_completion_streaming(
    prompt: str,
    system_prompt: str = ""
):
    """
    流式获取完成，实时输出。
    
    参数:
        prompt: 用户提示
        system_prompt: 系统提示
    
    生成:
        逐块生成的文本
    """
    with client.messages.stream(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        system=system_prompt,
        messages=[{"role": "user", "content": prompt}]
    ) as stream:
        for text in stream.text_stream:
            yield text
```

**使用示例**：
```python
for chunk in get_completion_streaming("写一首关于春天的诗"):
    print(chunk, end="", flush=True)
```

---

## 参数详解

### 模型选择指南

| 模型 | 特点 | 适用场景 | 上下文窗口 |
|------|------|----------|------------|
| Claude 3 Opus | 最强大，最准确 | 复杂推理、创意写作 | 200K tokens |
| Claude 3 Sonnet | 平衡性能和成本 | 通用任务、数据处理 | 200K tokens |
| Claude 3 Haiku | 最快速，成本最低 | 简单任务、高吞吐量 | 200K tokens |
| Claude 2.1 | 上一代，稳定 | 遗留系统集成 | 200K tokens |

### Token 计算

**估算规则**：
- 英文：1 token ≈ 4 个字符 ≈ 0.75 个单词
- 中文：1 token ≈ 1-2 个汉字
- 代码：取决于语言和格式

**示例**：
```text
# 英文
"Hello, world!" ≈ 4 tokens

# 中文
"你好，世界！" ≈ 5-6 tokens

# 代码
"def hello(): print('hi')" ≈ 10 tokens
```

**查看实际使用**：
```python
message = client.messages.create(...)
print(f"输入 tokens: {message.usage['input_tokens']}")
print(f"输出 tokens: {message.usage['output_tokens']}")
```

### Temperature 使用指南

**Temperature = 0.0**
- 最确定性的输出
- 适用场景：
  - 数据提取
  - 代码生成
  - 事实性问答
  - 需要一致性的任务

**Temperature = 0.3-0.7**
- 平衡创造性和一致性
- 适用场景：
  - 内容生成
  - 对话系统
  - 文本改写

**Temperature = 0.8-1.0**
- 最大创造性
- 适用场景：
  - 创意写作
  - 头脑风暴
  - 生成多样化的想法

### 系统提示最佳实践

**有效的系统提示**：
```python
# ✅ 好的系统提示
system_prompt = """你是一位经验丰富的 Python 导师。

教学风格：
- 使用简单的语言解释概念
- 提供实际的代码示例
- 鼓励最佳实践
- 指出常见错误

在回答时：
1. 先解释概念
2. 提供代码示例
3. 说明注意事项
4. 建议进一步学习资源"""
```

**无效的系统提示**：
```python
# ❌ 不好的系统提示
system_prompt = "你是一个助手。帮助用户。"  # 太笼统
```

---

## 错误处理

### 常见错误类型

#### `AuthenticationError`

**原因**：API 密钥无效或缺失

**处理**：
```python
try:
    message = client.messages.create(...)
except anthropic.AuthenticationError as e:
    print(f"认证失败：{e}")
    print("请检查您的 API 密钥")
```

#### `RateLimitError`

**原因**：超过速率限制

**处理**：
```python
import time

try:
    message = client.messages.create(...)
except anthropic.RateLimitError as e:
    print(f"速率限制：{e}")
    print("等待后重试...")
    time.sleep(60)  # 等待 60 秒
    # 重试请求
```

#### `BadRequestError`

**原因**：请求参数无效

**处理**：
```python
try:
    message = client.messages.create(...)
except anthropic.BadRequestError as e:
    print(f"请求错误：{e}")
    print("请检查您的参数")
```

#### `APIError`

**原因**：API 服务器错误

**处理**：
```python
try:
    message = client.messages.create(...)
except anthropic.APIError as e:
    print(f"API 错误：{e}")
    print("请稍后重试")
```

### 完整错误处理示例

```python
import anthropic
import time

def safe_api_call(prompt, max_retries=3):
    """
    带重试机制的安全 API 调用
    """
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
            
        except anthropic.AuthenticationError:
            print("认证失败，请检查 API 密钥")
            return None
            
        except anthropic.RateLimitError:
            wait_time = (attempt + 1) * 30
            print(f"速率限制，等待 {wait_time} 秒...")
            time.sleep(wait_time)
            
        except anthropic.BadRequestError as e:
            print(f"请求参数错误：{e}")
            return None
            
        except anthropic.APIError as e:
            print(f"API 错误（尝试 {attempt + 1}/{max_retries}）：{e}")
            if attempt < max_retries - 1:
                time.sleep(5)
            else:
                return None
    
    return None
```

---

## 最佳实践

### 1. API 密钥管理

**使用环境变量**：
```python
import os
from anthropic import Anthropic

# 从环境变量读取
api_key = os.environ.get("ANTHROPIC_API_KEY")
client = Anthropic(api_key=api_key)
```

**使用配置文件**：
```python
import json

# 从配置文件读取
with open("config.json") as f:
    config = json.load(f)
    
client = Anthropic(api_key=config["api_key"])
```

### 2. Token 优化

**控制输入长度**：
```python
def truncate_text(text, max_tokens=1000):
    """
    截断文本以适应 token 限制
    """
    # 粗略估算：1 token ≈ 4 字符
    max_chars = max_tokens * 4
    if len(text) > max_chars:
        return text[:max_chars] + "..."
    return text
```

**批量处理**：
```python
def process_batch(items, batch_size=10):
    """
    批量处理以优化 API 调用
    """
    results = []
    for i in range(0, len(items), batch_size):
        batch = items[i:i+batch_size]
        # 将批次合并为单个请求
        combined_prompt = "\n\n".join(batch)
        result = get_completion(combined_prompt)
        results.append(result)
    return results
```

### 3. 缓存策略

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_completion(prompt: str) -> str:
    """
    缓存相同提示的结果
    """
    return get_completion(prompt)
```

### 4. 异步调用

```python
import asyncio
from anthropic import AsyncAnthropic

async_client = AsyncAnthropic(api_key=API_KEY)

async def async_completion(prompt: str) -> str:
    """
    异步 API 调用
    """
    message = await async_client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

# 并发处理多个请求
async def process_multiple(prompts: list) -> list:
    tasks = [async_completion(p) for p in prompts]
    return await asyncio.gather(*tasks)
```

### 5. 日志记录

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def logged_completion(prompt: str) -> str:
    """
    带日志的 API 调用
    """
    logger.info(f"发送请求，提示长度：{len(prompt)}")
    
    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        logger.info(f"收到响应，tokens: {message.usage}")
        return message.content[0].text
        
    except Exception as e:
        logger.error(f"API 调用失败：{e}")
        raise
```

---

## 相关资源

- [完整使用手册](user-guide.md)
- [配置说明](configuration.md)
- [示例集合](examples.md)
- [Anthropic 官方 API 文档](https://docs.anthropic.com/claude/reference/)

---

**文档版本**：1.0  
**最后更新**：2024-01  
**适用 SDK 版本**：anthropic >= 0.18.0

