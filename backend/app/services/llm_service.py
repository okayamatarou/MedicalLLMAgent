from typing import Dict, Any, Optional
import logging
from ..config import config_manager
from ..models import LLMInterface, OllamaModel, OpenAIModel, AnthropicModel

logger = logging.getLogger(__name__)

class LLMService:
    """Service for managing LLM interactions"""
    
    def __init__(self):
        self.current_model: Optional[LLMInterface] = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the LLM model based on current configuration"""
        try:
            config = config_manager.get_config()
            model_config = config.model.model  # Access nested model config
            
            model_type = model_config.get("type", "").lower()
            
            if model_type == "ollama":
                self.current_model = OllamaModel(model_config)
            elif model_type == "openai":
                self.current_model = OpenAIModel(model_config)
            elif model_type == "anthropic":
                self.current_model = AnthropicModel(model_config)
            else:
                raise ValueError(f"Unsupported model type: {model_type}")
            
            logger.info(f"Initialized {model_type} model: {model_config.get('name', 'unknown')}")
        except Exception as e:
            logger.error(f"Failed to initialize LLM model: {e}")
            raise
    
    async def switch_model(self, model_name: str) -> bool:
        """Switch to a different model configuration"""
        try:
            config_manager.update_config({"model": model_name})
            
            self._initialize_model()
            
            if await self.current_model.health_check():
                logger.info(f"Successfully switched to model: {model_name}")
                return True
            else:
                logger.error(f"Health check failed for model: {model_name}")
                return False
        except Exception as e:
            logger.error(f"Failed to switch model to {model_name}: {e}")
            return False
    
    async def generate_response(self, messages: list, stream: bool = False):
        """Generate response using current model"""
        if not self.current_model:
            raise RuntimeError("No model initialized")
        
        return await self.current_model.generate_response(messages, stream)
    
    async def health_check(self) -> bool:
        """Check if current model is healthy"""
        if not self.current_model:
            return False
        return await self.current_model.health_check()
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get current model information"""
        if not self.current_model:
            return {}
        return self.current_model.get_model_info()
    
    def get_available_models(self) -> list:
        """Get list of available models"""
        return config_manager.get_available_models()

llm_service = LLMService()
