"""
API Adapter module for LiteLLM and OpenAI API integrations.
Provides a unified interface for working with multiple AI providers.
"""

import os
import json
from typing import Optional, Dict, List, Generator, Union, Any


class LiteLLMClient:
    """
    A client for interacting with various AI models through LiteLLM.
    LiteLLM provides a unified interface to 100+ LLM APIs (OpenAI, Anthropic, etc.)
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo", **kwargs):
        """
        Initialize the LiteLLM client.

        Args:
            api_key: API key for the provider (optional, can use env vars)
            model: Model name to use (default: gpt-3.5-turbo)
            **kwargs: Additional configuration options
        """
        try:
            import litellm
            self.litellm = litellm
        except ImportError:
            raise ImportError(
                "LiteLLM is not installed. Please install it with: pip install litellm"
            )

        self.model = model
        self.api_key = api_key
        self.config = kwargs

        # Set API key if provided
        if api_key:
            os.environ.setdefault("OPENAI_API_KEY", api_key)

    def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        """
        Send a chat completion request.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            stream: Whether to stream the response
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API

        Returns:
            Response dictionary or generator for streaming responses
        """
        try:
            response = self.litellm.completion(
                model=self.model,
                messages=messages,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
                **{**self.config, **kwargs}
            )

            if stream:
                return self._stream_response(response)
            else:
                return self._parse_response(response)

        except Exception as e:
            raise Exception(f"LiteLLM API error: {str(e)}")

    def search(
        self,
        query: str,
        system_prompt: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        """
        Perform a search/query using the LiteLLM API.

        Args:
            query: The search query
            system_prompt: Optional system prompt to guide the response
            stream: Whether to stream the response
            **kwargs: Additional parameters

        Returns:
            Response dictionary or generator for streaming responses
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})

        return self.chat(messages=messages, stream=stream, **kwargs)

    def _stream_response(self, response) -> Generator[Dict[str, Any], None, None]:
        """Generator for streaming responses."""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield {
                    "text": chunk.choices[0].delta.content,
                    "model": chunk.model,
                    "finish_reason": chunk.choices[0].finish_reason
                }

    def _parse_response(self, response) -> Dict[str, Any]:
        """Parse a non-streaming response."""
        return {
            "text": response.choices[0].message.content,
            "model": response.model,
            "finish_reason": response.choices[0].finish_reason,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }


class OpenAIClient:
    """
    A client for interacting directly with the OpenAI API.
    Provides standard OpenAI functionality with error handling.
    """

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo", **kwargs):
        """
        Initialize the OpenAI client.

        Args:
            api_key: OpenAI API key (optional, can use OPENAI_API_KEY env var)
            model: Model name to use (default: gpt-3.5-turbo)
            **kwargs: Additional configuration options
        """
        try:
            from openai import OpenAI
            self.OpenAI = OpenAI
        except ImportError:
            raise ImportError(
                "OpenAI is not installed. Please install it with: pip install openai"
            )

        self.model = model
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OpenAI API key is required. Set OPENAI_API_KEY environment variable "
                "or pass api_key parameter."
            )

        self.client = self.OpenAI(api_key=self.api_key, **kwargs)

    def chat(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        """
        Send a chat completion request.

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            stream: Whether to stream the response
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens to generate
            **kwargs: Additional parameters for the API

        Returns:
            Response dictionary or generator for streaming responses
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=stream,
                temperature=temperature,
                max_tokens=max_tokens,
                **kwargs
            )

            if stream:
                return self._stream_response(response)
            else:
                return self._parse_response(response)

        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")

    def search(
        self,
        query: str,
        system_prompt: Optional[str] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[Dict[str, Any], Generator[Dict[str, Any], None, None]]:
        """
        Perform a search/query using the OpenAI API.

        Args:
            query: The search query
            system_prompt: Optional system prompt to guide the response
            stream: Whether to stream the response
            **kwargs: Additional parameters

        Returns:
            Response dictionary or generator for streaming responses
        """
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": query})

        return self.chat(messages=messages, stream=stream, **kwargs)

    def _stream_response(self, response) -> Generator[Dict[str, Any], None, None]:
        """Generator for streaming responses."""
        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                yield {
                    "text": chunk.choices[0].delta.content,
                    "model": chunk.model,
                    "finish_reason": chunk.choices[0].finish_reason
                }

    def _parse_response(self, response) -> Dict[str, Any]:
        """Parse a non-streaming response."""
        return {
            "text": response.choices[0].message.content,
            "model": response.model,
            "finish_reason": response.choices[0].finish_reason,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            }
        }
