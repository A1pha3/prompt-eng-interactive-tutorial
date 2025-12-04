# Anthropic 1P 版本文档

## 目录

- [概述](#概述)
- [目标读者](#目标读者)
- [版本特点](#版本特点)
- [前置条件](#前置条件)
- [安装指南](#安装指南)
- [配置说明](#配置说明)
- [使用示例](#使用示例)
- [教程结构](#教程结构)
- [最佳实践](#最佳实践)
- [故障排除](#故障排除)
- [版本更新](#版本更新)
- [相关资源](#相关资源)
- [下一步](#下一步)

---

## 概述

Anthropic 1P（第一方）版本是使用 Anthropic 官方 API 的原生实现。这是最直接、最简单的方式来使用 Claude 模型，适合快速开发、学习和实验。

**版本标识**：🟦 Anthropic 1P

**目录位置**：`Anthropic 1P/`

## 目标读者

- 希望快速开始学习 Claude 提示工程的初学者
- 进行原型开发和实验的开发者
- 不依赖 AWS 基础设施的个人用户
- 需要使用最新 Claude 功能的研究人员

## 版本特点

### 核心优势

✅ **简单直接**
- 最少的配置步骤
- 清晰的 API 接口
- 快速上手

✅ **最新功能**
- 第一时间获得新模型和功能
- 直接访问 Anthropic 的最新更新
- 完整的功能支持

✅ **独立部署**
- 不依赖云服务提供商
- 灵活的部署选择
- 简单的依赖管理

✅ **透明定价**
- 按 token 使用量计费
- 清晰的定价结构
- 无隐藏费用

### 适用场景

- 🎓 **学习和教育**：最适合学习提示工程的版本
- 🔬 **研究和实验**：快速测试新想法和方法
- 🚀 **原型开发**：快速构建概念验证
- 💻 **个人项目**：小规模应用和工具开发

### 不适用场景

- ❌ 需要与 AWS 服务深度集成
- ❌ 企业级合规和审计要求
- ❌ 需要 AWS 企业支持和 SLA
- ❌ 已有 AWS 基础设施且希望统一管理

## 前置条件

### 1. Anthropic API 密钥

您需要一个有效的 Anthropic API 密钥。

**获取方式**：
1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册或登录您的账户
3. 在 API Keys 页面创建新的 API 密钥
4. 安全保存您的密钥（密钥只显示一次）

**定价信息**：
- 查看最新定价：[Anthropic Pricing](https://www.anthropic.com/pricing)
- 按输入和输出 token 分别计费
- 不同模型有不同的定价

### 2. Python 环境

- Python 3.7 或更高版本
- pip 包管理器
- Jupyter Notebook（用于运行教程）

### 3. 系统要求

- 稳定的互联网连接
- 足够的磁盘空间（约 100MB）
- 支持的操作系统：Windows、macOS、Linux

## 安装指南

### 步骤 1：克隆仓库

```bash
git clone https://github.com/anthropics/prompt-eng-interactive-tutorial.git
cd prompt-eng-interactive-tutorial
```

### 步骤 2：进入 Anthropic 1P 目录

```bash
cd "Anthropic 1P"
```

### 步骤 3：安装依赖

使用 pip 安装 Anthropic Python SDK：

```bash
pip install anthropic
```

**依赖版本**：
```
anthropic==0.21.3
```

### 步骤 4：启动 Jupyter Notebook

```bash
jupyter notebook
```

这将在浏览器中打开 Jupyter Notebook 界面。

### 步骤 5：配置 API 密钥

打开 `00_Tutorial_How-To.ipynb` 文件，在相应的单元格中设置您的 API 密钥：

```ipython
API_KEY = "your_api_key_here"  # 替换为您的实际 API 密钥
MODEL_NAME = "claude-3-haiku-20240307"

# 存储变量供其他 notebook 使用
%store API_KEY
%store MODEL_NAME
```

**安全提示**：
- ⚠️ 不要将 API 密钥提交到版本控制系统
- ⚠️ 不要在公共场合分享您的 API 密钥
- ⚠️ 定期轮换您的 API 密钥
- ⚠️ 使用环境变量存储敏感信息

### 步骤 6：验证安装

运行以下代码验证配置是否正确：

```python
import anthropic

client = anthropic.Anthropic(api_key=API_KEY)

def get_completion(prompt: str):
    message = client.messages.create(
        model=MODEL_NAME,
        max_tokens=2000,
        temperature=0.0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

# 测试
print(get_completion("Hello, Claude!"))
```

如果看到 Claude 的回复，说明配置成功！

## 配置说明

### API 客户端配置

#### 基本配置

```python
import anthropic

# 创建客户端
client = anthropic.Anthropic(
    api_key="your_api_key_here"
)
```

#### 使用环境变量

推荐使用环境变量存储 API 密钥：

```python
import os
import anthropic

# 从环境变量读取
client = anthropic.Anthropic(
    api_key=os.environ.get("ANTHROPIC_API_KEY")
)
```

设置环境变量：

**Linux/macOS**：
```bash
export ANTHROPIC_API_KEY="your_api_key_here"
```

**Windows (PowerShell)**：
```powershell
$env:ANTHROPIC_API_KEY="your_api_key_here"
```

**Windows (CMD)**：
```cmd
set ANTHROPIC_API_KEY=your_api_key_here
```

### 模型选择

Anthropic 1P 版本支持所有 Anthropic 模型：

```python
# Claude 3 系列
MODEL_NAME = "claude-3-opus-20240229"    # 最强大
MODEL_NAME = "claude-3-sonnet-20240229"  # 平衡性能
MODEL_NAME = "claude-3-haiku-20240307"   # 最快速（教程默认）

# Claude 2 系列（传统模型）
MODEL_NAME = "claude-2.1"
MODEL_NAME = "claude-2.0"
```

**模型选择建议**：
- **学习教程**：使用 `claude-3-haiku-20240307`（快速且经济）
- **生产应用**：根据需求选择 Sonnet 或 Opus
- **成本优化**：Haiku < Sonnet < Opus

### API 参数配置

```python
message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=2000,        # 最大输出 token 数
    temperature=0.0,        # 温度（0-1，越高越随机）
    messages=[
        {"role": "user", "content": "Your prompt here"}
    ],
    system="Optional system prompt",  # 可选的系统提示
    stop_sequences=["\n\n"]  # 可选的停止序列
)
```

**参数说明**：
- `model`：要使用的模型名称
- `max_tokens`：生成的最大 token 数（必需）
- `temperature`：控制输出随机性（0 = 确定性，1 = 最随机）
- `messages`：对话消息列表
- `system`：系统级指令（可选）
- `stop_sequences`：遇到这些序列时停止生成（可选）

## 使用示例

### 示例 1：基本对话

```python
import anthropic

client = anthropic.Anthropic(api_key=API_KEY)

def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        temperature=0.0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

# 使用
response = get_completion("解释什么是提示工程")
print(response)
```

### 示例 2：使用系统提示

```python
def get_completion_with_system(prompt: str, system: str = ""):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        temperature=0.0,
        system=system,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return message.content[0].text

# 使用
system_prompt = "你是一位专业的 Python 编程导师"
response = get_completion_with_system(
    "如何使用列表推导式？",
    system_prompt
)
print(response)
```

### 示例 3：多轮对话

```python
def chat(messages: list):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        temperature=0.0,
        messages=messages
    )
    return message.content[0].text

# 构建对话历史
conversation = [
    {"role": "user", "content": "什么是机器学习？"},
]

# 第一轮
response1 = chat(conversation)
print("Claude:", response1)

# 添加回复到历史
conversation.append({"role": "assistant", "content": response1})

# 第二轮
conversation.append({"role": "user", "content": "能举个例子吗？"})
response2 = chat(conversation)
print("Claude:", response2)
```


### 示例 4：流式响应

```python
def stream_completion(prompt: str):
    with client.messages.stream(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        temperature=0.0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    ) as stream:
        for text in stream.text_stream:
            print(text, end="", flush=True)
    print()  # 换行

# 使用
stream_completion("写一首关于编程的短诗")
```

## 教程结构

Anthropic 1P 版本包含以下教程文件：

### 核心教程

1. **00_Tutorial_How-To.ipynb** - 教程使用指南
2. **01_Basic_Prompt_Structure.ipynb** - 基本提示结构
3. **02_Being_Clear_and_Direct.ipynb** - 清晰直接的表达
4. **03_Assigning_Roles_Role_Prompting.ipynb** - 角色分配
5. **04_Separating_Data_and_Instructions.ipynb** - 分离数据和指令
6. **05_Formatting_Output_and_Speaking_for_Claude.ipynb** - 格式化输出
7. **06_Precognition_Thinking_Step_by_Step.ipynb** - 逐步思考
8. **07_Using_Examples_Few-Shot_Prompting.ipynb** - 少样本提示
9. **08_Avoiding_Hallucinations.ipynb** - 避免幻觉
10. **09_Complex_Prompts_from_Scratch.ipynb** - 复杂提示构建

### 附录教程

- **10.1_Appendix_Chaining Prompts.ipynb** - 提示链接
- **10.2_Appendix_Tool Use.ipynb** - 工具使用
- **10.3_Appendix_Search & Retrieval.ipynb** - 搜索和检索

### 辅助文件

- **hints.py** - 提示和答案辅助函数

## 最佳实践

### 1. API 密钥管理

**推荐做法**：
```python
# 使用环境变量
import os
API_KEY = os.environ.get("ANTHROPIC_API_KEY")

# 或使用配置文件（不要提交到 Git）
import json
with open("config.json") as f:
    config = json.load(f)
    API_KEY = config["api_key"]
```

**避免做法**：
```python
# ❌ 不要硬编码 API 密钥
API_KEY = "sk-ant-api03-..."  # 危险！

# ❌ 不要在代码中明文存储
client = anthropic.Anthropic(api_key="sk-ant-api03-...")
```

### 2. 错误处理

```python
import anthropic
from anthropic import APIError, APIConnectionError, RateLimitError

def safe_completion(prompt: str, max_retries: int = 3):
    for attempt in range(max_retries):
        try:
            message = client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return message.content[0].text
        
        except RateLimitError:
            print(f"速率限制，等待后重试... (尝试 {attempt + 1}/{max_retries})")
            time.sleep(2 ** attempt)  # 指数退避
        
        except APIConnectionError:
            print(f"连接错误，重试... (尝试 {attempt + 1}/{max_retries})")
            time.sleep(1)
        
        except APIError as e:
            print(f"API 错误: {e}")
            raise
    
    raise Exception("达到最大重试次数")
```

### 3. 成本控制

```python
def estimate_cost(input_tokens: int, output_tokens: int, model: str = "haiku"):
    # Claude 3 Haiku 定价（示例，请查看最新定价）
    prices = {
        "haiku": {"input": 0.25 / 1_000_000, "output": 1.25 / 1_000_000},
        "sonnet": {"input": 3.0 / 1_000_000, "output": 15.0 / 1_000_000},
        "opus": {"input": 15.0 / 1_000_000, "output": 75.0 / 1_000_000}
    }
    
    price = prices.get(model, prices["haiku"])
    cost = (input_tokens * price["input"]) + (output_tokens * price["output"])
    return cost

# 使用
response = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt}]
)

input_tokens = response.usage.input_tokens
output_tokens = response.usage.output_tokens
cost = estimate_cost(input_tokens, output_tokens, "haiku")

print(f"输入 tokens: {input_tokens}")
print(f"输出 tokens: {output_tokens}")
print(f"预估成本: ${cost:.6f}")
```

### 4. 性能优化

**批量处理**：
```python
import asyncio
from anthropic import AsyncAnthropic

async_client = AsyncAnthropic(api_key=API_KEY)

async def process_prompts(prompts: list):
    tasks = [
        async_client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            messages=[{"role": "user", "content": p}]
        )
        for p in prompts
    ]
    return await asyncio.gather(*tasks)

# 使用
prompts = ["提示1", "提示2", "提示3"]
responses = asyncio.run(process_prompts(prompts))
```

**缓存常用响应**：
```python
from functools import lru_cache

@lru_cache(maxsize=100)
def cached_completion(prompt: str):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

## 故障排除

### 常见问题

#### 1. API 密钥无效

**错误信息**：
```
anthropic.AuthenticationError: Invalid API key
```

**解决方案**：
- 检查 API 密钥是否正确复制
- 确认密钥未过期或被撤销
- 在 Anthropic Console 中验证密钥状态

#### 2. 速率限制

**错误信息**：
```
anthropic.RateLimitError: Rate limit exceeded
```

**解决方案**：
- 实现指数退避重试机制
- 减少并发请求数量
- 考虑升级到更高的速率限制层级
- 使用批量处理优化请求

#### 3. 连接超时

**错误信息**：
```
anthropic.APIConnectionError: Connection timeout
```

**解决方案**：
- 检查网络连接
- 增加超时时间
- 使用代理（如果在受限网络环境）
- 实现重试逻辑

#### 4. Token 限制超出

**错误信息**：
```
anthropic.BadRequestError: max_tokens exceeds model limit
```

**解决方案**：
- 减少 `max_tokens` 值
- 缩短输入提示
- 使用支持更长上下文的模型

### 调试技巧

#### 启用详细日志

```python
import logging

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# Anthropic SDK 日志
anthropic_logger = logging.getLogger("anthropic")
anthropic_logger.setLevel(logging.DEBUG)
```

#### 检查请求和响应

```python
def debug_completion(prompt: str):
    print(f"发送提示: {prompt[:100]}...")
    
    try:
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        print(f"模型: {message.model}")
        print(f"输入 tokens: {message.usage.input_tokens}")
        print(f"输出 tokens: {message.usage.output_tokens}")
        print(f"停止原因: {message.stop_reason}")
        
        return message.content[0].text
    
    except Exception as e:
        print(f"错误类型: {type(e).__name__}")
        print(f"错误信息: {str(e)}")
        raise
```

## 版本更新

### 检查 SDK 版本

```python
import anthropic
print(f"Anthropic SDK 版本: {anthropic.__version__}")
```

### 升级 SDK

```bash
pip install --upgrade anthropic
```

### 版本兼容性

本教程使用 `anthropic==0.21.3`。较新版本通常向后兼容，但建议查看 [发布说明](https://github.com/anthropics/anthropic-sdk-python/releases) 了解重大变更。

## 相关资源

### 官方文档

- [Anthropic API 文档](https://docs.anthropic.com/)
- [Python SDK 文档](https://github.com/anthropics/anthropic-sdk-python)
- [Claude 模型文档](https://docs.anthropic.com/claude/docs/models-overview)
- [API 参考](https://docs.anthropic.com/claude/reference/messages_post)

### 社区资源

- [Anthropic Discord](https://discord.gg/anthropic)
- [GitHub Issues](https://github.com/anthropics/anthropic-sdk-python/issues)
- [示例代码库](https://github.com/anthropics/anthropic-cookbook)

### 项目文档

- [版本对比](./comparison.md) - 了解不同版本的差异
- [安装指南](../getting-started/installation.md) - 详细安装说明
- [快速开始](../getting-started/quickstart.md) - 5 分钟快速上手
- [使用手册](../user-guide/user-guide.md) - 完整教程说明

## 下一步

1. **开始学习**：打开 `00_Tutorial_How-To.ipynb` 开始教程
2. **探索示例**：查看 [示例文档](../user-guide/examples.md)
3. **深入理解**：阅读 [设计原理](../advanced/design-principles.md)
4. **优化性能**：学习 [性能优化](../advanced/performance.md)

如需切换到其他版本，请参考：
- [Bedrock Anthropic SDK 版本](./bedrock-anthropic.md)
- [Bedrock Boto3 版本](./bedrock-boto3.md)
