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

## 版本说明

本项目提供三个版本的教程实现：

1. **Anthropic 1P**：使用 Anthropic 官方 API
2. **Amazon Bedrock (Anthropic SDK)**：使用 AWS Bedrock 上的 Anthropic SDK
3. **Amazon Bedrock (Boto3)**：使用 AWS Boto3 SDK

请根据您的使用场景选择合适的版本。详细的版本对比和选择指南，请参阅[版本对比文档](docs/zh/versions/comparison.md)。

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

## 文档导航

### 📚 入门文档
- [安装指南](docs/zh/getting-started/installation.md) - 详细的安装步骤和环境配置
- [快速开始](docs/zh/getting-started/quickstart.md) - 5 分钟快速上手教程

### 📖 使用文档
- [完整使用手册](docs/zh/user-guide/user-guide.md) - 所有章节的详细说明
- [API 参考](docs/zh/user-guide/api-reference.md) - API 接口文档
- [配置说明](docs/zh/user-guide/configuration.md) - 配置选项和环境变量
- [示例集合](docs/zh/user-guide/examples.md) - 实用示例和最佳实践

### 🔧 开发文档
- [架构设计](docs/zh/development/architecture.md) - 项目架构和设计模式
- [开发指南](docs/zh/development/development-guide.md) - 开发环境搭建
- [贡献指南](docs/zh/development/contributing.md) - 如何为项目做贡献
- [代码规范](docs/zh/development/code-style.md) - 代码风格和规范

### 🚀 进阶文档
- [设计原理](docs/zh/advanced/design-principles.md) - 提示工程的核心原理
- [性能优化](docs/zh/advanced/performance.md) - 优化技巧和最佳实践
- [问题排查](docs/zh/advanced/troubleshooting.md) - 常见问题和解决方案
- [常见问题](docs/zh/advanced/faq.md) - FAQ

### 🔄 版本文档
- [版本对比](docs/zh/versions/comparison.md) - 三个版本的特性对比
- [Anthropic 1P](docs/zh/versions/anthropic-1p.md) - Anthropic 官方 API 版本
- [Bedrock Anthropic SDK](docs/zh/versions/bedrock-anthropic.md) - AWS Bedrock Anthropic SDK 版本
- [Bedrock Boto3](docs/zh/versions/bedrock-boto3.md) - AWS Bedrock Boto3 版本

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
