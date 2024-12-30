from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from typing import List, Dict, Any

class OutputParser:
    response_schemas: List[ResponseSchema] = [
        ResponseSchema(name="title", description="Document title"),
        ResponseSchema(name="author", description="Document author", type="list"),
        ResponseSchema(name="summary", description="The summary of the document"),
        ResponseSchema(name="key_points", description="List of key points from the document", type="list"),
        ResponseSchema(name="conclusion", description="List of conclusions of the document", type="list"),
        ResponseSchema(name="recommendations", description="Recommendations or action items based on the document content", type="list"),
        ResponseSchema(name="detailed_content", description="Organize and summarize detailed information for each chapter according to the paper structure. Each chapter should be summarized as a dictionary with 'section' and 'content' keys. The content should be a list of strings about the chapter.", type="list")
    ]
    parser = StructuredOutputParser.from_response_schemas(response_schemas)

    def __init__(self, template_path: str):
        """初始化输出解析器"""
        self.template_path = template_path
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = f.read()

    def get_format_instructions(self) -> str:
        """获取格式化指令
        
        Returns:
            str: 格式化指令字符串
        """
        return self.parser.get_format_instructions()
        
    def parse(self, text: str) -> Dict[str, Any]:
        """解析文本到结构化输出
        
        Args:
            text (str): 需要解析的文本
            
        Returns:
            Dict[str, Any]: 解析后的结构化数据
        """
        try:
            return self.parser.parse(text)
        except Exception as e:
            raise Exception(f"解析输出失败: {str(e)}")

    def _format_list(self, items: List[str]) -> str:
        """格式化列表
        
        Args:
            items (List[str]): 列表项
            
        Returns:
            str: 格式化后的列表
        """
        return '\n'.join([f"- {item}" for item in items])

    def _format_detailed_content(self, sections: List[Dict[str, Any]]) -> str:
        """格式化详细内容
        
        Args:
            sections (List[Dict[str, Any]]): 章节内容列表
            
        Returns:
            str: 格式化后的章节内容
        """
        formatted_sections = []
        for section in sections:
            # 添加章节标题
            section_content = [f"### {section['section']}"]
            # 添加章节内容列表
            if type(section['content']) == list:
                section_content.extend([f"- {item}" for item in section['content']])
            else:
                section_content.append(section['content'])
            formatted_sections.append('\n'.join(section_content))
        return '\n\n'.join(formatted_sections)

    def to_template(self, data: Dict[str, Any]) -> str:
        """将解析后的数据转换为模板字符串
        
        Args:
            data (Dict[str, Any]): 解析后的数据
            
        Returns:
            str: 模板字符串
        """
        # 处理数据格式
        formatted_data = {
            'title': data['title'],
            'author': self._format_list(data['author']),
            'summary': data['summary'],
            'key_points': self._format_list(data['key_points']),
            'conclusion': self._format_list(data['conclusion']),
            'recommendations': self._format_list(data['recommendations']),
            'detailed_content': self._format_detailed_content(data.get('detailed_content', []))
        }
        # 使用格式化字符串填充模板
        template_str = self.template
        for key, value in formatted_data.items():
            placeholder = "{" + key + "}"
            if placeholder in template_str:
                template_str = template_str.replace(placeholder, str(value))
        return template_str


    def save(self, data: Dict[str, Any], file_path: str) -> None:
        """将解析后的数据保存到文件
        
        Args:
            data (Dict[str, Any]): 解析后的数据
            file_path (str): 文件路径
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(self.to_template(data))
