import os
import yaml
from typing import Dict, Any, Optional

class Config:
    """配置管理类"""
    
    def __init__(self, config_path: str = "config/config.yaml"):
        """
        初始化配置管理器
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config = self._load_config()
        
    def _load_config(self) -> Dict[str, Any]:
        """
        加载配置文件
        Returns:
            Dict: 配置信息
        """
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")
            
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
            
    def get_llm_config(self) -> Dict[str, Any]:
        """
        获取LLM配置
        Returns:
            Dict: LLM配置信息
        """
        provider = self.config['llm']['provider']
        if provider != 'deepseek':
            raise ValueError(f"不支持的LLM提供商: {provider}")
            
        return {
            'provider': provider,
            'config': self.config['llm'][provider]
        }
        
    def get_pdf_config(self) -> Dict[str, Any]:
        """
        获取PDF配置
        Returns:
            Dict: PDF配置信息
        """
        return self.config['pdf']
        
    @staticmethod
    def create_default_config(output_path: str = "config/config.yaml"):
        """
        创建默认配置文件
        Args:
            output_path: 输出路径
        """
        template_path = "config/config.yaml.template"
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"配置模板文件不存在: {template_path}")
            
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if not os.path.exists(output_path):
            with open(template_path, 'r', encoding='utf-8') as src:
                with open(output_path, 'w', encoding='utf-8') as dst:
                    dst.write(src.read()) 