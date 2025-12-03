# 版本文档

## 概述

本目录包含 Anthropic Claude 提示工程教程三个不同版本的详细文档。每个版本都有其独特的特点和适用场景。

## 版本标识

为了帮助用户快速识别版本相关内容，我们使用以下标识：

- 🟦 **Anthropic 1P**：Anthropic 第一方 API 版本
- 🟧 **Bedrock Anthropic SDK**：使用 Anthropic SDK 的 AWS Bedrock 版本
- 🟨 **Bedrock Boto3**：使用 Boto3 的 AWS Bedrock 版本

## 文档列表

### [版本对比](./comparison.md)
详细对比三个版本的特性、优缺点和适用场景，帮助您选择最适合的版本。

**包含内容**：
- 功能特性对比表
- 技术实现差异
- 成本对比
- 版本选择指南
- 版本迁移指南

### [Anthropic 1P 版本](./anthropic-1p.md)
🟦 使用 Anthropic 官方 API 的原生实现版本。

**适用场景**：
- 快速原型开发
- 个人学习和研究
- 需要最新功能
- 不依赖 AWS

### [Bedrock Anthropic SDK 版本](./bedrock-anthropic.md)
🟧 通过 AWS Bedrock 使用 Anthropic SDK 的版本。

**适用场景**：
- AWS 企业用户
- 需要 AWS 集成
- 从 Anthropic 1P 迁移
- 保持熟悉的 API

### [Bedrock Boto3 版本](./bedrock-boto3.md)
🟨 使用 AWS 原生 Boto3 SDK 的版本。

**适用场景**：
- 深度 AWS 集成
- 已使用 Boto3 的项目
- 需要底层控制
- AWS 原生应用

## 版本标注规范

在文档中使用版本标注时，请遵循以下规范：

### 1. 通用内容

对于适用于所有版本的内容，无需添加版本标注。

### 2. 版本特定内容

对于仅适用于特定版本的内容，使用以下格式：

```markdown
> **🟦 Anthropic 1P 专用**：此内容仅适用于 Anthropic 1P 版本。
```

或

```markdown
> **🟧 Bedrock Anthropic SDK 专用**：此内容仅适用于 Bedrock Anthropic SDK 版本。
```

或

```markdown
> **🟨 Bedrock Boto3 专用**：此内容仅适用于 Bedrock Boto3 版本。
```

### 3. 多版本适用

对于适用于多个版本的内容：

```markdown
> **🟧🟨 Bedrock 版本适用**：此内容适用于所有 Bedrock 版本。
```

### 4. 版本差异说明

当需要说明版本间的差异时：

```markdown
> **版本差异**：
> - 🟦 **Anthropic 1P**：使用 `anthropic.Anthropic(api_key=...)`
> - 🟧 **Bedrock Anthropic SDK**：使用 `AnthropicBedrock(aws_region=...)`
> - 🟨 **Bedrock Boto3**：使用 `boto3.client('bedrock-runtime')`
```

### 5. 版本选择提示

在文档开头提供版本选择提示：

```markdown
> **版本说明**：本文档涵盖所有版本。如需查看特定版本的详细信息，请参考：
> - [Anthropic 1P 版本文档](./anthropic-1p.md)
> - [Bedrock Anthropic SDK 版本文档](./bedrock-anthropic.md)
> - [Bedrock Boto3 版本文档](./bedrock-boto3.md)
```

## 快速导航

### 我应该选择哪个版本？

**如果您是新手**：
- 推荐从 🟦 Anthropic 1P 开始，最简单易用

**如果您使用 AWS**：
- 已有 AWS 基础设施 → 🟧 Bedrock Anthropic SDK
- 深度使用 Boto3 → 🟨 Bedrock Boto3

**如果您需要迁移**：
- 从 Anthropic 1P 到 AWS → 🟧 Bedrock Anthropic SDK（最平滑）

### 版本间如何迁移？

查看 [版本对比文档的迁移指南部分](./comparison.md#版本迁移指南)。

## 相关资源

- [主文档](../../../README.md)
- [安装指南](../getting-started/installation.md)
- [快速开始](../getting-started/quickstart.md)
- [使用手册](../user-guide/user-guide.md)

## 反馈和贡献

如果您发现版本文档有任何问题或建议，欢迎：
- 提交 Issue
- 提交 Pull Request
- 联系维护团队

---

**最后更新**：2024年12月

**维护者**：Anthropic 提示工程教程团队
