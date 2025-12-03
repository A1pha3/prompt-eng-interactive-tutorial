# 开发指南

## 目录

- [概述](#概述)
- [开发环境要求](#开发环境要求)
- [环境搭建](#环境搭建)
- [项目结构](#项目结构)
- [运行和调试](#运行和调试)
- [开发工具推荐](#开发工具推荐)
- [常见开发任务](#常见开发任务)
- [故障排查](#故障排查)
- [相关资源](#相关资源)

## 概述

本文档为开发者提供详细的开发环境搭建指南，帮助您快速开始为 Anthropic Claude 提示工程交互式教程项目做贡献。

### 适用人群

- 希望为项目贡献代码的开发者
- 需要在本地运行和测试项目的贡献者
- 想要基于本项目创建自定义教程的开发者

### 前置知识

- Python 编程基础
- Git 版本控制基础
- Jupyter Notebook 使用经验
- 基本的命令行操作

## 开发环境要求

### 系统要求

- **操作系统**：Windows 10+、macOS 10.14+、Linux（Ubuntu 18.04+ 或同等版本）
- **Python 版本**：Python 3.7 或更高版本（推荐 3.9+）
- **内存**：至少 4GB RAM（推荐 8GB+）
- **磁盘空间**：至少 500MB 可用空间

### 必需软件

1. **Python 3.7+**
   - 下载地址：https://www.python.org/downloads/
   - 验证安装：`python --version` 或 `python3 --version`

2. **pip**（Python 包管理器）
   - 通常随 Python 一起安装
   - 验证安装：`pip --version` 或 `pip3 --version`

3. **Git**
   - 下载地址：https://git-scm.com/downloads
   - 验证安装：`git --version`

4. **Jupyter Notebook 或 JupyterLab**
   - 将在环境搭建步骤中安装

### 可选软件

- **虚拟环境管理工具**：`venv`（Python 内置）、`conda`、`virtualenv`
- **代码编辑器**：VS Code、PyCharm、Sublime Text
- **终端工具**：iTerm2（macOS）、Windows Terminal（Windows）

## 环境搭建

### 1. 克隆仓库

```bash
# 克隆项目仓库
git clone https://github.com/anthropics/prompt-eng-interactive-tutorial.git

# 进入项目目录
cd prompt-eng-interactive-tutorial
```

### 2. 创建虚拟环境（推荐）

使用虚拟环境可以隔离项目依赖，避免与系统 Python 包冲突。

#### 使用 venv（Python 内置）

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

#### 使用 conda

```bash
# 创建虚拟环境
conda create -n prompt-tutorial python=3.9

# 激活虚拟环境
conda activate prompt-tutorial
```

### 3. 安装依赖

根据您要使用的版本安装相应的依赖。

#### Anthropic 1P 版本

```bash
# 安装核心依赖
pip install anthropic jupyter

# 或从 requirements 文件安装（如果有）
pip install -r requirements.txt
```

#### Amazon Bedrock 版本

```bash
# 进入 Bedrock 目录
cd AmazonBedrock

# 安装依赖
pip install -r requirements.txt

# 返回项目根目录
cd ..
```

依赖包说明：
- `anthropic`：Anthropic Python SDK
- `boto3`：AWS Python SDK
- `jupyter`：Jupyter Notebook 环境
- `awscli`：AWS 命令行工具（Bedrock 版本需要）

### 4. 配置 API 凭证

#### Anthropic 1P 版本

```bash
# 设置环境变量
export ANTHROPIC_API_KEY="your-api-key-here"

# 或在 ~/.bashrc 或 ~/.zshrc 中添加
echo 'export ANTHROPIC_API_KEY="your-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

获取 API 密钥：
1. 访问 https://console.anthropic.com/
2. 登录或注册账户
3. 在 API Keys 页面生成新密钥

#### AWS Bedrock 版本

```bash
# 配置 AWS 凭证
aws configure

# 按提示输入：
# AWS Access Key ID: your-access-key
# AWS Secret Access Key: your-secret-key
# Default region name: us-east-1
# Default output format: json
```

或手动创建配置文件：

```bash
# ~/.aws/credentials
[default]
aws_access_key_id = your-access-key
aws_secret_access_key = your-secret-key

# ~/.aws/config
[default]
region = us-east-1
output = json
```

### 5. 验证安装

创建测试脚本验证环境配置：

```python
# test_setup.py
import sys

print(f"Python 版本: {sys.version}")

try:
    import anthropic
    print(f"✓ Anthropic SDK 已安装: {anthropic.__version__}")
except ImportError:
    print("✗ Anthropic SDK 未安装")

try:
    import boto3
    print(f"✓ Boto3 已安装: {boto3.__version__}")
except ImportError:
    print("✗ Boto3 未安装")

try:
    import jupyter
    print("✓ Jupyter 已安装")
except ImportError:
    print("✗ Jupyter 未安装")

print("\n环境配置完成！")
```

运行测试：
```bash
python test_setup.py
```


## 项目结构

```
prompt-eng-interactive-tutorial/
├── README.md                          # 项目主页（中文）
├── README_EN.md                       # 项目主页（英文）
├── LICENSE                            # 许可证
├── .gitignore                         # Git 忽略文件
│
├── Anthropic 1P/                      # Anthropic 1P 版本
│   ├── 00_Tutorial_How-To.ipynb      # 教程使用说明
│   ├── 01_Basic_Prompt_Structure.ipynb
│   ├── 02_Being_Clear_and_Direct.ipynb
│   ├── ...                            # 其他章节
│   └── hints.py                       # 练习提示工具
│
├── AmazonBedrock/                     # Bedrock 版本
│   ├── README.md                      # Bedrock 版本说明
│   ├── CONTRIBUTING.md                # 贡献指南
│   ├── requirements.txt               # Python 依赖
│   ├── anthropic/                     # Anthropic SDK 版本
│   │   ├── 00_Tutorial_How-To.ipynb
│   │   ├── 01_Basic_Prompt_Structure.ipynb
│   │   └── ...
│   ├── boto3/                         # Boto3 版本
│   │   ├── 00_Tutorial_How-To.ipynb
│   │   ├── 01_Basic_Prompt_Structure.ipynb
│   │   └── ...
│   ├── utils/                         # 工具模块
│   │   ├── __init__.py
│   │   └── hints.py
│   └── cloudformation/                # AWS CloudFormation 模板
│       └── workshop-v1-final-cfn.yml
│
└── docs/                              # 文档目录
    └── zh/                            # 中文文档
        ├── getting-started/           # 入门文档
        ├── user-guide/                # 使用文档
        ├── development/               # 开发文档
        ├── advanced/                  # 进阶文档
        ├── versions/                  # 版本文档
        ├── templates/                 # 文档模板
        └── glossary.md                # 术语表
```

### 核心目录说明

- **Anthropic 1P/**：使用 Anthropic 官方 API 的教程版本
- **AmazonBedrock/**：使用 AWS Bedrock 的教程版本
  - `anthropic/`：使用 Anthropic SDK 访问 Bedrock
  - `boto3/`：使用 Boto3 SDK 访问 Bedrock
- **docs/zh/**：中文文档体系
- **utils/**：辅助工具和函数

## 运行和调试

### 启动 Jupyter Notebook

#### 方法 1：使用 Jupyter Notebook

```bash
# 在项目根目录启动
jupyter notebook

# 或指定端口
jupyter notebook --port 8888

# 或指定 IP（允许远程访问）
jupyter notebook --ip 0.0.0.0
```

浏览器会自动打开 `http://localhost:8888`

#### 方法 2：使用 JupyterLab（推荐）

```bash
# 安装 JupyterLab
pip install jupyterlab

# 启动 JupyterLab
jupyter lab
```

JupyterLab 提供更现代的界面和更多功能。

### 运行特定 Notebook

1. 在 Jupyter 界面中导航到相应目录
2. 点击要运行的 `.ipynb` 文件
3. 使用 `Shift + Enter` 逐个运行单元格
4. 或使用菜单 `Cell > Run All` 运行所有单元格

### 调试技巧

#### 1. 使用 print 调试

```python
# 在 Notebook 单元格中
prompt = "Hello, Claude"
print(f"发送的提示词: {prompt}")

response = client.messages.create(...)
print(f"响应内容: {response.content}")
```

#### 2. 使用 IPython 魔法命令

```python
# 查看变量内容
%whos

# 测量执行时间
%%time
response = client.messages.create(...)

# 调试模式
%debug
```

#### 3. 使用 Python 调试器

```python
# 在需要调试的地方插入断点
import pdb; pdb.set_trace()

# 或使用 IPython 调试器
from IPython.core.debugger import set_trace
set_trace()
```

#### 4. 查看 API 请求详情

```python
# 启用详细日志
import logging
logging.basicConfig(level=logging.DEBUG)

# 查看完整的请求和响应
import json
print(json.dumps(response.model_dump(), indent=2))
```

### 常见运行问题

#### 问题 1：API 密钥未设置

**错误信息**：
```
AuthenticationError: API key not found
```

**解决方案**：
```bash
# 检查环境变量
echo $ANTHROPIC_API_KEY

# 如果为空，设置环境变量
export ANTHROPIC_API_KEY="your-api-key"

# 重启 Jupyter Notebook
```

#### 问题 2：模块导入失败

**错误信息**：
```
ModuleNotFoundError: No module named 'anthropic'
```

**解决方案**：
```bash
# 确认虚拟环境已激活
which python

# 重新安装依赖
pip install anthropic

# 重启 Jupyter 内核
```

#### 问题 3：AWS 凭证错误

**错误信息**：
```
NoCredentialsError: Unable to locate credentials
```

**解决方案**：
```bash
# 配置 AWS 凭证
aws configure

# 或检查凭证文件
cat ~/.aws/credentials
```

## 开发工具推荐

### 1. 代码编辑器

#### Visual Studio Code（推荐）

**优点**：
- 优秀的 Jupyter Notebook 支持
- 丰富的 Python 扩展
- 集成终端和 Git

**推荐扩展**：
- Python（Microsoft）
- Jupyter（Microsoft）
- Pylance（类型检查）
- GitLens（Git 增强）
- Markdown All in One

**配置**：
```json
// .vscode/settings.json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "jupyter.askForKernelRestart": false
}
```

#### PyCharm

**优点**：
- 强大的 Python IDE
- 内置 Jupyter 支持
- 智能代码补全

**适用场景**：大型项目开发

### 2. 终端工具

- **iTerm2**（macOS）：功能丰富的终端模拟器
- **Windows Terminal**（Windows）：现代化的 Windows 终端
- **Tmux**：终端复用器，适合远程开发

### 3. Git 工具

- **Git CLI**：命令行工具（推荐）
- **GitHub Desktop**：图形化界面
- **GitKraken**：可视化 Git 客户端

### 4. API 测试工具

- **Postman**：API 测试和调试
- **curl**：命令行 HTTP 客户端
- **httpie**：用户友好的 HTTP 客户端

### 5. Python 工具

#### 代码格式化

```bash
# Black - 代码格式化
pip install black
black your_file.py

# isort - 导入排序
pip install isort
isort your_file.py
```

#### 代码检查

```bash
# Pylint - 代码质量检查
pip install pylint
pylint your_file.py

# Flake8 - 风格检查
pip install flake8
flake8 your_file.py
```

#### 类型检查

```bash
# mypy - 静态类型检查
pip install mypy
mypy your_file.py
```

## 常见开发任务

### 1. 创建新章节

```bash
# 1. 复制现有章节作为模板
cp "01_Basic_Prompt_Structure.ipynb" "10_New_Chapter.ipynb"

# 2. 在 Jupyter 中打开并编辑
jupyter notebook "10_New_Chapter.ipynb"

# 3. 更新章节内容
# - 修改标题和学习目标
# - 添加新的示例和练习
# - 测试所有代码单元格

# 4. 更新 README.md 目录
```

### 2. 添加辅助函数

```python
# utils/helpers.py
def format_prompt(template: str, **kwargs) -> str:
    """格式化提示词模板
    
    Args:
        template: 提示词模板字符串
        **kwargs: 模板变量
        
    Returns:
        格式化后的提示词
    """
    return template.format(**kwargs)

def validate_response(response, expected_keywords: list) -> bool:
    """验证响应是否包含预期关键词
    
    Args:
        response: API 响应对象
        expected_keywords: 预期关键词列表
        
    Returns:
        是否通过验证
    """
    content = response.content[0].text.lower()
    return all(keyword.lower() in content for keyword in expected_keywords)
```

### 3. 运行测试

```bash
# 如果项目有测试套件
pytest tests/

# 运行特定测试
pytest tests/test_helpers.py

# 查看覆盖率
pytest --cov=utils tests/
```

### 4. 更新文档

```bash
# 编辑文档
vim docs/zh/user-guide/user-guide.md

# 预览 Markdown（使用 VS Code 或其他工具）
# 或使用 grip 在浏览器中预览
pip install grip
grip docs/zh/user-guide/user-guide.md
```

### 5. 提交代码

```bash
# 查看修改
git status
git diff

# 添加文件
git add .

# 提交（遵循提交规范）
git commit -m "feat: 添加新章节 - 高级提示技巧"

# 推送到远程
git push origin feature/advanced-prompting
```

## 故障排查

### Jupyter Notebook 问题

#### Kernel 无法启动

```bash
# 重新安装 ipykernel
pip install --upgrade ipykernel

# 注册内核
python -m ipykernel install --user --name=prompt-tutorial
```

#### 无法导入模块

```bash
# 确认内核使用正确的 Python
import sys
print(sys.executable)

# 在 Notebook 中安装包
!pip install anthropic
```

### API 调用问题

#### 请求超时

```python
# 增加超时时间
client = Anthropic(
    api_key="your-key",
    timeout=60.0  # 60 秒
)
```

#### 速率限制

```python
import time

def call_with_retry(func, max_retries=3):
    """带重试的 API 调用"""
    for i in range(max_retries):
        try:
            return func()
        except Exception as e:
            if "rate_limit" in str(e).lower():
                wait_time = 2 ** i  # 指数退避
                print(f"速率限制，等待 {wait_time} 秒...")
                time.sleep(wait_time)
            else:
                raise
    raise Exception("达到最大重试次数")
```

### 性能问题

#### Notebook 运行缓慢

- 重启内核：`Kernel > Restart`
- 清理输出：`Cell > All Output > Clear`
- 关闭不需要的 Notebook
- 检查内存使用：`!free -h`（Linux）或 `!vm_stat`（macOS）

## 相关资源

### 官方文档

- [Anthropic API 文档](https://docs.anthropic.com/)
- [AWS Bedrock 文档](https://docs.aws.amazon.com/bedrock/)
- [Jupyter 文档](https://jupyter.org/documentation)
- [Python 官方文档](https://docs.python.org/3/)

### 开发指南

- [架构设计](architecture.md) - 了解项目架构
- [贡献指南](contributing.md) - 了解贡献流程
- [代码规范](code-style.md) - 了解代码风格
- [开发术语表](glossary-dev.md) - 开发相关术语中英文对照
- [完整术语表](../glossary.md) - 项目完整术语表

### 学习资源

- [Python 最佳实践](https://docs.python-guide.org/)
- [Jupyter Notebook 技巧](https://jupyter-notebook.readthedocs.io/)
- [Git 教程](https://git-scm.com/book/zh/v2)

### 获取帮助

- **GitHub Issues**：报告 bug 或提出功能请求
- **讨论区**：技术讨论和问答
- **文档**：查看[常见问题](../advanced/faq.md)

---

**最后更新**：2024-12-02  
**维护者**：项目团队

**下一步**：
- 阅读[贡献指南](contributing.md)了解如何提交代码
- 查看[代码规范](code-style.md)了解编码标准
- 浏览[架构设计](architecture.md)了解系统设计
