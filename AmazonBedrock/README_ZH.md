# 欢迎使用 Anthropic 提示工程交互式教程 - Bedrock 版本

🟧 **版本标识**：Amazon Bedrock 版本

## 课程简介和目标

本课程旨在为您提供全面的分步指导，帮助您在 Amazon Bedrock 平台上使用 Claude 进行最佳提示工程。

**完成本课程后，您将能够**：
- 掌握良好提示的基本结构
- 识别常见的失败模式并学习"二八法则"技术来解决它们
- 理解 Claude 的优势和局限性
- 从零开始为常见用例构建强大的提示

## 版本说明

本目录包含两个 Amazon Bedrock 实现版本：

### 📁 anthropic/ - Bedrock Anthropic SDK 版本
使用 Anthropic SDK 的 Bedrock 适配器访问 Claude 模型。

**特点**：
- 保持与 Anthropic SDK 相似的 API 接口
- 易于从 Anthropic 1P 版本迁移
- 集成 AWS 生态系统

**适用场景**：
- 从 Anthropic 1P 迁移到 AWS
- 需要熟悉的 Anthropic API 风格
- 希望简化的集成体验

**详细文档**：[Bedrock Anthropic SDK 版本文档](../docs/zh/versions/bedrock-anthropic.md)

### 📁 boto3/ - Bedrock Boto3 版本
使用 AWS 原生 Boto3 SDK 通过 Amazon Bedrock 访问 Claude 模型。

**特点**：
- 完全的 AWS 原生体验
- 更底层的 API 控制
- 与其他 AWS 服务无缝集成

**适用场景**：
- 深度集成 AWS 服务
- 已经使用 Boto3 管理 AWS 资源
- 需要细粒度控制

**详细文档**：[Bedrock Boto3 版本文档](../docs/zh/versions/bedrock-boto3.md)

## 快速开始

### 前置条件

1. **AWS 账户**
   - 有效的 AWS 账户
   - 启用 Amazon Bedrock 服务
   - 请求并获得 Claude 模型访问权限

2. **AWS 凭证配置**
   ```bash
   aws configure
   ```

3. **Python 环境**
   - Python 3.7 或更高版本
   - Jupyter Notebook

### 安装步骤

#### 1. 克隆仓库
```bash
git clone https://github.com/anthropics/prompt-eng-interactive-tutorial.git
cd prompt-eng-interactive-tutorial/AmazonBedrock
```

#### 2. 选择版本

**选择 Anthropic SDK 版本**：
```bash
cd anthropic
```

**选择 Boto3 版本**：
```bash
cd boto3
```

#### 3. 安装依赖
```bash
pip install -U pip
pip install -r ../requirements.txt
```

#### 4. 启动 Jupyter Notebook
```bash
jupyter notebook
```

#### 5. 开始学习
打开 `00_Tutorial_How-To.ipynb` 开始您的学习之旅！

## 课程结构和内容

本课程为您提供了许多练习编写和调试提示的机会。课程分为 **9 个章节及配套练习**，以及包含更多高级方法的附录。建议您**按章节顺序学习**。

**每节课底部都有"示例练习场"区域**，您可以自由实验课程中的示例，亲自观察更改提示如何改变 Claude 的响应。

注意：本教程使用我们最小、最快、最经济的模型 Claude 3 Haiku。Anthropic 还有[两个其他模型](https://docs.anthropic.com/claude/docs/models-overview)：Claude 3 Sonnet 和 Claude 3 Opus，它们比 Haiku 更智能，其中 Opus 是最智能的。

准备好后，请前往 `01_Basic_Prompt_Structure` 开始学习。

## 目录

每章包含一节课和一组练习。

### 初级
- **第 1 章**：基本提示结构

- **第 2 章**：清晰直接的表达

- **第 3 章**：角色分配

### 中级
- **第 4 章**：分离数据和指令

- **第 5 章**：格式化输出与为 Claude 代言

- **第 6 章**：预知（逐步思考）

- **第 7 章**：使用示例

### 高级
- **第 8 章**：避免幻觉

- **第 9 章**：构建复杂提示（行业用例）
  - 从零开始构建复杂提示 - 聊天机器人
  - 法律服务的复杂提示
  - **练习**：金融服务的复杂提示
  - **练习**：编程的复杂提示
  - 恭喜与下一步

- **附录**：超越标准提示
  - 提示链接
  - 工具使用
  - 实证性能评估
  - 搜索与检索

## 版本对比

不确定选择哪个版本？查看我们的[版本对比文档](../docs/zh/versions/comparison.md)了解详细对比和选择建议。

### 快速对比

| 特性 | Anthropic SDK | Boto3 |
|------|--------------|-------|
| **API 风格** | Anthropic 风格 | AWS 原生 |
| **学习曲线** | 中等 | 中等 |
| **迁移难度** | 从 1P 迁移简单 | 需要重写代码 |
| **AWS 集成** | 完整 | 完整 |
| **控制粒度** | 高级 API | 底层 API |

## 相关资源

### 官方文档
- [Amazon Bedrock 文档](https://docs.aws.amazon.com/bedrock/)
- [Anthropic API 文档](https://docs.anthropic.com/)
- [Claude on Bedrock](https://docs.anthropic.com/claude/reference/claude-on-amazon-bedrock)

### 项目文档
- [中文主文档](../README.md)
- [安装指南](../docs/zh/getting-started/installation.md)
- [快速开始](../docs/zh/getting-started/quickstart.md)
- [完整使用手册](../docs/zh/user-guide/user-guide.md)
- [版本对比](../docs/zh/versions/comparison.md)

### AWS 资源
- [AWS CLI 配置](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)
- [IAM 权限管理](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [Boto3 文档](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

## 常见问题

### Q: 两个 Bedrock 版本有什么区别？

A: Anthropic SDK 版本使用 Anthropic 的 SDK 接口，API 风格与 Anthropic 1P 相似，易于迁移。Boto3 版本使用 AWS 原生 SDK，提供更底层的控制，适合深度 AWS 集成。

### Q: 我应该选择哪个版本？

A: 如果您从 Anthropic 1P 迁移或希望保持熟悉的 API 风格，选择 Anthropic SDK 版本。如果您已经使用 Boto3 或需要更细粒度的控制，选择 Boto3 版本。

### Q: 两个版本的教程内容相同吗？

A: 是的，两个版本包含完全相同的提示工程教程内容。唯一的区别在于技术实现和 API 调用方式。

### Q: 如何获取 Bedrock 访问权限？

A: 登录 AWS 控制台，搜索 Amazon Bedrock 服务，在支持的区域启用服务，然后请求访问 Claude 模型。访问请求通常在几分钟内获得批准。

### Q: 需要支付额外费用吗？

A: 使用 Amazon Bedrock 会按 AWS Bedrock 定价计费。具体定价请查看 [AWS Bedrock 定价页面](https://aws.amazon.com/bedrock/pricing/)。

## 获取帮助

如果您在使用过程中遇到问题：

1. **查看文档**：
   - [Bedrock Anthropic SDK 版本文档](../docs/zh/versions/bedrock-anthropic.md)
   - [Bedrock Boto3 版本文档](../docs/zh/versions/bedrock-boto3.md)
   - [故障排除指南](../docs/zh/advanced/troubleshooting.md)
   - [常见问题](../docs/zh/advanced/faq.md)

2. **AWS 支持**：
   - [AWS Support Center](https://console.aws.amazon.com/support/)
   - [AWS 论坛](https://forums.aws.amazon.com/)

3. **社区资源**：
   - [Anthropic Discord](https://discord.gg/anthropic)
   - [GitHub Issues](https://github.com/anthropics/anthropic-sdk-python/issues)

## 贡献

欢迎贡献！请查看我们的[贡献指南](../docs/zh/development/contributing.md)了解如何参与项目。

## 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

---

**准备好开始了吗？** 选择您的版本并打开 `00_Tutorial_How-To.ipynb` 开始学习！

如需更多信息，请访问[项目主页](../README.md)或查看[完整文档](../docs/zh/README.md)。
