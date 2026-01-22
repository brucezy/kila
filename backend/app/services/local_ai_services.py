import httpx
import logging
from typing import Optional, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)


class LocalModelService:
    """Service for interacting with local models (wrapped in ollama)"""

    def __init__(self):
        self.base_url = settings.ai_model_url.rstrip('/')
        self.model = settings.ai_model
        self.timeout = httpx.Timeout(settings.ai_timeout, read=settings.ai_timeout)  # Longer timeout for local models

    async def generate(
            self,
            prompt: str,
            stream: bool = False,
            options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Generate text using local model.

        Args:
            prompt: The input prompt
            stream: Whether to stream the response
            options: Additional model options (temperature, top_p, etc.)

        Returns:
            str: Generated text response
        """
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            # "format": "json",
            "stream": stream
        }

        print(payload)

        if options:
            payload["options"] = options

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

                result = response.json()
                return result.get("response", "")

        except httpx.HTTPError as e:
            logger.error(f"Ollama HTTP error: {str(e)}")
            raise Exception(f"Failed to call Ollama: {str(e)}")
        except Exception as e:
            logger.error(f"Ollama error: {str(e)}")
            raise Exception(f"Ollama processing error: {str(e)}")

    async def chat(
            self,
            messages: list[Dict[str, str]],
            stream: bool = False
    ) -> str:
        """
        Chat completion using local model.

        Args:
            messages: List of message dicts with 'role' and 'content'
                     [{"role": "user", "content": "Hello"}]
            stream: Whether to stream the response

        Returns:
            str: Generated response
        """
        url = f"{self.base_url}/api/chat"

        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()

                result = response.json()
                message = result.get("message", {})
                return message.get("content", "")

        except httpx.HTTPError as e:
            logger.error(f"Ollama chat HTTP error: {str(e)}")
            raise Exception(f"Failed to call Ollama chat: {str(e)}")
        except Exception as e:
            logger.error(f"Ollama chat error: {str(e)}")
            raise Exception(f"Ollama chat processing error: {str(e)}")

    async def list_models(self) -> list[str]:
        """List available Ollama models"""
        url = f"{self.base_url}/api/tags"

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(url)
                response.raise_for_status()

                result = response.json()
                models = result.get("models", [])
                return [model["name"] for model in models]

        except Exception as e:
            logger.error(f"Failed to list Ollama models: {str(e)}")
            return []

    async def check_health(self) -> bool:
        """Check if Ollama service is running"""
        try:
            async with httpx.AsyncClient(timeout=httpx.Timeout(5.0)) as client:
                response = await client.get(self.base_url)
                return response.status_code == 200
        except:
            return False


# Create global instance
local_model_service = LocalModelService()
