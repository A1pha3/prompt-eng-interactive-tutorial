# 版本对比

## 目录

- [概述](#概述)
- [目标读者](#目标读者)
- [三个版本概览](#三个版本概览)
- [详细特性对比](#详细特性对比)
- [版本选择指南](#版本选择指南)
- [版本迁移指南](#版本迁移指南)
- [常见问题](#常见问题)
- [相关资源](#相关资源)
- [下一步](#下一步)

---

## 概述

本教程提供三个不同的实现版本，分别适用于不同的使用场景和技术栈。本文档将帮助您了解各版本的特点、差异和适用场景，以便选择最适合您需求的版本。

## 目标读者

- 需要选择合适版本的新用户
- 考虑在不同版本间迁移的现有用户
- 希望了解各版本技术差异的开发者

## 三个版本概览

### 1. Anthropic 1P（第一方 API）

**位置**：`Anthropic 1P/` 目录

**简介**：使用 Anthropic 官方 API 的原生实现版本，直接连接到 Anthropic 的服务端点。

**核心特点**：
- 直接使用 Anthropic 官方 Python SDK
- 需要 Anthropic API 密钥
- 最新功能和模型的首发平台
- 简单直接的 API 调用方式

### 2. Bedrock Anthropic SDK

**位置**：`AmazonBedrock/anthropic/` 目录

**简介**：通过 Amazon Bedrock 平台使用 Anthropic SDK 访问 Claude 模型。

**核心特点**：
- 使用 Anthropic SDK 的 Bedrock 适配器
- 需要 AWS 账户和 Bedrock 访问权限
- 集成 AWS 生态系统
- 保持与 Anthropic SDK 相似的 API 接口

### 3. Bedrock Boto3

**位置**：`AmazonBedrock/boto3/` 目录

**简介**：使用 AWS Boto3 SDK 通过 Amazon Bedrock 访问 Claude 模型。

**核心特点**：
- 使用 AWS 原生 Boto3 SDK
- 需要 AWS 账户和 Bedrock 访问权限
- 完全的 AWS 原生体验
- 更底层的 API 控制

## 详细特性对比

### 功能特性对比表

| 特性 | Anthropic 1P | Bedrock Anthropic SDK | Bedrock Boto3 |
|------|--------------|----------------------|---------------|
| **API 提供商** | Anthropic 官方 | AWS Bedrock | AWS Bedrock |
| **SDK 类型** | Anthropic SDK | Anthropic SDK (Bedrock) | AWS Boto3 |
| **认证方式** | API 密钥 | AWS 凭证 | AWS 凭证 |
| **模型访问** | 所有 Anthropic 模型 | Bedrock 支持的模型 | Bedrock 支持的模型 |
| **新功能可用性** | 最快 | 稍后 | 稍后 |
| **AWS 集成** | 无 | 完整 | 完整 |
| **定价模式** | Anthropic 定价 | AWS Bedrock 定价 | AWS Bedrock 定价 |
| **区域可用性** | 全球 | AWS 区域限制 | AWS 区域限制 |
| **企业功能** | 基础 | AWS 企业功能 | AWS 企业功能 |
| **学习曲线** | 简单 | 中等 | 中等 |

### 技术实现对比

#### 依赖项

**Anthropic 1P**：
```text
anthropic==0.21.3
```

**Bedrock Anthropic SDK**：
```text
anthropic==0.21.3
boto3==1.34.74
botocore==1.34.74
awscli==1.32.74
```

**Bedrock Boto3**：
```text
boto3==1.34.74
botocore==1.34.74
awscli==1.32.74
```

#### 初始化方式

**Anthropic 1P**：
```python
import anthropic

client = anthropic.Anthropic(api_key=API_KEY)
```

**Bedrock Anthropic SDK**：
```python
from anthropic import AnthropicBedrock

client = AnthropicBedrock(aws_region=AWS_REGION)
```

**Bedrock Boto3**：
```python
import boto3

bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
```

#### API 调用方式

**Anthropic 1P**：
```python
message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=2000,
    temperature=0.0,
    messages=[
        {"role": "user", "content": prompt}
    ]
)
response = message.content[0].text
```

**Bedrock Anthropic SDK**：
```python
message = client.messages.create(
    model="anthropic.claude-3-haiku-20240307-v1:0",
    max_tokens=2000,
    temperature=0.0,
    messages=[
        {"role": "user", "content": prompt}
    ],
    system=system
)
response = message.content[0].text
```

**Bedrock Boto3**：
```python
import json

body = json.dumps({
    "anthropic_version": '',
    "max_tokens": 2000,
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.0,
    "top_p": 1,
    "system": ''
})

response = bedrock.invoke_model(body=body, modelId=MODEL_NAME)
response_body = json.loads(response.get('body').read())
result = response_body.get('content')[0].get('text')
```

### 成本对比

#### Anthropic 1P
- 按 Anthropic 官方定价计费
- 直接向 Anthropic 付费
- 定价透明，按 token 计费
- 适合小规模和中等规模使用

#### Bedrock 版本（Anthropic SDK 和 Boto3）
- 按 AWS Bedrock 定价计费
- 通过 AWS 账单付费
- 可能包含 AWS 数据传输费用
- 可利用 AWS 企业折扣和承诺使用折扣
- 适合已有 AWS 基础设施的企业

## 版本选择指南

### 选择 Anthropic 1P 的场景

✅ **推荐使用场景**：
- 快速原型开发和实验
- 个人学习和研究项目
- 需要最新 Claude 功能和模型
- 不依赖 AWS 基础设施
- 简单的集成需求

❌ **不推荐场景**：
- 需要与 AWS 服务深度集成
- 企业级合规和审计要求
- 需要 AWS 企业支持

### 选择 Bedrock Anthropic SDK 的场景

✅ **推荐使用场景**：
- 已有 AWS 基础设施
- 需要 AWS 企业功能（IAM、CloudWatch 等）
- 希望保持与 Anthropic SDK 相似的 API
- 从 Anthropic 1P 迁移到 AWS
- 需要 AWS 合规性和安全性

❌ **不推荐场景**：
- 不熟悉 AWS 生态系统
- 需要最底层的 AWS 控制
- 预算非常有限的个人项目

### 选择 Bedrock Boto3 的场景

✅ **推荐使用场景**：
- 深度集成 AWS 服务
- 已经使用 Boto3 管理其他 AWS 资源
- 需要完全的 AWS 原生体验
- 需要更细粒度的请求控制
- 企业级 AWS 应用

❌ **不推荐场景**：
- 不熟悉 AWS 和 Boto3
- 希望简化的 API 接口
- 快速原型开发

## 版本迁移指南

本节提供详细的版本迁移步骤和注意事项，帮助您顺利完成版本切换。

### 从 Anthropic 1P 迁移到 Bedrock Anthropic SDK

**难度**：⭐⭐ (简单)

**预计时间**：30-60 分钟

#### 迁移前准备

1. **AWS 账户设置**
   - 创建或登录 AWS 账户
   - 在支持的区域启用 Amazon Bedrock
   - 请求 Claude 模型访问权限（通常几分钟内批准）

2. **配置 AWS 凭证**
   ```bash
   aws configure
   # 输入 Access Key ID、Secret Access Key 和区域
   ```

3. **备份现有代码**
   - 创建代码备份或新分支
   - 记录当前 API 使用情况

#### 主要变更

1. **更新依赖项**
   ```bash
   # 安装 AWS 相关依赖
   pip install boto3 botocore awscli
   ```

2. **更改导入语句**
   ```python
# 之前
import anthropic

# 之后
from anthropic import AnthropicBedrock
   ```

3. **更改客户端初始化**
   - 使用 AWS 区域而非 API 密钥
   - 自动使用 AWS 凭证

4. **更新模型名称**
   - 添加 Bedrock 模型 ID 前缀和版本后缀

#### 详细迁移步骤

**步骤 1：更新客户端初始化**
```python
# 之前 (Anthropic 1P)
import anthropic
client = anthropic.Anthropic(api_key=API_KEY)

# 之后 (Bedrock Anthropic SDK)
from anthropic import AnthropicBedrock
client = AnthropicBedrock(aws_region="us-east-1")  # 指定 AWS 区域
```

**步骤 2：更新模型 ID**
```python
# 之前
model = "claude-3-haiku-20240307"

# 之后 - 添加前缀和版本后缀
model = "anthropic.claude-3-haiku-20240307-v1:0"
```

**模型 ID 对照表**：
| Anthropic 1P | Bedrock |
|--------------|---------|
| `claude-3-opus-20240229` | `anthropic.claude-3-opus-20240229-v1:0` |
| `claude-3-sonnet-20240229` | `anthropic.claude-3-sonnet-20240229-v1:0` |
| `claude-3-haiku-20240307` | `anthropic.claude-3-haiku-20240307-v1:0` |

**步骤 3：API 调用保持不变**
```python
# API 调用方式完全相同！
message = client.messages.create(
    model=model,
    max_tokens=2000,
    temperature=0.0,
    messages=[{"role": "user", "content": prompt}],
    system="可选的系统提示"
)
response = message.content[0].text
```

#### 迁移注意事项

**优势**：
- ✅ API 接口几乎完全兼容
- ✅ 最小化代码变更
- ✅ 保持熟悉的开发体验

**需要注意**：
- ⚠️ 确保 AWS 凭证正确配置
- ⚠️ 检查所选区域是否支持 Bedrock
- ⚠️ 更新所有模型 ID 引用
- ⚠️ 测试错误处理逻辑（错误类型可能不同）

**成本变化**：
- 从 Anthropic 直接计费改为 AWS Bedrock 计费
- 可能包含 AWS 数据传输费用
- 可利用 AWS 企业折扣

#### 迁移检查清单

- [ ] AWS 账户已设置并启用 Bedrock
- [ ] AWS 凭证已配置（`aws configure`）
- [ ] 已安装 boto3 和相关依赖
- [ ] 更新了导入语句
- [ ] 更新了客户端初始化代码
- [ ] 更新了所有模型 ID
- [ ] 测试了基本 API 调用
- [ ] 更新了错误处理逻辑
- [ ] 配置了 CloudWatch 监控（可选）
- [ ] 更新了文档和注释

### 从 Anthropic 1P 迁移到 Bedrock Boto3

**难度**：⭐⭐⭐⭐ (较难)

**预计时间**：2-4 小时

**建议**：如果可能，建议先迁移到 Bedrock Anthropic SDK，再根据需要迁移到 Boto3。

#### 迁移前准备

1. **完成 AWS 设置**（同上）
2. **熟悉 Boto3**
   - 了解 Boto3 的基本用法
   - 理解 JSON 请求/响应格式
3. **准备重构代码**
   - 这是一次较大的代码重构
   - 需要重写所有 API 调用逻辑

#### 主要变更

1. **完全更改 SDK**
   - 从 Anthropic SDK 切换到 Boto3
   - 不再使用 `anthropic` 包

2. **重写 API 调用逻辑**
   - 使用 JSON 序列化构建请求
   - 手动构建请求体

3. **更改响应处理**
   - 解析 JSON 响应
   - 提取嵌套的响应数据

4. **配置 AWS 凭证**（同上）

#### 详细迁移步骤

**步骤 1：更新依赖和导入**
```python
# 之前 (Anthropic 1P)
import anthropic
client = anthropic.Anthropic(api_key=API_KEY)

# 之后 (Bedrock Boto3)
import boto3
import json
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
```

**步骤 2：重写 API 调用函数**
```python
# 之前 (Anthropic 1P)
def get_completion(prompt: str):
    message = client.messages.create(
        model="claude-3-haiku-20240307",
        max_tokens=2000,
        temperature=0.0,
        messages=[{"role": "user", "content": prompt}]
    )
    return message.content[0].text

# 之后 (Bedrock Boto3)
def get_completion(prompt: str):
    # 1. 构建 JSON 请求体
    body = json.dumps({
        "anthropic_version": "",
        "max_tokens": 2000,
        "temperature": 0.0,
        "messages": [{"role": "user", "content": prompt}]
    })
    
    # 2. 调用 Bedrock API
    response = bedrock.invoke_model(
        body=body,
        modelId="anthropic.claude-3-haiku-20240307-v1:0"
    )
    
    # 3. 解析 JSON 响应
    response_body = json.loads(response['body'].read())
    return response_body['content'][0]['text']
```

**步骤 3：处理系统提示**
```python
# 之前
message = client.messages.create(
    model=model,
    max_tokens=2000,
    system="你是一个助手",
    messages=[{"role": "user", "content": prompt}]
)

# 之后 - 系统提示在请求体中
body = json.dumps({
    "anthropic_version": "",
    "max_tokens": 2000,
    "system": "你是一个助手",  # 添加到请求体
    "messages": [{"role": "user", "content": prompt}]
})
```

**步骤 4：处理流式响应**
```python
# 之前
with client.messages.stream(...) as stream:
    for text in stream.text_stream:
        print(text, end="")

# 之后
response = bedrock.invoke_model_with_response_stream(
    body=body,
    modelId=model_id
)

stream = response.get('body')
for event in stream:
    chunk = event.get('chunk')
    if chunk:
        chunk_data = json.loads(chunk.get('bytes').decode())
        if chunk_data['type'] == 'content_block_delta':
            if chunk_data['delta']['type'] == 'text_delta':
                print(chunk_data['delta']['text'], end='')
```

#### 迁移注意事项

**挑战**：
- ❌ 需要完全重写 API 调用代码
- ❌ 需要手动处理 JSON 序列化/反序列化
- ❌ 错误处理方式完全不同
- ❌ 响应结构需要手动解析

**优势**：
- ✅ 完全的 AWS 原生体验
- ✅ 更细粒度的控制
- ✅ 与其他 AWS 服务无缝集成
- ✅ 统一的 Boto3 错误处理

**错误处理变更**：
```python
# 之前 (Anthropic SDK)
from anthropic import APIError, RateLimitError
try:
    response = get_completion(prompt)
except RateLimitError:
    # 处理速率限制
    pass

# 之后 (Boto3)
from botocore.exceptions import ClientError
try:
    response = get_completion(prompt)
except ClientError as e:
    error_code = e.response['Error']['Code']
    if error_code == 'ThrottlingException':
        # 处理速率限制
        pass
```

#### 迁移检查清单

- [ ] AWS 账户和 Bedrock 已设置
- [ ] 已安装 boto3（不需要 anthropic 包）
- [ ] 重写了所有 API 调用函数
- [ ] 更新了请求体构建逻辑
- [ ] 更新了响应解析逻辑
- [ ] 重写了错误处理代码
- [ ] 测试了所有 API 功能
- [ ] 测试了流式响应（如使用）
- [ ] 更新了单元测试
- [ ] 更新了文档和注释

#### 迁移辅助工具

创建一个包装函数来简化迁移：

```python
class ClaudeBedrockWrapper:
    """简化 Boto3 调用的包装类"""
    
    def __init__(self, region_name='us-east-1'):
        self.client = boto3.client('bedrock-runtime', region_name=region_name)
        self.model_id = "anthropic.claude-3-haiku-20240307-v1:0"
    
    def create_message(self, messages, max_tokens=2000, temperature=0.0, system=""):
        body = json.dumps({
            "anthropic_version": "",
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": messages,
            "system": system
        })
        
        response = self.client.invoke_model(
            body=body,
            modelId=self.model_id
        )
        
        response_body = json.loads(response['body'].read())
        return response_body['content'][0]['text']

# 使用包装类
claude = ClaudeBedrockWrapper()
response = claude.create_message(
    messages=[{"role": "user", "content": "Hello"}]
)
```

### 在 Bedrock 版本间迁移

#### 从 Bedrock Anthropic SDK 到 Bedrock Boto3

**难度**：⭐⭐⭐ (中等)

**预计时间**：1-2 小时

**适用场景**：
- 需要更底层的 AWS 控制
- 希望统一使用 Boto3 管理所有 AWS 资源
- 需要与其他 Boto3 代码集成

**迁移步骤**：

1. **更新导入**
   ```python
# 之前
from anthropic import AnthropicBedrock
client = AnthropicBedrock(aws_region="us-east-1")

# 之后
import boto3
import json
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
   ```

2. **重写 API 调用**（参考上面的 Boto3 迁移步骤）

3. **AWS 配置保持不变**
   - 凭证配置无需更改
   - IAM 权限保持相同
   - 区域设置保持相同

**优势**：
- AWS 配置和权限无需更改
- 可以复用现有的 AWS 基础设施代码

#### 从 Bedrock Boto3 到 Bedrock Anthropic SDK

**难度**：⭐⭐ (简单)

**预计时间**：30-60 分钟

**适用场景**：
- 希望简化 API 调用代码
- 从 Anthropic 1P 迁移过来，希望保持熟悉的 API
- 不需要底层 Boto3 控制

**迁移步骤**：

1. **安装 Anthropic SDK**
   ```bash
   pip install anthropic
   ```

2. **更新导入和初始化**
   ```python
# 之前
import boto3
import json
bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')

# 之后
from anthropic import AnthropicBedrock
client = AnthropicBedrock(aws_region="us-east-1")
   ```

3. **简化 API 调用**
   ```python
# 之前 (Boto3) - 复杂
body = json.dumps({
    "anthropic_version": "",
    "max_tokens": 2000,
    "messages": [{"role": "user", "content": prompt}]
})
response = bedrock.invoke_model(body=body, modelId=model_id)
response_body = json.loads(response['body'].read())
text = response_body['content'][0]['text']

# 之后 (Anthropic SDK) - 简单
message = client.messages.create(
    model=model_id,
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt}]
)
text = message.content[0].text
   ```

**优势**：
- 代码更简洁易读
- 自动处理 JSON 序列化
- 更好的类型提示和 IDE 支持
- 与 Anthropic 1P API 保持一致

#### 迁移决策树

```
需要迁移版本？
│
├─ 从 Anthropic 1P 出发
│  │
│  ├─ 需要简单迁移？ → Bedrock Anthropic SDK
│  └─ 需要完全 AWS 原生？ → Bedrock Boto3
│
├─ 从 Bedrock Anthropic SDK 出发
│  │
│  ├─ 需要更多控制？ → Bedrock Boto3
│  └─ 保持现状 → 无需迁移
│
└─ 从 Bedrock Boto3 出发
   │
   ├─ 希望简化代码？ → Bedrock Anthropic SDK
   └─ 保持现状 → 无需迁移
```

#### 通用迁移最佳实践

1. **分阶段迁移**
   - 先在开发环境测试
   - 逐步迁移功能模块
   - 保持旧代码作为备份

2. **充分测试**
   - 单元测试
   - 集成测试
   - 性能测试
   - 成本测试

3. **监控和日志**
   - 设置 CloudWatch 监控
   - 记录迁移过程中的问题
   - 对比迁移前后的性能

4. **文档更新**
   - 更新代码注释
   - 更新 API 文档
   - 记录迁移经验

5. **团队培训**
   - 培训团队成员新 API
   - 分享迁移经验
   - 建立最佳实践文档

## 常见问题

### Q: 三个版本的教程内容是否相同？

A: 是的，所有版本都包含相同的提示工程教程内容和练习。唯一的区别在于技术实现和 API 调用方式。

### Q: 我可以在同一个项目中使用多个版本吗？

A: 技术上可以，但不推荐。建议选择一个版本并保持一致，以避免依赖冲突和代码复杂性。

### Q: Bedrock 版本支持哪些 AWS 区域？

A: Amazon Bedrock 的可用区域会不断更新。请查看 [AWS Bedrock 文档](https://docs.aws.amazon.com/bedrock/latest/userguide/what-is-bedrock.html) 获取最新的区域支持信息。

### Q: 哪个版本的性能最好？

A: 性能主要取决于网络延迟和地理位置：
- Anthropic 1P：连接到 Anthropic 服务器
- Bedrock 版本：连接到最近的 AWS 区域

选择地理位置最近的服务可以获得最佳性能。

### Q: 我需要为每个版本单独付费吗？

A: 不需要。您只需为实际使用的版本付费。选择一个版本后，只会产生该版本的相关费用。

## 相关资源

- [Anthropic 1P 版本文档](./anthropic-1p.md)
- [Bedrock Anthropic SDK 版本文档](./bedrock-anthropic.md)
- [Bedrock Boto3 版本文档](./bedrock-boto3.md)
- [Anthropic API 文档](https://docs.anthropic.com/)
- [AWS Bedrock 文档](https://docs.aws.amazon.com/bedrock/)

## 下一步

选择了适合您的版本后，请参考对应的版本文档进行详细配置和使用：

1. **Anthropic 1P**：查看 [Anthropic 1P 版本文档](./anthropic-1p.md)
2. **Bedrock Anthropic SDK**：查看 [Bedrock Anthropic SDK 版本文档](./bedrock-anthropic.md)
3. **Bedrock Boto3**：查看 [Bedrock Boto3 版本文档](./bedrock-boto3.md)

您也可以返回 [主文档](../../../README.md) 查看完整的文档导航。
