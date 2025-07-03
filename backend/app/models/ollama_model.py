import ollama
from typing import Dict, Any, AsyncGenerator
import logging
from .llm_interface import LLMInterface

logger = logging.getLogger(__name__)

class OllamaModel(LLMInterface):
    """Ollama LLM implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        self.client = ollama.AsyncClient(
            host=config.get("ollama", {}).get("base_url", "http://localhost:11434"),
            timeout=config.get("ollama", {}).get("timeout", 60)
        )
    
    async def generate_response(self, messages: list, stream: bool = False) -> str | AsyncGenerator[str, None]:
        """Generate response using Ollama"""
        try:
            if stream:
                return self._stream_response(messages)
            else:
                response = await self.client.chat(
                    model=self.model_id,
                    messages=messages,
                    options={
                        "temperature": self.temperature,
                        "top_p": self.top_p,
                        "num_predict": self.max_tokens
                    }
                )
                return response["message"]["content"]
        except Exception as e:
            logger.error(f"Error generating response with Ollama: {e}")
            raise
    
    async def _stream_response(self, messages: list) -> AsyncGenerator[str, None]:
        """Stream response from Ollama"""
        try:
            async for chunk in await self.client.chat(
                model=self.model_id,
                messages=messages,
                stream=True,
                options={
                    "temperature": self.temperature,
                    "top_p": self.top_p,
                    "num_predict": self.max_tokens
                }
            ):
                if chunk["message"]["content"]:
                    yield chunk["message"]["content"]
        except Exception as e:
            logger.error(f"Error streaming response with Ollama: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if Ollama is available"""
        try:
            models = await self.client.list()
            logger.info(f"Raw models response: {models}")
            logger.info(f"Models type: {type(models)}")
            
            if hasattr(models, 'models'):
                models_list = models.models
            elif isinstance(models, dict) and 'models' in models:
                models_list = models['models']
            else:
                logger.error(f"Unexpected models response structure: {models}")
                return False
            
            logger.info(f"Models list: {models_list}")
            logger.info(f"Models list type: {type(models_list)}")
            
            available_models = []
            for model in models_list:
                logger.info(f"Processing model: {model}, type: {type(model)}")
                if hasattr(model, 'model'):
                    available_models.append(model.model)
                elif hasattr(model, 'name'):
                    available_models.append(model.name)
                elif isinstance(model, dict) and 'model' in model:
                    available_models.append(model['model'])
                elif isinstance(model, dict) and 'name' in model:
                    available_models.append(model['name'])
                else:
                    logger.warning(f"Model has no model/name attribute: {model}")
            
            model_available = (
                self.model_id in available_models or 
                f"{self.model_id}:latest" in available_models
            )
            
            logger.info(f"Available models: {available_models}")
            logger.info(f"Looking for model: {self.model_id}")
            logger.info(f"Model available: {model_available}")
            
            return model_available
        except Exception as e:
            logger.error(f"Ollama health check failed: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return False
