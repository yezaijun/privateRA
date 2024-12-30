# Private Research Assistant

[简体中文](README.md) | English

**Note**: This is a rough implementation without any optimization. Developed with the assistance of [Cursor AI](https://www.cursor.com/).

This is an LLM-based research paper analysis tool that automatically parses academic papers and generates structured analysis reports.

## Features

- Automatic PDF paper parsing
- LLM-based intelligent analysis
- Structured output
- Custom template support
- Multiple LLM model support (currently supports DeepSeek)

## Installation

1. Clone the repository
```bash
git clone [repository-url]
cd privateRA
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Configuration
Create a `config.yaml` file and configure your API key:
```yaml
llm:
  type: "deepseek"  # LLM type
  api_key: "your-api-key"  # API key
  base_url: "https://api.deepseek.com/v1"  # API base URL
```
For DeepSeek API key, please refer to [DeepSeek API Documentation](https://api-docs.deepseek.com/).

## Usage

### Command Line Interface
The simplest way to use the tool is through the command line:

```bash
python -m src.main \
    --config path/to/config.yaml \
    --template path/to/template.md \
    --pdf path/to/document.pdf \
    --output path/to/output.md
```

Or using the short form:

```bash
python -m src.main \
    -c path/to/config.yaml \
    -t path/to/template.md \
    -p path/to/document.pdf \
    -o path/to/output.md
```

Parameters:
- `--config` or `-c`: Configuration file path containing LLM API settings
- `--template` or `-t`: Markdown template file path
- `--pdf` or `-p`: Path to the PDF file to analyze
- `--output` or `-o`: Output file path

### Programmatic Usage
You can also use the components directly in your code:

```python
from src.pdf_parser.pdf_parser import PDFParser
from src.llm_interface.llm_factory import LLMFactory
from src.utils.output_parser import OutputParser

# Initialize components
llm = LLMFactory.create_llm_from_config("config.yaml")
output_parser = OutputParser("templates/default.md")
pdf_parser = PDFParser("your-paper.pdf")

# Parse PDF
documents = pdf_parser.parse()

# Generate analysis report
response = llm.chat(system_prompt=system_prompt, user_prompt=prompt)
result = output_parser.parse(response)
output_parser.save(result, "output.md")
```

## Markdown Template Fields

You can use the following fields in your template (using `{field_name}` syntax):

1. `{title}` - Document title
   - Type: string
   - Example: `# {title}`

2. `{author}` - Author information
   - Type: list
   - Format: automatically formatted as markdown list
   - Example:
     ```markdown
     - Author1 (Institution1)
     - Author2 (Institution2)
     ```

3. `{summary}` - Document summary
   - Type: string
   - Example: `## Summary\n{summary}`

4. `{key_points}` - Key points
   - Type: string list
   - Format: automatically formatted as markdown list
   - Example:
     ```markdown
     - Key point 1
     - Key point 2
     ```

5. `{conclusion}` - Conclusions
   - Type: string list
   - Format: automatically formatted as markdown list

6. `{recommendations}` - Recommendations
   - Type: string list
   - Format: automatically formatted as markdown list

7. `{detailed_content}` - Detailed content
   - Type: structured list
   - Format: automatically formatted as sections with headings
   - Example:
     ```markdown
     ### Chapter 1
     - Content point 1
     - Content point 2

     ### Chapter 2
     - Content point 1
     - Content point 2
     ```

## Template Example

```markdown
# {title}

## Authors
{author}

## Summary
{summary}

## Key Points
{key_points}

## Main Conclusions
{conclusion}

## Recommendations
{recommendations}

## Detailed Content
{detailed_content}
```

## Development

### Project Structure
```
privateRA/
├── src/                        # Source code directory
│   ├── pdf_parser/            # PDF parsing related
│   │   └── pdf_parser.py      # PDF parser implementation
│   ├── llm_interface/         # LLM interface related
│   │   ├── __init__.py
│   │   ├── base_llm.py       # LLM base class
│   │   ├── deepseek_llm.py   # DeepSeek LLM implementation
│   │   └── llm_factory.py    # LLM factory class
│   └── utils/                 # Utility classes
│       ├── __init__.py
│       ├── config.py         # Configuration management
│       └── output_parser.py  # Output parser
│
├── templates/                 # Template directory
│   └── default.md           # Default output template
│
├── testfile/                 # Test file directory
│
├── config.yaml              # Configuration file
├── requirements.txt         # Project dependencies
├── README.md               # Project documentation
├── README_EN.md            # Project documentation (English)
└── template.md             # Template file
```

### Adding New LLM Support
1. Create a new LLM class in `src/llm_interface`
2. Inherit from `BaseLLM` class and implement required methods
3. Add support for the new LLM type in `LLMFactory`

## License

This project is licensed under the [MIT License](LICENSE). 