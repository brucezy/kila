from anthropic import Anthropic
from app.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Anthropic client
client = Anthropic(api_key=settings.anthropic_api_key)


async def process_prompt(prompt: str) -> str:
    """
    Process a prompt using Claude AI model.

    Args:
        prompt: The user's prompt text

    Returns:
        str: The AI model's response text

    Raises:
        Exception: If AI processing fails
    """
    try:
        logger.info(f"Processing prompt with AI model: {settings.ai_model}")

        response = client.messages.create(
            model=settings.ai_model,
            max_tokens=settings.max_tokens,
            messages=[{
                "role": "user",
                "content": prompt
            }]
        )

        result = response.content[0].text
        logger.info(
            f"AI processing completed. Tokens used: {response.usage.input_tokens + response.usage.output_tokens}")

        return result

    except Exception as e:
        logger.error(f"AI processing error: {str(e)}")
        raise Exception(f"Failed to process prompt with AI model: {str(e)}")
