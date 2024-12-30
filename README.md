# 私人研究助手 (Private Research Assistant)

[English](README_EN.md) | 简体中文

**注意**：这是一个粗糙的实现，没有任何优化。由[Cursor AI](https://www.cursor.com/)助力开发。

这是一个基于 LLM 的研究论文分析工具，能够自动解析学术论文并生成结构化的分析报告。

## 功能特点

- PDF论文自动解析
- 基于LLM的智能分析
- 结构化输出
- 自定义模板支持
- 多种LLM模型支持（目前支持DeepSeek）

## 安装

1. 克隆仓库
```bash
git clone [repository-url]
cd privateRA
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 配置
创建 `config.yaml` 文件并配置你的API密钥：
```yaml
llm:
  type: "deepseek"  # LLM类型
  api_key: "your-api-key"  # API密钥
  base_url: "https://api.deepseek.com/v1"  # API基础URL
```
关于DeepSeek的API密钥，请参考[DeepSeek API文档](https://api-docs.deepseek.com/zh-cn/)。


## 使用方法

### 命令行使用
最简单的使用方式是通过命令行：

```bash
python -m src.main \
    --config path/to/config.yaml \
    --template path/to/template.md \
    --pdf path/to/document.pdf \
    --output path/to/output.md
```

或使用简写形式：

```bash
python -m src.main \
    -c path/to/config.yaml \
    -t path/to/template.md \
    -p path/to/document.pdf \
    -o path/to/output.md
```

参数说明：
- `--config` 或 `-c`: 配置文件路径，包含 LLM API 配置信息
- `--template` 或 `-t`: Markdown 模板文件路径
- `--pdf` 或 `-p`: 要分析的 PDF 文件路径
- `--output` 或 `-o`: 输出文件路径

### 代码中使用
你也可以在代码中直接使用相关组件：

```python
from src.pdf_parser.pdf_parser import PDFParser
from src.llm_interface.llm_factory import LLMFactory
from src.utils.output_parser import OutputParser

# 初始化组件
llm = LLMFactory.create_llm_from_config("config.yaml")
output_parser = OutputParser("templates/default.md")
pdf_parser = PDFParser("your-paper.pdf")

# 解析PDF
documents = pdf_parser.parse()

# 生成分析报告
response = llm.chat(system_prompt=system_prompt, user_prompt=prompt)
result = output_parser.parse(response)
output_parser.save(result, "output.md")
```

## Markdown模板字段说明

在模板中，你可以使用以下字段（使用 `{field_name}` 语法）：

1. `{title}` - 文档标题
   - 类型：字符串
   - 示例：`# {title}`

2. `{author}` - 作者信息
   - 类型：列表
   - 格式：自动格式化为markdown列表
   - 示例：
     ```markdown
     - 作者1 (机构1)
     - 作者2 (机构2)
     ```

3. `{summary}` - 文档摘要
   - 类型：字符串
   - 示例：`## 摘要\n{summary}`

4. `{key_points}` - 关键要点
   - 类型：字符串列表
   - 格式：自动格式化为markdown列表
   - 示例：
     ```markdown
     - 关键点1
     - 关键点2
     ```

5. `{conclusion}` - 结论
   - 类型：字符串列表
   - 格式：自动格式化为markdown列表

6. `{recommendations}` - 建议
   - 类型：字符串列表
   - 格式：自动格式化为markdown列表

7. `{detailed_content}` - 详细内容
   - 类型：结构化列表
   - 格式：自动格式化为带标题的章节
   - 示例：
     ```markdown
     ### 第一章
     - 内容点1
     - 内容点2

     ### 第二章
     - 内容点1
     - 内容点2
     ```

## 模板示例

```markdown
# {title}

## 作者
{author}

## 摘要
{summary}

## 关键要点
{key_points}

## 主要结论
{conclusion}

## 建议
{recommendations}

## 详细内容
{detailed_content}
```

## 开发

### 文件结构
```
privateRA/
├── src/                        # 源代码目录
│   ├── pdf_parser/            # PDF解析相关
│   │   └── pdf_parser.py      # PDF解析器实现
│   ├── llm_interface/         # LLM接口相关
│   │   ├── __init__.py
│   │   ├── base_llm.py       # LLM基类
│   │   ├── deepseek_llm.py   # DeepSeek LLM实现
│   │   └── llm_factory.py    # LLM工厂类
│   └── utils/                 # 工具类
│       ├── __init__.py
│       ├── config.py         # 配置管理
│       └── output_parser.py  # 输出解析器
│
├── config.yaml              # 配置文件
├── requirements.txt         # 项目依赖
├── README.md               # 项目说明
├── README_EN.md            # 项目说明（英文）
├── template.md             # 模板文件
└── LICENSE                 # 许可证
```

### 添加新的LLM支持
1. 在 `src/llm_interface` 下创建新的LLM类
2. 继承 `BaseLLM` 类并实现必要方法
3. 在 `LLMFactory` 中添加新的LLM类型支持

## 许可证

本项目采用 [MIT 许可证](LICENSE) 进行许可。

