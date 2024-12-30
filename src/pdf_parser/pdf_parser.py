from langchain_community.document_loaders import PyPDFLoader
from typing import List
from langchain.schema import Document

class PDFParser:
    def __init__(self, pdf_path: str):
        """初始化PDF解析器
        
        Args:
            pdf_path (str): PDF文件路径
        """
        self.pdf_path = pdf_path
        self.loader = PyPDFLoader(pdf_path)
        
    def parse(self) -> List[Document]:
        """解析PDF文件
        
        Returns:
            List[Document]: 解析后的文档列表
        """
        try:
            documents = self.loader.load()
            return documents
        except Exception as e:
            raise Exception(f"解析PDF文件失败: {str(e)}") 