import anthropic
from typing import Dict, Any, AsyncGenerator
import logging
from .llm_interface import LLMInterface

logger = logging.getLogger(__name__)

class AnthropicModel(LLMInterface):
    """Anthropic Claude LLM implementation"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__(config)
        api_key = config.get("anthropic", {}).get("api_key")
        if not api_key:
            raise ValueError("Anthropic API key is required")
        
        self.client = anthropic.AsyncAnthropic(
            api_key=api_key,
            timeout=config.get("anthropic", {}).get("timeout", 60)
        )
    
    async def generate_response(self, messages: list, stream: bool = False) -> str | AsyncGenerator[str, None]:
        """Generate response using Anthropic Claude"""
        try:
            system_message = ""
            user_messages = []
            
            for msg in messages:
                if msg["role"] == "system":
                    system_message = msg["content"]
                else:
                    user_messages.append(msg)
            
            if stream:
                return self._stream_response(system_message, user_messages)
            else:
                response = await self.client.messages.create(
                    model=self.model_id,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    system=system_message,
                    messages=user_messages
                )
                return response.content[0].text
        except Exception as e:
            logger.error(f"Error generating response with Anthropic: {e}")
            raise
    
    async def _stream_response(self, system_message: str, user_messages: list) -> AsyncGenerator[str, None]:
        """Stream response from Anthropic"""
        try:
            async with self.client.messages.stream(
                model=self.model_id,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                system=system_message,
                messages=user_messages
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as e:
            logger.error(f"Error streaming response with Anthropic: {e}")
            raise
    
    async def health_check(self) -> bool:
        """Check if Anthropic API is available"""
        try:
            await self.client.messages.create(
                model=self.model_id,
                max_tokens=1,
                messages=[{"role": "user", "content": "test"}]
            )
            return True
        except Exception as e:
            logger.error(f"Anthropic health check failed: {e}")
            return False
