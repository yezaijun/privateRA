from typing import Dict, Any
from src.llm_interface.base_llm import BaseLLM
from src.llm_interface.deepseek_llm import DeepSeekLLM
from src.utils.config import Config

class LLMFactory:
    """LLM工厂类，用于创建不同的LLM实例"""
    
    @staticmethod
    def create_llm(provider: str, config: Dict[str, Any]) -> BaseLLM:
        """
        创建LLM实例
        Args:
            provider: LLM提供商
            config: 配置信息
        Returns:
            BaseLLM: LLM实例
        """
        if provider == "deepseek":
            return DeepSeekLLM(
                api_key=config['api_key'],
                model_config={'model': config['model']}
            )
        else:
            raise ValueError(f"不支持的LLM提供商: {provider}")
            
    @staticmethod
    def create_llm_from_config(config_path: str) -> BaseLLM:
        """
        从配置文件创建LLM实例
        Args:
            config_path: 配置文件路径
        Returns:
            BaseLLM: LLM实例
        """
        # 加载配置
        config = Config(config_path)
        llm_config = config.get_llm_config()
        
        # 创建LLM实例
        return LLMFactory.create_llm(llm_config['provider'], llm_config['config']) 