# 版本对比

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
```python
anthropic==0.21.3
```

**Bedrock Anthropic SDK**：
```python
anthropic==0.21.3
boto3==1.34.74
botocore==1.34.74
awscli==1.32.74
```

**Bedrock Boto3**：
```python
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

### 从 Anthropic 1P 迁移到 Bedrock Anthropic SDK

**难度**：⭐⭐ (简单)

**主要变更**：
1. 更改导入语句：`from anthropic import AnthropicBedrock`
2. 更改客户端初始化：使用 AWS 区域而非 API 密钥
3. 更新模型名称：添加 Bedrock 模型 ID 前缀
4. 配置 AWS 凭证

**代码变更示例**：
```python
# 之前 (Anthropic 1P)
import anthropic
client = anthropic.Anthropic(api_key=API_KEY)
model = "claude-3-haiku-20240307"

# 之后 (Bedrock Anthropic SDK)
from anthropic import AnthropicBedrock
client = AnthropicBedrock(aws_region=AWS_REGION)
model = "anthropic.claude-3-haiku-20240307-v1:0"
```

### 从 Anthropic 1P 迁移到 Bedrock Boto3

**难度**：⭐⭐⭐⭐ (较难)

**主要变更**：
1. 完全更改 SDK：从 Anthropic SDK 切换到 Boto3
2. 重写 API 调用逻辑：使用 JSON 序列化
3. 更改响应处理：解析 JSON 响应
4. 配置 AWS 凭证

**代码变更示例**：
```python
# 之前 (Anthropic 1P)
import anthropic
client = anthropic.Anthropic(api_key=API_KEY)
message = client.messages.create(
    model="claude-3-haiku-20240307",
    max_tokens=2000,
    messages=[{"role": "user", "content": prompt}]
)
response = message.content[0].text

# 之后 (Bedrock Boto3)
import boto3
import json
bedrock = boto3.client('bedrock-runtime', region_name=AWS_REGION)
body = json.dumps({
    "anthropic_version": '',
    "max_tokens": 2000,
    "messages": [{"role": "user", "content": prompt}],
    "temperature": 0.0
})
response = bedrock.invoke_model(
    body=body, 
    modelId="anthropic.claude-3-haiku-20240307-v1:0"
)
response_body = json.loads(response.get('body').read())
result = response_body.get('content')[0].get('text')
```

### 在 Bedrock 版本间迁移

**从 Bedrock Anthropic SDK 到 Bedrock Boto3**：

**难度**：⭐⭐⭐ (中等)

这需要重写 API 调用逻辑，但 AWS 配置可以保持不变。

**从 Bedrock Boto3 到 Bedrock Anthropic SDK**：

**难度**：⭐⭐ (简单)

这是一个简化过程，可以使用更高级的 API 接口。

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
