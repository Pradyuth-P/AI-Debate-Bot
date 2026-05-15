import os
import json
import re
from openai import AsyncOpenAI
from typing import List, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class OpenAIService:
    """Service layer for OpenAI API interactions."""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is not set")

        self.client = AsyncOpenAI(api_key=api_key)
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "1000"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.8"))

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = None,
        max_tokens: int = None,
    ) -> str:
        """Send messages to OpenAI and return the response text."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")

    async def json_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: float = 0.3,
    ) -> Dict[str, Any]:
        """Send messages expecting a JSON response."""
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=500,
                response_format={"type": "json_object"},
            )
            content = response.choices[0].message.content.strip()
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback: try to extract JSON from response
            content = response.choices[0].message.content.strip()
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            raise RuntimeError("Failed to parse JSON response from OpenAI")
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
