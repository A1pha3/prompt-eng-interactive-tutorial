# 欢迎来到 Anthropic 提示工程交互式教程

## 课程简介与目标

本课程旨在为您提供全面、循序渐进的指导，帮助您掌握如何在 Claude 中设计最优提示词。

**完成本课程后，您将能够**：
- 掌握优质提示词的基本结构
- 识别常见的失败模式，并学习"二八法则"技巧来解决这些问题
- 理解 Claude 的优势和局限性
- 从零开始为常见用例构建强大的提示词

## 课程结构与内容

本课程的设计为您提供了大量练习编写和调试提示词的机会。课程分为 **9 个章节及配套练习**，以及一个包含更多高级方法的附录。建议您**按章节顺序学习**。

**每节课底部都有一个"示例练习场"区域**，您可以在此自由实验课程中的示例，亲自体验修改提示词如何改变 Claude 的响应。此外还有一个[答案参考](https://docs.google.com/spreadsheets/d/1jIxjzUWG-6xBVIa2ay6yDpLyeuOh_hR_ZB75a47KX_E/edit?usp=sharing)。

注意：本教程使用我们最小、最快、最经济的模型 Claude 3 Haiku。Anthropic 还有[另外两个模型](https://docs.anthropic.com/claude/docs/models-overview)：Claude 3 Sonnet 和 Claude 3 Opus，它们比 Haiku 更智能，其中 Opus 是最智能的。

*本教程也有 [Google Sheets 版本，使用 Anthropic 的 Claude for Sheets 扩展](https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8/edit?usp=sharing)。我们推荐使用该版本，因为它更加用户友好。*

准备好开始时，请前往 `01_Basic Prompt Structure` 继续学习。

## 版本说明

本教程提供三个不同的实现版本，适用于不同的使用场景：

### 🟦 Anthropic 1P（第一方 API）
**位置**：`Anthropic 1P/` 目录  
**适用场景**：快速开始、个人学习、原型开发  
**特点**：使用 Anthropic 官方 API，配置简单，功能最新

### 🟧 Bedrock Anthropic SDK
**位置**：`AmazonBedrock/anthropic/` 目录  
**适用场景**：AWS 企业用户、需要 AWS 集成  
**特点**：通过 AWS Bedrock 使用 Anthropic SDK，保持熟悉的 API 风格

### 🟨 Bedrock Boto3
**位置**：`AmazonBedrock/boto3/` 目录  
**适用场景**：深度 AWS 集成、需要底层控制  
**特点**：使用 AWS 原生 Boto3 SDK，完全的 AWS 原生体验

**如何选择？** 查看 [版本对比文档](docs/zh/versions/comparison.md) 了解详细差异和选择建议。

## 目录

每个章节包含一节课程和一组练习。

### 初级
- **第 1 章：** 基本提示词结构

- **第 2 章：** 清晰直接的表达

- **第 3 章：** 角色分配

### 中级
- **第 4 章：** 分离数据与指令

- **第 5 章：** 格式化输出与为 Claude 代言

- **第 6 章：** 预知（逐步思考）

- **第 7 章：** 使用示例

### 高级
- **第 8 章：** 避免幻觉

- **第 9 章：** 构建复杂提示词（行业用例）
  - 从零开始构建复杂提示词 - 聊天机器人
  - 法律服务的复杂提示词
  - **练习：** 金融服务的复杂提示词
  - **练习：** 编程的复杂提示词
  - 恭喜与下一步

- **附录：** 超越标准提示
  - 提示词链接
  - 工具使用
  - 搜索与检索



## 快速开始

### 前置要求

- Python 3.7 或更高版本
- Jupyter Notebook 或 JupyterLab
- Anthropic API 密钥（Anthropic 1P 版本）或 AWS 账户（Bedrock 版本）

### 安装步骤

详细的安装指南请参阅[安装文档](docs/zh/getting-started/installation.md)。

快速安装（Anthropic 1P 版本）：

```bash
# 克隆仓库
git clone <repository-url>
cd <repository-name>

# 安装依赖
pip install anthropic jupyter

# 启动 Jupyter Notebook
jupyter notebook
```

### 5 分钟快速上手

完整的快速开始教程请参阅[快速开始文档](docs/zh/getting-started/quickstart.md)。

## 📖 完整文档地图

本项目提供全面的中文文档体系，涵盖从入门到进阶的所有内容。以下是完整的文档导航：

### 📚 入门文档（Getting Started）

新手必读，快速上手教程：

- **[安装指南](docs/zh/getting-started/installation.md)**  
  详细的安装步骤、环境配置、依赖项说明，支持 macOS、Linux 和 Windows 系统。包含常见安装问题的故障排除。

- **[快速开始](docs/zh/getting-started/quickstart.md)**  
  5 分钟快速上手教程，通过第一个示例快速体验 Claude 提示工程的核心功能。

### 📖 使用文档（User Guide）

深入了解功能和使用方法：

- **[完整使用手册](docs/zh/user-guide/user-guide.md)**  
  涵盖所有 9 个章节的详细说明，从基本提示结构到复杂提示构建的完整学习路径。包含每章的学习目标、关键概念和实践练习。

- **[API 参考](docs/zh/user-guide/api-reference.md)**  
  完整的 API 接口文档，包含所有可用方法、参数说明、返回值和代码示例。按功能模块组织，便于查找。

- **[配置说明](docs/zh/user-guide/configuration.md)**  
  详细的配置选项和环境变量说明，包含不同版本的配置差异和配置文件示例。

- **[示例集合](docs/zh/user-guide/examples.md)**  
  从 Notebook 中提取的实用示例，按使用场景分类，每个示例都包含说明和预期输出。

### 🔧 开发文档（Development）

为项目做出贡献：

- **[架构设计](docs/zh/development/architecture.md)**  
  项目的整体架构和设计模式，包含架构图和各组件的职责说明。帮助理解项目结构。

- **[开发指南](docs/zh/development/development-guide.md)**  
  开发环境搭建的详细步骤，包含如何运行和调试项目，以及开发工具推荐。

- **[贡献指南](docs/zh/development/contributing.md)**  
  如何为项目贡献代码和文档，包含代码提交流程、Pull Request 规范和审查检查清单。

- **[代码规范](docs/zh/development/code-style.md)**  
  Python 代码风格规范、Notebook 编写规范和文档编写规范，确保代码质量和一致性。

- **[开发术语表](docs/zh/development/glossary-dev.md)**  
  开发相关的中英文术语对照表，确保技术术语使用的一致性。

### 🚀 进阶文档（Advanced）

深度技术内容和最佳实践：

- **[设计原理](docs/zh/advanced/design-principles.md)**  
  提示工程的核心设计原理和教学理念，解析关键设计决策的背景和理由。

- **[性能优化](docs/zh/advanced/performance.md)**  
  提示优化的最佳实践，如何提高响应速度和质量，包含性能测试和基准测试方法。

- **[问题排查](docs/zh/advanced/troubleshooting.md)**  
  常见问题和解决方案，按问题类型分类组织，提供调试技巧和工具推荐。

- **[常见问题 FAQ](docs/zh/advanced/faq.md)**  
  高频问题解答，涵盖使用、配置、开发等各方面的常见疑问。

### 🔄 版本文档（Versions）

了解不同版本的特性和选择：

- **[版本对比](docs/zh/versions/comparison.md)**  
  Anthropic 1P、Bedrock Anthropic SDK、Bedrock Boto3 三个版本的详细对比，包含特性对比表格和版本选择建议。

- **[Anthropic 1P 版本](docs/zh/versions/anthropic-1p.md)**  
  Anthropic 官方 API 版本的特点、适用场景、配置说明和专门示例。

- **[Bedrock Anthropic SDK 版本](docs/zh/versions/bedrock-anthropic.md)**  
  AWS Bedrock Anthropic SDK 版本的特点、AWS 配置说明和使用示例。

- **[Bedrock Boto3 版本](docs/zh/versions/bedrock-boto3.md)**  
  AWS Bedrock Boto3 版本的特点、Boto3 配置说明和使用示例。

- **[版本文档中心](docs/zh/versions/README.md)**  
  版本文档的总览和快速导航。

### 📝 其他资源

- **[术语表](docs/zh/glossary.md)**  
  完整的中英文技术术语对照表，确保文档中术语使用的一致性。

- **[文档模板](docs/zh/templates/README.md)**  
  文档编写模板和规范，用于创建新文档或扩展现有文档。

- **[中文文档中心](docs/zh/README.md)**  
  中文文档的总入口，提供文档导航和快速链接。

---

## 🎯 快速导航

根据您的需求，选择合适的起点：

### 我是新手，想快速开始
1. 📥 阅读 [安装指南](docs/zh/getting-started/installation.md) 配置环境
2. ⚡ 完成 [快速开始](docs/zh/getting-started/quickstart.md) 教程
3. 📚 浏览 [示例集合](docs/zh/user-guide/examples.md) 学习实践
4. 🔄 查看 [版本对比](docs/zh/versions/comparison.md) 选择适合的版本

### 我想深入学习提示工程
1. 📖 阅读 [完整使用手册](docs/zh/user-guide/user-guide.md) 系统学习
2. 🔍 查看 [API 参考](docs/zh/user-guide/api-reference.md) 了解接口
3. 🎓 学习 [设计原理](docs/zh/advanced/design-principles.md) 理解核心概念
4. 🚀 研究 [性能优化](docs/zh/advanced/performance.md) 提升技能

### 我想为项目做贡献
1. 🏗️ 了解 [架构设计](docs/zh/development/architecture.md) 理解项目结构
2. 💻 阅读 [开发指南](docs/zh/development/development-guide.md) 搭建环境
3. 📋 查看 [贡献指南](docs/zh/development/contributing.md) 了解流程
4. ✨ 遵循 [代码规范](docs/zh/development/code-style.md) 保证质量

### 我遇到了问题
1. ❓ 查看 [常见问题 FAQ](docs/zh/advanced/faq.md) 寻找答案
2. 🔧 参考 [问题排查](docs/zh/advanced/troubleshooting.md) 解决问题
3. 📖 检查 [配置说明](docs/zh/user-guide/configuration.md) 确认配置
4. 💬 在 GitHub 提交 Issue 获取帮助

### 我需要选择版本
1. 📊 阅读 [版本对比](docs/zh/versions/comparison.md) 了解差异
2. 🟦 查看 [Anthropic 1P](docs/zh/versions/anthropic-1p.md) - 适合快速开始
3. 🟧 查看 [Bedrock Anthropic SDK](docs/zh/versions/bedrock-anthropic.md) - 适合 AWS 用户
4. 🟨 查看 [Bedrock Boto3](docs/zh/versions/bedrock-boto3.md) - 适合深度 AWS 集成

## 术语表

完整的中英文术语对照表请参阅[术语表](docs/zh/glossary.md)。

## 贡献

我们欢迎各种形式的贡献！请阅读[贡献指南](docs/zh/development/contributing.md)了解如何参与项目。

## 许可证

请参阅 [LICENSE](LICENSE) 文件了解详情。

## 相关资源

- [Anthropic 官方文档](https://docs.anthropic.com/)
- [Claude API 参考](https://docs.anthropic.com/claude/reference/)
- [Amazon Bedrock 文档](https://docs.aws.amazon.com/bedrock/)
- [提示工程指南](https://docs.anthropic.com/claude/docs/prompt-engineering)

## 联系方式

如有问题或建议，请通过以下方式联系我们：
- 提交 Issue
- 发起 Pull Request
- 查看[常见问题](docs/zh/advanced/faq.md)

---

**English Version**: [README_EN.md](README_EN.md)
