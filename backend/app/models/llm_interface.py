from abc import ABC, abstractmethod
from typing import Dict, Any, AsyncGenerator
import logging

logger = logging.getLogger(__name__)

class LLMInterface(ABC):
    """Abstract base class for LLM implementations"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.model_name = config.get("name", "unknown")
        self.model_id = config.get("model_id", "")
        self.temperature = config.get("temperature", 0.7)
        self.max_tokens = config.get("max_tokens", 2048)
        self.top_p = config.get("top_p", 0.9)
    
    @abstractmethod
    async def generate_response(self, messages: list, stream: bool = False) -> str | AsyncGenerator[str, None]:
        """Generate response from the LLM"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the LLM is available and healthy"""
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information"""
        return {
            "name": self.model_name,
            "model_id": self.model_id,
            "type": self.config.get("type", "unknown"),
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p
        }
