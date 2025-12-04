# 安装指南

## 目录

- [概述](#概述)
- [目标读者](#目标读者)
- [前置条件](#前置条件)
- [安装步骤](#安装步骤)
- [针对不同操作系统的说明](#针对不同操作系统的说明)
- [验证安装](#验证安装)
- [常见安装问题与解决方案](#常见安装问题与解决方案)
- [环境配置最佳实践](#环境配置最佳实践)
- [升级和更新](#升级和更新)
- [卸载](#卸载)
- [下一步](#下一步)
- [另请参阅](#另请参阅)
- [获取帮助](#获取帮助)

---

## 概述

本指南将帮助您在本地环境中安装和配置 Anthropic Claude 提示工程交互式教程。我们提供了针对不同操作系统和不同版本的详细安装说明。

> **版本说明**：本教程提供三个版本（🟦 Anthropic 1P、🟧 Bedrock Anthropic SDK、🟨 Bedrock Boto3）。本指南涵盖所有版本的通用安装步骤。版本特定的配置请参考：
> - [Anthropic 1P 版本文档](../versions/anthropic-1p.md)
> - [Bedrock Anthropic SDK 版本文档](../versions/bedrock-anthropic.md)
> - [Bedrock Boto3 版本文档](../versions/bedrock-boto3.md)

## 目标读者

本指南适用于：
- 希望在本地运行教程的开发者
- 需要配置开发环境的学习者
- 准备为项目做贡献的贡献者

## 前置条件

在开始安装之前，请确保您的系统满足以下要求：

### 必需软件

1. **Python 3.7 或更高版本**
   - 推荐使用 Python 3.8 或更高版本
   - 检查 Python 版本：`python --version` 或 `python3 --version`

2. **pip（Python 包管理器）**
   - 通常随 Python 一起安装
   - 检查 pip 版本：`pip --version` 或 `pip3 --version`

3. **Jupyter Notebook 或 JupyterLab**
   - 用于运行交互式教程
   - 将在安装步骤中安装

4. **Git**（可选，用于克隆仓库）
   - 检查 Git 版本：`git --version`

### API 密钥或 AWS 账户

根据您选择的版本，您需要：

- **Anthropic 1P 版本**：Anthropic API 密钥
  - 在 [Anthropic Console](https://console.anthropic.com/) 注册并获取
  
- **Amazon Bedrock 版本**：AWS 账户和相应权限
  - 需要访问 Amazon Bedrock 服务的权限
  - 配置 AWS CLI 凭证

## 安装步骤

### 方法 1：使用 Anthropic 1P 版本（推荐新手）

这是最简单的安装方法，适合想要快速开始的用户。

#### 步骤 1：克隆仓库

```bash
# 使用 Git 克隆
git clone <repository-url>
cd <repository-name>

# 或者下载 ZIP 文件并解压
```

#### 步骤 2：创建虚拟环境（推荐）

使用虚拟环境可以避免依赖冲突：

**macOS/Linux:**
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate
```

**Windows:**
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate
```

#### 步骤 3：安装依赖

```bash
# 安装 Anthropic SDK
pip install anthropic

# 安装 Jupyter Notebook
pip install jupyter

# 或者安装 JupyterLab（更现代的界面）
pip install jupyterlab
```

#### 步骤 4：配置 API 密钥

1. 访问 [Anthropic Console](https://console.anthropic.com/) 获取 API 密钥
2. 打开 `Anthropic 1P/00_Tutorial_How-To.ipynb`
3. 在相应的代码单元格中设置您的 API 密钥：

```python
API_KEY = "your_api_key_here"  # 替换为您的实际 API 密钥
MODEL_NAME = "claude-3-haiku-20240307"
```

#### 步骤 5：启动 Jupyter Notebook

```bash
# 启动 Jupyter Notebook
jupyter notebook

# 或启动 JupyterLab
jupyter lab
```

浏览器将自动打开，导航到 `Anthropic 1P` 目录开始学习。

### 方法 2：使用 Amazon Bedrock (Anthropic SDK) 版本

适合已有 AWS 账户并希望使用 Bedrock 服务的用户。

#### 步骤 1：克隆仓库

```bash
git clone <repository-url>
cd <repository-name>
```

#### 步骤 2：创建虚拟环境

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### 步骤 3：安装依赖

```bash
# 进入 AmazonBedrock 目录
cd AmazonBedrock

# 安装所有依赖
pip install -r requirements.txt

# 或手动安装
pip install anthropic boto3 awscli jupyter
```

#### 步骤 4：配置 AWS 凭证

**方法 A：使用 AWS CLI 配置**

```bash
# 配置 AWS CLI
aws configure

# 输入以下信息：
# AWS Access Key ID: [您的访问密钥]
# AWS Secret Access Key: [您的密钥]
# Default region name: us-east-1  # 或其他支持 Bedrock 的区域
# Default output format: json
```

**方法 B：使用环境变量**

```bash
# macOS/Linux
export AWS_ACCESS_KEY_ID="your_access_key"
export AWS_SECRET_ACCESS_KEY="your_secret_key"
export AWS_DEFAULT_REGION="us-east-1"

# Windows (PowerShell)
$env:AWS_ACCESS_KEY_ID="your_access_key"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key"
$env:AWS_DEFAULT_REGION="us-east-1"
```

#### 步骤 5：验证 Bedrock 访问权限

```bash
# 列出可用的 Bedrock 模型
aws bedrock list-foundation-models --region us-east-1
```

#### 步骤 6：启动 Jupyter Notebook

```bash
jupyter notebook
# 或
jupyter lab
```

导航到 `AmazonBedrock/anthropic` 目录开始学习。

### 方法 3：使用 Amazon Bedrock (Boto3) 版本

适合需要更底层 AWS SDK 控制的高级用户。

安装步骤与方法 2 相同，但使用 `AmazonBedrock/boto3` 目录中的 Notebook。

## 针对不同操作系统的说明

### macOS

#### 安装 Python

```bash
# 使用 Homebrew 安装 Python
brew install python3

# 验证安装
python3 --version
```

#### 常见问题

- 如果遇到 SSL 证书错误，运行：
  ```bash
  /Applications/Python\ 3.x/Install\ Certificates.command
  ```

### Linux (Ubuntu/Debian)

#### 安装 Python 和依赖

```bash
# 更新包列表
sudo apt update

# 安装 Python 3 和 pip
sudo apt install python3 python3-pip python3-venv

# 安装 Jupyter 依赖
sudo apt install python3-dev build-essential
```

### Windows

#### 安装 Python

1. 从 [python.org](https://www.python.org/downloads/) 下载 Python 安装程序
2. 运行安装程序，**确保勾选 "Add Python to PATH"**
3. 验证安装：打开命令提示符，运行 `python --version`

#### 使用 PowerShell

推荐使用 PowerShell 而不是命令提示符，以获得更好的体验。

## 验证安装

安装完成后，运行以下命令验证所有组件是否正确安装：

```bash
# 检查 Python 版本
python --version  # 或 python3 --version

# 检查 pip 版本
pip --version  # 或 pip3 --version

# 检查 Jupyter 安装
jupyter --version

# 检查 Anthropic SDK（Anthropic 1P 版本）
python -c "import anthropic; print(anthropic.__version__)"

# 检查 Boto3（Bedrock 版本）
python -c "import boto3; print(boto3.__version__)"
```

## 常见安装问题与解决方案

### 问题 1：找不到 Python 命令

**症状**：
```
'python' is not recognized as an internal or external command
```

**解决方案**：
- **Windows**：重新安装 Python，确保勾选 "Add Python to PATH"
- **macOS/Linux**：使用 `python3` 而不是 `python`
- 或者手动添加 Python 到系统 PATH

### 问题 2：pip 安装失败

**症状**：
```
ERROR: Could not install packages due to an EnvironmentError
```

**解决方案**：
```bash
# 使用 --user 标志安装到用户目录
pip install --user anthropic jupyter

# 或者升级 pip
pip install --upgrade pip
```

### 问题 3：权限错误

**症状**：
```
Permission denied
```

**解决方案**：
```bash
# macOS/Linux：使用虚拟环境（推荐）
python3 -m venv venv
source venv/bin/activate

# 或使用 --user 标志
pip install --user <package-name>

# 避免使用 sudo pip（不推荐）
```

### 问题 4：Jupyter Notebook 无法启动

**症状**：
```
jupyter: command not found
```

**解决方案**：
```bash
# 确保 Jupyter 已安装
pip install jupyter

# 检查 PATH 设置
# macOS/Linux
export PATH="$HOME/.local/bin:$PATH"

# Windows：将 Python Scripts 目录添加到 PATH
# 通常位于：C:\Users\<用户名>\AppData\Local\Programs\Python\Python3x\Scripts
```

### 问题 5：AWS 凭证配置错误

**症状**：
```
botocore.exceptions.NoCredentialsError: Unable to locate credentials
```

**解决方案**：
```bash
# 重新配置 AWS CLI
aws configure

# 或检查凭证文件
# macOS/Linux: ~/.aws/credentials
# Windows: C:\Users\<用户名>\.aws\credentials

# 验证凭证
aws sts get-caller-identity
```

### 问题 6：Bedrock 区域不可用

**症状**：
```
An error occurred (AccessDeniedException) when calling the ListFoundationModels operation
```

**解决方案**：
- 确保使用支持 Bedrock 的 AWS 区域（如 us-east-1, us-west-2）
- 检查您的 AWS 账户是否有 Bedrock 访问权限
- 在 AWS Console 中请求 Bedrock 模型访问权限

### 问题 7：依赖版本冲突

**症状**：
```
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed
```

**解决方案**：
```bash
# 使用虚拟环境（强烈推荐）
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 重新安装依赖
pip install -r requirements.txt
```

### 问题 8：SSL 证书错误

**症状**：
```
SSL: CERTIFICATE_VERIFY_FAILED
```

**解决方案**：
```bash
# macOS
/Applications/Python\ 3.x/Install\ Certificates.command

# 或安装 certifi
pip install --upgrade certifi

# Linux
sudo apt-get install ca-certificates
```

## 环境配置最佳实践

### 1. 使用虚拟环境

始终使用虚拟环境来隔离项目依赖：

```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# 退出虚拟环境
deactivate
```

### 2. 管理依赖版本

创建 `requirements.txt` 文件记录依赖：

```bash
# 导出当前环境的依赖
pip freeze > requirements.txt

# 从文件安装依赖
pip install -r requirements.txt
```

### 3. 保护 API 密钥

**不要**将 API 密钥硬编码在代码中或提交到版本控制系统。

推荐方法：

**方法 A：使用环境变量**

```bash
# macOS/Linux
export ANTHROPIC_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="your_api_key_here"

# 在代码中读取
import os
API_KEY = os.environ.get("ANTHROPIC_API_KEY")
```

**方法 B：使用 .env 文件**

```bash
# 安装 python-dotenv
pip install python-dotenv

# 创建 .env 文件（添加到 .gitignore）
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env

# 在代码中加载
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("ANTHROPIC_API_KEY")
```

### 4. 配置 Jupyter Notebook

优化 Jupyter Notebook 体验：

```bash
# 安装有用的扩展
pip install jupyter_contrib_nbextensions
jupyter contrib nbextension install --user

# 启用代码折叠、目录等功能
jupyter nbextension enable codefolding/main
jupyter nbextension enable toc2/main
```

## 升级和更新

### 更新依赖包

```bash
# 更新单个包
pip install --upgrade anthropic

# 更新所有包
pip list --outdated
pip install --upgrade <package-name>
```

### 更新教程内容

```bash
# 拉取最新代码
git pull origin main

# 如果有新的依赖，重新安装
pip install -r requirements.txt
```

## 卸载

如果需要完全卸载：

```bash
# 退出虚拟环境
deactivate

# 删除虚拟环境目录
rm -rf venv  # macOS/Linux
rmdir /s venv  # Windows

# 删除项目目录
cd ..
rm -rf <repository-name>
```

## 下一步

安装完成后，请继续阅读：
- [快速开始指南](quickstart.md) - 5 分钟快速上手教程
- [配置说明](../user-guide/configuration.md) - 详细的配置选项
- [版本对比](../versions/comparison.md) - 选择适合您的版本

## 另请参阅

**相关文档**：
- [快速开始](quickstart.md) - 完成安装后的下一步
- [配置说明](../user-guide/configuration.md) - 高级配置选项
- [问题排查](../advanced/troubleshooting.md) - 解决安装问题
- [版本对比](../versions/comparison.md) - 了解不同版本

**外部资源**：
- [Python 官方文档](https://docs.python.org/)
- [Jupyter 文档](https://jupyter.org/documentation)
- [Anthropic API 文档](https://docs.anthropic.com/)
- [AWS Bedrock 文档](https://docs.aws.amazon.com/bedrock/)
- [AWS CLI 配置指南](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html)

## 获取帮助

如果遇到本指南未涵盖的问题：
1. 查看[问题排查文档](../advanced/troubleshooting.md)
2. 查看[常见问题](../advanced/faq.md)
3. 在项目仓库提交 Issue
4. 查阅相关官方文档

---

**文档导航**：
- **上一步**: [主页](../../README.md)
- **下一步**: [快速开始](quickstart.md)
- **相关主题**: [配置说明](../user-guide/configuration.md) | [问题排查](../advanced/troubleshooting.md)
