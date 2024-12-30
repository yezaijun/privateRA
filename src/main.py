import argparse
from pathlib import Path
from src.pdf_parser.pdf_parser import PDFParser
from src.llm_interface.llm_factory import LLMFactory
from src.utils.output_parser import OutputParser


def process_document(config_path: str, template_path: str, pdf_path: str, output_path: str):
    """
    处理PDF文档并生成分析报告
    
    Args:
        config_path: 配置文件路径
        template_path: 模板文件路径
        pdf_path: PDF文件路径
        output_path: 输出文件路径
    """
    # 初始化组件
    llm = LLMFactory.create_llm_from_config(config_path)
    output_parser = OutputParser(template_path)
    pdf_parser = PDFParser(pdf_path)
    
    try:
        # 解析PDF
        documents = pdf_parser.parse()
        
        # 合并所有页面的内容
        full_text = "\n".join([doc.page_content for doc in documents])
        
        # 获取输出格式指令
        output_format = output_parser.get_format_instructions()
        
        # 准备prompt
        system_prompt = f"""
        You are a professional document analysis assistant. Your tasks are:
        1. Carefully read and understand the document content
        2. Extract key information and organize it in a structured way
        3. Maintain an objective and professional analytical approach
        4. Ensure output format strictly follows requirements
        5. For uncertain information, clearly mark as "Not Provided" or "Cannot Determine"

        Please analyze according to the following requirements:
        - Title: Extract the complete document title
        - Author: Identify all author names and institutions if available
        - Summary: Summarize the core content in 200-300 words
        - Key Points: Extract at least 3 most important arguments or findings
        - Conclusions: Summarize main conclusions and research findings
        - Recommendations: Propose at least 2 specific actionable suggestions based on content

        Note:
        1. Maintain objectivity, avoid subjective speculation
        2. Ensure accuracy and completeness of information
        3. Use clear and structured language
        4. Important conclusions must be supported by document content

        {output_format}
        """

        prompt = f"""
        Document content:
        {full_text}
        """
        
        # 获取结构化输出
        response = llm.chat(
            message=prompt,
            system_prompt=system_prompt
        )
        message = output_parser.parse(response)
        
    except Exception as e:
        message = f"错误：无法解析文档。错误信息：{str(e)}"
    
    # 保存结果
    output_parser.save(message, output_path)
    print(f"分析完成！结果已保存至: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="PDF文档分析工具")
    parser.add_argument("--config", "-c", required=True, help="配置文件路径")
    parser.add_argument("--template", "-t", required=True, help="模板文件路径")
    parser.add_argument("--pdf", "-p", required=True, help="PDF文件路径")
    parser.add_argument("--output", "-o", required=True, help="输出文件路径")
    
    args = parser.parse_args()
    
    # 检查文件是否存在
    for path, path_type in [
        (args.config, "配置文件"),
        (args.template, "模板文件"),
        (args.pdf, "PDF文件")
    ]:
        if not Path(path).exists():
            print(f"错误：{path_type} '{path}' 不存在")
            return
    
    # 确保输出目录存在
    output_dir = Path(args.output).parent
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 处理文档
    process_document(args.config, args.template, args.pdf, args.output)


if __name__ == "__main__":
    main() 