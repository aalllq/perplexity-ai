"""
LiteLLM Custom Provider Adapter for Perplexity AI
This module allows using Perplexity AI as a custom provider in LiteLLM.
"""

from typing import Optional, List, Dict, Any, Union
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from perplexity import Client


class PerplexityLiteLLMProvider:
    """
    Custom LiteLLM provider for Perplexity AI.
    This allows using Perplexity through LiteLLM's unified interface.
    """
    
    def __init__(self, cookies: Optional[Dict] = None):
        """
        Initialize the Perplexity provider.
        
        Args:
            cookies: Optional Perplexity cookies for authenticated access
        """
        self.client = Client(cookies=cookies or {})
        self.provider_name = "perplexity"
    
    def completion(
        self,
        model: str,
        messages: List[Dict[str, str]],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Union[Dict[str, Any], Any]:
        """
        Generate a completion using Perplexity AI.
        
        Args:
            model: Model name (e.g., "perplexity-auto", "perplexity-pro")
            messages: List of message dictionaries
            temperature: Sampling temperature
            max_tokens: Maximum tokens to generate
            stream: Whether to stream the response
            **kwargs: Additional parameters
            
        Returns:
            Completion response in LiteLLM format
        """
        # Extract query from messages
        query = messages[-1]["content"] if messages else ""
        
        # Map model to mode
        mode_map = {
            "perplexity-auto": "auto",
            "perplexity-pro": "pro",
            "perplexity-reasoning": "reasoning",
            "perplexity-deep-research": "deep research",
        }
        mode = mode_map.get(model, "auto")
        
        # Get model parameter if specified in kwargs
        model_param = kwargs.get("model_param", None)
        
        # Call Perplexity API
        response = self.client.search(
            query=query,
            mode=mode,
            model=model_param,
            stream=stream,
            **kwargs
        )
        
        if stream:
            return self._stream_response(response, model)
        else:
            return self._format_response(response, model)
    
    def _format_response(self, response: Any, model: str) -> Dict[str, Any]:
        """
        Format Perplexity response to LiteLLM format.
        
        Args:
            response: Response from Perplexity
            model: Model name
            
        Returns:
            Formatted response dictionary
        """
        import time
        
        # Extract text from response
        if isinstance(response, dict):
            text = response.get("text", str(response))
        else:
            text = str(response)
        
        # Create LiteLLM-compatible response
        return {
            "id": f"perplexity-{int(time.time())}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": text
                    },
                    "finish_reason": "stop"
                }
            ],
            "usage": {
                "prompt_tokens": 0,  # Perplexity doesn't provide token counts
                "completion_tokens": len(text.split()),
                "total_tokens": len(text.split())
            }
        }
    
    def _stream_response(self, response: Any, model: str):
        """
        Stream Perplexity response in LiteLLM format.
        
        Args:
            response: Streaming response from Perplexity
            model: Model name
            
        Yields:
            Formatted chunk dictionaries
        """
        import time
        
        completion_id = f"perplexity-{int(time.time())}"
        
        for chunk in response:
            if isinstance(chunk, dict):
                text = chunk.get("text", "")
            else:
                text = str(chunk)
            
            if text:
                yield {
                    "id": completion_id,
                    "object": "chat.completion.chunk",
                    "created": int(time.time()),
                    "model": model,
                    "choices": [
                        {
                            "index": 0,
                            "delta": {"content": text},
                            "finish_reason": None
                        }
                    ]
                }


# Register the provider with LiteLLM
def register_perplexity_provider():
    """
    Register Perplexity as a custom provider in LiteLLM.
    Call this function before using Perplexity through LiteLLM.
    """
    try:
        import litellm
        from litellm import CustomLLM
        
        # Create custom provider instance
        provider = PerplexityLiteLLMProvider()
        
        # Register with LiteLLM
        litellm.register_model({
            "perplexity-auto": {
                "max_tokens": 4096,
                "max_input_tokens": 4096,
                "max_output_tokens": 4096,
                "input_cost_per_token": 0.0,
                "output_cost_per_token": 0.0,
                "litellm_provider": "perplexity",
                "mode": "chat"
            },
            "perplexity-pro": {
                "max_tokens": 4096,
                "max_input_tokens": 4096,
                "max_output_tokens": 4096,
                "input_cost_per_token": 0.0,
                "output_cost_per_token": 0.0,
                "litellm_provider": "perplexity",
                "mode": "chat"
            },
            "perplexity-reasoning": {
                "max_tokens": 4096,
                "max_input_tokens": 4096,
                "max_output_tokens": 4096,
                "input_cost_per_token": 0.0,
                "output_cost_per_token": 0.0,
                "litellm_provider": "perplexity",
                "mode": "chat"
            }
        })
        
        print("✓ Perplexity provider registered with LiteLLM")
        return True
        
    except ImportError:
        print("✗ LiteLLM not installed. Install with: pip install litellm")
        return False
    except Exception as e:
        print(f"✗ Error registering Perplexity provider: {e}")
        return False


# Example usage
if __name__ == "__main__":
    print("Registering Perplexity AI as LiteLLM provider...")
    success = register_perplexity_provider()
    
    if success:
        print("\nYou can now use Perplexity through LiteLLM:")
        print("""
import litellm
from perplexity.litellm_adapter import register_perplexity_provider

# Register the provider
register_perplexity_provider()

# Use it like any other LiteLLM model
response = litellm.completion(
    model="perplexity-auto",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response)
""")
