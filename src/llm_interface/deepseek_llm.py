from typing import Dict, Any, Optional, List
from openai import OpenAI
from .base_llm import BaseLLM

class DeepSeekLLM(BaseLLM):
    """DeepSeek大模型接口实现"""
    
    def __init__(self, api_key: str, model_config: Optional[Dict[str, Any]] = None):
        """
        初始化DeepSeek接口
        Args:
            api_key: DeepSeek API密钥
            model_config: 模型配置参数
        """
        super().__init__(api_key, model_config)
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )
        self.model = (model_config or {}).get('model', 'deepseek-chat')
        self.system_prompt = (model_config or {}).get('system_prompt', 'You are a helpful assistant')
        
    def chat(self, system_prompt: str, message: str, history: List[Dict[str, str]] = None) -> str:
        """
        与模型进行对话
        Args:
            system_prompt: 系统提示词
            message: 用户输入的消息
            history: 对话历史记录
        Returns:
            str: 模型的回复
        """
        messages = [{"role": "system", "content": system_prompt}]
        
        # 添加历史记录
        if history:
            messages.extend(history)
            
        # 添加当前用户消息
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"DeepSeek API调用失败: {str(e)}")
            return ""