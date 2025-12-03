# 配置说明文档

## 目录

- [概述](#概述)
- [环境变量配置](#环境变量配置)
- [API 密钥配置](#api-密钥配置)
- [模型配置](#模型配置)
- [Notebook 配置](#notebook-配置)
- [版本特定配置](#版本特定配置)
- [高级配置](#高级配置)
- [故障排除](#故障排除)

---

## 概述

本文档说明如何配置 Claude 提示工程教程的各种选项和环境变量。正确的配置是成功运行教程的关键。

> **版本说明**：不同版本的配置方式有所不同：
> - 🟦 **Anthropic 1P**：需要 Anthropic API 密钥
> - 🟧 **Bedrock Anthropic SDK**：需要 AWS 凭证和区域配置
> - 🟨 **Bedrock Boto3**：需要 AWS 凭证和区域配置
> 
> 详细的版本特定配置请参考 [版本特定配置](#版本特定配置) 部分。

### 配置层级

1. **环境变量**：系统级配置
2. **配置文件**：项目级配置
3. **代码内配置**：运行时配置

---

## 环境变量配置

### 核心环境变量

#### `ANTHROPIC_API_KEY`

**说明**：Anthropic API 密钥

**必需性**：必需

**设置方法**：

**Linux/macOS**：
```bash
# 临时设置（当前会话）
export ANTHROPIC_API_KEY="your_api_key_here"

# 永久设置（添加到 ~/.bashrc 或 ~/.zshrc）
echo 'export ANTHROPIC_API_KEY="your_api_key_here"' >> ~/.bashrc
source ~/.bashrc
```

**Windows (PowerShell)**：
```powershell
# 临时设置
$env:ANTHROPIC_API_KEY="your_api_key_here"

# 永久设置
[System.Environment]::SetEnvironmentVariable('ANTHROPIC_API_KEY', 'your_api_key_here', 'User')
```

**Windows (CMD)**：
```cmd
# 临时设置
set ANTHROPIC_API_KEY=your_api_key_here

# 永久设置
setx ANTHROPIC_API_KEY "your_api_key_here"
```

#### `MODEL_NAME`

**说明**：默认使用的 Claude 模型

**必需性**：可选（有默认值）

**默认值**：`claude-3-haiku-20240307`

**可选值**：
- `claude-3-opus-20240229`
- `claude-3-sonnet-20240229`
- `claude-3-haiku-20240307`
- `claude-2.1`
- `claude-2.0`

**设置方法**：
```bash
export MODEL_NAME="claude-3-sonnet-20240229"
```

### AWS Bedrock 环境变量

如果使用 AWS Bedrock 版本，需要额外配置：

#### `AWS_ACCESS_KEY_ID`

**说明**：AWS 访问密钥 ID

**必需性**：使用 Bedrock 时必需

```bash
export AWS_ACCESS_KEY_ID="your_aws_access_key"
```

#### `AWS_SECRET_ACCESS_KEY`

**说明**：AWS 秘密访问密钥

**必需性**：使用 Bedrock 时必需

```bash
export AWS_SECRET_ACCESS_KEY="your_aws_secret_key"
```

#### `AWS_REGION`

**说明**：AWS 区域

**必需性**：使用 Bedrock 时必需

**默认值**：`us-east-1`

```bash
export AWS_REGION="us-west-2"
```

### 使用 .env 文件

创建 `.env` 文件来管理环境变量：

```bash
# .env 文件示例
ANTHROPIC_API_KEY=your_api_key_here
MODEL_NAME=claude-3-haiku-20240307

# AWS Bedrock 配置（如果使用）
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1
```

**加载 .env 文件**：

```python
# 使用 python-dotenv
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")
model_name = os.getenv("MODEL_NAME", "claude-3-haiku-20240307")
```

**安装 python-dotenv**：
```bash
pip install python-dotenv
```

---

## API 密钥配置

### 获取 API 密钥

1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 注册或登录账户
3. 导航到 API Keys 页面
4. 创建新的 API 密钥
5. 复制并安全保存密钥

### 密钥安全最佳实践

**DO（应该做）**：
- ✅ 使用环境变量存储密钥
- ✅ 使用 `.env` 文件（添加到 `.gitignore`）
- ✅ 使用密钥管理服务（如 AWS Secrets Manager）
- ✅ 定期轮换密钥
- ✅ 为不同环境使用不同密钥

**DON'T（不应该做）**：
- ❌ 在代码中硬编码密钥
- ❌ 将密钥提交到版本控制
- ❌ 在公共场所分享密钥
- ❌ 在日志中打印密钥
- ❌ 在客户端代码中暴露密钥

### 密钥验证

验证 API 密钥是否正确配置：

```python
import anthropic
import os

def verify_api_key():
    """验证 API 密钥配置"""
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        print("❌ 未找到 API 密钥")
        print("请设置 ANTHROPIC_API_KEY 环境变量")
        return False
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        # 发送测试请求
        message = client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print("✅ API 密钥验证成功")
        return True
    except anthropic.AuthenticationError:
        print("❌ API 密钥无效")
        return False
    except Exception as e:
        print(f"❌ 验证失败：{e}")
        return False

# 运行验证
verify_api_key()
```

---

## 模型配置

### 模型选择

根据需求选择合适的模型：

| 需求 | 推荐模型 | 原因 |
|------|----------|------|
| 学习教程 | Claude 3 Haiku | 快速、成本低 |
| 复杂任务 | Claude 3 Opus | 最强大、最准确 |
| 生产环境 | Claude 3 Sonnet | 平衡性能和成本 |
| 预算有限 | Claude 3 Haiku | 最经济 |

### 模型配置示例

**在 Notebook 中配置**：

```python
# 00_Tutorial_How-To.ipynb
API_KEY = "your_api_key_here"
MODEL_NAME = "claude-3-haiku-20240307"

# 存储到 IPython store
%store API_KEY
%store MODEL_NAME
```

**在 Python 脚本中配置**：

```python
import os
from anthropic import Anthropic

# 从环境变量读取
API_KEY = os.getenv("ANTHROPIC_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "claude-3-haiku-20240307")

client = Anthropic(api_key=API_KEY)
```

### 模型参数配置

**基本配置**：
```python
DEFAULT_CONFIG = {
    "model": "claude-3-haiku-20240307",
    "max_tokens": 2000,
    "temperature": 0.0
}
```

**自定义配置**：
```python
CUSTOM_CONFIG = {
    "model": "claude-3-sonnet-20240229",
    "max_tokens": 4000,
    "temperature": 0.7,
    "top_p": 0.9,
    "stop_sequences": ["\n\nHuman:"]
}
```

---

## Notebook 配置

### IPython Store

教程使用 IPython store 在 Notebook 间共享变量：

**存储变量**：
```python
# 在第一个 Notebook 中
API_KEY = "your_api_key"
MODEL_NAME = "claude-3-haiku-20240307"

%store API_KEY
%store MODEL_NAME
```

**读取变量**：
```python
# 在后续 Notebook 中
%store -r API_KEY
%store -r MODEL_NAME
```

**查看所有存储的变量**：
```python
%store
```

**删除变量**：
```python
%store -d API_KEY
```

### Jupyter 配置

**自动重载模块**：
```python
%load_ext autoreload
%autoreload 2
```

**设置显示选项**：
```python
import pandas as pd

# 显示更多行
pd.set_option('display.max_rows', 100)

# 显示更多列
pd.set_option('display.max_columns', 50)
```

---

## 版本特定配置

### Anthropic 1P 版本

**依赖安装**：
```bash
pip install anthropic
```

**配置示例**：
```python
import anthropic

client = anthropic.Anthropic(
    api_key="your_api_key_here"
)

def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

### Bedrock Anthropic SDK 版本

**依赖安装**：
```bash
pip install anthropic[bedrock]
```

**配置示例**：
```python
from anthropic import AnthropicBedrock

client = AnthropicBedrock(
    aws_access_key="your_aws_access_key",
    aws_secret_key="your_aws_secret_key",
    aws_region="us-east-1"
)

def get_completion(prompt: str):
    message = client.messages.create(
        model="anthropic.claude-3-haiku-20240307-v1:0",
        max_tokens=2000,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text
```

**Bedrock 模型 ID 映射**：
```python
BEDROCK_MODEL_IDS = {
    "claude-3-opus": "anthropic.claude-3-opus-20240229-v1:0",
    "claude-3-sonnet": "anthropic.claude-3-sonnet-20240229-v1:0",
    "claude-3-haiku": "anthropic.claude-3-haiku-20240307-v1:0",
    "claude-2.1": "anthropic.claude-v2:1",
    "claude-2.0": "anthropic.claude-v2"
}
```

### Bedrock Boto3 版本

**依赖安装**：
```bash
pip install boto3
```

**配置示例**：
```python
import boto3
import json

bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-east-1',
    aws_access_key_id='your_access_key',
    aws_secret_access_key='your_secret_key'
)

def get_completion(prompt: str):
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 2000,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    })
    
    response = bedrock.invoke_model(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        body=body
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']
```

**AWS 凭证配置**：

使用 AWS CLI 配置：
```bash
aws configure
```

或使用配置文件 `~/.aws/credentials`：
```ini
[default]
aws_access_key_id = your_access_key
aws_secret_access_key = your_secret_key
region = us-east-1
```

---

## 高级配置

### 超时配置

**设置请求超时**：
```python
from anthropic import Anthropic

client = Anthropic(
    api_key=API_KEY,
    timeout=300.0  # 5 分钟超时
)
```

**自定义超时策略**：
```python
from anthropic import Anthropic
import httpx

# 创建自定义 HTTP 客户端
http_client = httpx.Client(
    timeout=httpx.Timeout(
        connect=10.0,  # 连接超时
        read=300.0,    # 读取超时
        write=10.0,    # 写入超时
        pool=5.0       # 连接池超时
    )
)

client = Anthropic(
    api_key=API_KEY,
    http_client=http_client
)
```

### 重试配置

**配置重试策略**：
```python
from anthropic import Anthropic

client = Anthropic(
    api_key=API_KEY,
    max_retries=3  # 最多重试 3 次
)
```

**自定义重试逻辑**：
```python
import time
from anthropic import Anthropic, RateLimitError

def api_call_with_retry(prompt, max_retries=3):
    """带指数退避的重试"""
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-3-haiku-20240307",
                max_tokens=1024,
                messages=[{"role": "user", "content": prompt}]
            )
        except RateLimitError:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # 指数退避
                print(f"速率限制，等待 {wait_time} 秒...")
                time.sleep(wait_time)
            else:
                raise
```

### 代理配置

**使用 HTTP 代理**：
```python
from anthropic import Anthropic
import httpx

# 配置代理
proxies = {
    "http://": "http://proxy.example.com:8080",
    "https://": "http://proxy.example.com:8080"
}

http_client = httpx.Client(proxies=proxies)

client = Anthropic(
    api_key=API_KEY,
    http_client=http_client
)
```

### 日志配置

**启用详细日志**：
```python
import logging

# 配置日志级别
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Anthropic SDK 日志
logging.getLogger("anthropic").setLevel(logging.DEBUG)
```

**自定义日志处理**：
```python
import logging

# 创建日志处理器
handler = logging.FileHandler('api_calls.log')
handler.setLevel(logging.INFO)

# 创建格式化器
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
handler.setFormatter(formatter)

# 添加到 logger
logger = logging.getLogger("anthropic")
logger.addHandler(handler)
```

### 并发配置

**异步客户端配置**：
```python
from anthropic import AsyncAnthropic

async_client = AsyncAnthropic(
    api_key=API_KEY,
    max_retries=3,
    timeout=300.0
)
```

**连接池配置**：
```python
import httpx
from anthropic import Anthropic

# 配置连接池
limits = httpx.Limits(
    max_keepalive_connections=20,
    max_connections=100
)

http_client = httpx.Client(limits=limits)

client = Anthropic(
    api_key=API_KEY,
    http_client=http_client
)
```

---

## 故障排除

### 常见配置问题

#### 问题 1：找不到 API 密钥

**症状**：
```
AuthenticationError: API key not found
```

**解决方案**：
1. 检查环境变量是否设置：
   ```bash
   echo $ANTHROPIC_API_KEY
   ```

2. 在 Python 中验证：
   ```python
   import os
   print(os.getenv("ANTHROPIC_API_KEY"))
   ```

3. 确保在正确的 shell 中设置了变量

#### 问题 2：模型不可用

**症状**：
```
BadRequestError: Model not found
```

**解决方案**：
1. 检查模型名称拼写
2. 确认模型在您的区域可用
3. 使用正确的模型 ID（特别是 Bedrock）

#### 问题 3：连接超时

**症状**：
```
TimeoutError: Request timed out
```

**解决方案**：
1. 增加超时时间：
   ```python
   client = Anthropic(api_key=API_KEY, timeout=600.0)
   ```

2. 检查网络连接
3. 检查防火墙设置

#### 问题 4：速率限制

**症状**：
```
RateLimitError: Rate limit exceeded
```

**解决方案**：
1. 实现重试逻辑
2. 减少请求频率
3. 考虑升级 API 计划
4. 使用批处理

#### 问题 5：AWS 凭证问题

**症状**：
```
NoCredentialsError: Unable to locate credentials
```

**解决方案**：
1. 配置 AWS CLI：
   ```bash
   aws configure
   ```

2. 检查凭证文件：
   ```bash
   cat ~/.aws/credentials
   ```

3. 设置环境变量：
   ```bash
   export AWS_ACCESS_KEY_ID="your_key"
   export AWS_SECRET_ACCESS_KEY="your_secret"
   ```

### 配置验证脚本

完整的配置验证脚本：

```python
import os
import sys

def validate_configuration():
    """验证所有配置"""
    print("=== 配置验证 ===\n")
    
    # 1. 检查 API 密钥
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if api_key:
        print("✅ API 密钥已设置")
        print(f"   密钥前缀: {api_key[:10]}...")
    else:
        print("❌ API 密钥未设置")
        print("   请设置 ANTHROPIC_API_KEY 环境变量")
        return False
    
    # 2. 检查模型配置
    model_name = os.getenv("MODEL_NAME", "claude-3-haiku-20240307")
    print(f"✅ 模型: {model_name}")
    
    # 3. 测试 API 连接
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=api_key)
        
        message = client.messages.create(
            model=model_name,
            max_tokens=10,
            messages=[{"role": "user", "content": "Hi"}]
        )
        print("✅ API 连接成功")
        print(f"   响应: {message.content[0].text}")
        
    except Exception as e:
        print(f"❌ API 连接失败: {e}")
        return False
    
    # 4. 检查依赖
    try:
        import anthropic
        print(f"✅ anthropic 版本: {anthropic.__version__}")
    except ImportError:
        print("❌ anthropic 未安装")
        print("   运行: pip install anthropic")
        return False
    
    print("\n=== 配置验证完成 ===")
    return True

if __name__ == "__main__":
    success = validate_configuration()
    sys.exit(0 if success else 1)
```

运行验证：
```bash
python validate_config.py
```

---

## 配置模板

### 开发环境配置

```bash
# .env.development
ANTHROPIC_API_KEY=your_dev_api_key
MODEL_NAME=claude-3-haiku-20240307
LOG_LEVEL=DEBUG
MAX_RETRIES=3
TIMEOUT=300
```

### 生产环境配置

```bash
# .env.production
ANTHROPIC_API_KEY=your_prod_api_key
MODEL_NAME=claude-3-sonnet-20240229
LOG_LEVEL=INFO
MAX_RETRIES=5
TIMEOUT=600
```

### 测试环境配置

```bash
# .env.test
ANTHROPIC_API_KEY=your_test_api_key
MODEL_NAME=claude-3-haiku-20240307
LOG_LEVEL=WARNING
MAX_RETRIES=1
TIMEOUT=60
```

---

## 相关资源

- [安装指南](../getting-started/installation.md)
- [快速开始](../getting-started/quickstart.md)
- [API 参考](api-reference.md)
- [版本对比](../versions/comparison.md)
- [问题排查](../advanced/troubleshooting.md)

---

**文档版本**：1.0  
**最后更新**：2024-01  
**适用版本**：所有版本

