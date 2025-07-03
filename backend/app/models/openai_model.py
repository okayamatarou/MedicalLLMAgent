import openai
from typing import Dict, Any, AsyncGenerator
import logging
from .llm_interface import LLMInterface

logger = logging.getLogger(__name__)

class OpenAIModel(LLMInterface):
    """OpenAI LLM implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        api_key = config.get("openai", {}).get("api_key")
        if not api_key:
            raise ValueError("OpenAI API key is required")
        
        self.client = openai.AsyncOpenAI(
            api_key=api_key,
            timeout=config.get("openai", {}).get("timeout", 60)
        )
    
    async def generate_response(self, messages: list, stream: bool = False) -> str | AsyncGenerator[str, None]:
        """Generate response using OpenAI"""
        try:
            if stream:
                return self._stream_response(messages)
            else:
                response = await self.client.chat.completions.create(
                    model=self.model_id,
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=self.top_p
                )
                return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating response with OpenAI: {e}")
            raise
    
    async def _stream_response(self, messages: list) -> AsyncGenerator[str, None]:
        """Stream response from OpenAI"""
        try:
            stream = await self.client.chat.completions.create(
                model=self.model_id,
                messages=messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
                top_p=self.top_p,
                stream=True
            )
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"Error streaming response with OpenAI: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if OpenAI API is available"""
        try:
            await self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"OpenAI health check failed: {e}")
            return False
