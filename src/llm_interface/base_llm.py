from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseLLM(ABC):
    """大模型接口基类"""
    
    def __init__(self, api_key: str, model_config: Optional[Dict[str, Any]] = None):
        """
        初始化大模型接口
        Args:
            api_key: API密钥
            model_config: 模型配置参数
        """
        self.api_key = api_key
        self.model_config = model_config or {}