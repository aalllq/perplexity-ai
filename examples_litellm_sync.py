"""
Example script demonstrating synchronous LiteLLM integration.
This script shows various ways to use the LiteLLM client.
"""

import os
import perplexity

def example_basic_search():
    """Basic search example with LiteLLM."""
    print("=" * 60)
    print("Example 1: Basic Search with LiteLLM")
    print("=" * 60)
    
    # Set your API key (you can also use environment variable)
    # os.environ["OPENAI_API_KEY"] = "your-api-key-here"
    
    try:
        # Initialize client with GPT-3.5-turbo (default)
        client = perplexity.LiteLLMClient(model="gpt-3.5-turbo")
        
        # Perform a simple search
        response = client.search(
            query="What is the capital of France?",
            stream=False
        )
        
        print(f"Query: What is the capital of France?")
        print(f"Response: {response['text']}")
        print(f"Model: {response['model']}")
        print(f"Tokens used: {response['usage']['total_tokens']}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()


def example_streaming():
    """Streaming response example."""
    print("=" * 60)
    print("Example 2: Streaming Response")
    print("=" * 60)
    
    try:
        client = perplexity.LiteLLMClient(model="gpt-3.5-turbo")
        
        print("Query: Explain quantum computing in simple terms")
        print("Response (streaming): ", end='', flush=True)
        
        for chunk in client.search(
            query="Explain quantum computing in simple terms",
            stream=True,
            temperature=0.7
        ):
            if chunk['text']:
                print(chunk['text'], end='', flush=True)
        
        print("\n")
        
    except Exception as e:
        print(f"\nError: {e}\n")


def example_with_system_prompt():
    """Example with custom system prompt."""
    print("=" * 60)
    print("Example 3: Search with System Prompt")
    print("=" * 60)
    
    try:
        client = perplexity.LiteLLMClient(model="gpt-3.5-turbo")
        
        response = client.search(
            query="Write a Python function to calculate factorial",
            system_prompt="You are an expert Python programmer. Provide clean, well-documented code with type hints.",
            temperature=0.5,
            stream=False
        )
        
        print("Query: Write a Python function to calculate factorial")
        print(f"Response:\n{response['text']}")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


def example_chat_method():
    """Example using the chat method directly."""
    print("=" * 60)
    print("Example 4: Direct Chat Method")
    print("=" * 60)
    
    try:
        client = perplexity.LiteLLMClient(model="gpt-3.5-turbo")
        
        # Create a conversation with multiple messages
        messages = [
            {"role": "system", "content": "You are a helpful assistant specializing in technology."},
            {"role": "user", "content": "What are the main differences between Python and JavaScript?"},
        ]
        
        response = client.chat(
            messages=messages,
            temperature=0.7,
            max_tokens=300
        )
        
        print("Conversation:")
        for msg in messages:
            print(f"  {msg['role'].title()}: {msg['content']}")
        
        print(f"\nAssistant Response: {response['text']}")
        print(f"Tokens used: {response['usage']['total_tokens']}")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


def example_different_models():
    """Example demonstrating different model options."""
    print("=" * 60)
    print("Example 5: Using Different Models")
    print("=" * 60)
    
    # Note: Make sure you have the appropriate API keys set for different providers
    models_to_try = [
        ("gpt-3.5-turbo", "OpenAI"),
        # Uncomment and set appropriate API keys to try other models:
        # ("claude-3-sonnet-20240229", "Anthropic"),
        # ("command-r", "Cohere"),
        # ("gemini-pro", "Google"),
    ]
    
    query = "What is the meaning of life?"
    
    for model, provider in models_to_try:
        try:
            print(f"\nTrying {provider} model: {model}")
            client = perplexity.LiteLLMClient(model=model)
            
            response = client.search(
                query=query,
                stream=False,
                max_tokens=100
            )
            
            print(f"Response: {response['text'][:150]}...")
            
        except Exception as e:
            print(f"Error with {model}: {e}")
    
    print()


def main():
    """Run all examples."""
    print("\n")
    print("*" * 60)
    print("LiteLLM Integration Examples (Synchronous)")
    print("*" * 60)
    print("\nNote: Make sure to set your API keys before running these examples.")
    print("You can set them via environment variables or pass them to the client.")
    print()
    
    # Run examples (comment out any you don't want to run)
    example_basic_search()
    example_streaming()
    example_with_system_prompt()
    example_chat_method()
    example_different_models()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
