"""
Example client for Perplexity AI OpenAI-compatible API server.
This demonstrates how to use the API server with the OpenAI Python client.
"""

import os
from openai import OpenAI


def example_basic_completion():
    """Basic completion example."""
    print("=" * 60)
    print("Example 1: Basic Completion")
    print("=" * 60)
    
    # Connect to local Perplexity API server
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"  # API key not required for local server
    )
    
    try:
        response = client.chat.completions.create(
            model="perplexity-auto",
            messages=[
                {"role": "user", "content": "What is the capital of France?"}
            ]
        )
        
        print(f"Model: {response.model}")
        print(f"Response: {response.choices[0].message.content}")
        print(f"Finish reason: {response.choices[0].finish_reason}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()


def example_streaming():
    """Streaming completion example."""
    print("=" * 60)
    print("Example 2: Streaming Completion")
    print("=" * 60)
    
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"
    )
    
    try:
        print("Query: Explain quantum computing")
        print("Response: ", end="", flush=True)
        
        stream = client.chat.completions.create(
            model="perplexity-pro",
            messages=[
                {"role": "user", "content": "Explain quantum computing in simple terms"}
            ],
            stream=True
        )
        
        for chunk in stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        
        print("\n")
        
    except Exception as e:
        print(f"\nError: {e}\n")


def example_with_system_message():
    """Example with system message."""
    print("=" * 60)
    print("Example 3: With System Message")
    print("=" * 60)
    
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"
    )
    
    try:
        response = client.chat.completions.create(
            model="perplexity-auto",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that explains technical concepts clearly."},
                {"role": "user", "content": "What is Docker?"}
            ],
            temperature=0.7
        )
        
        print(f"Response: {response.choices[0].message.content}")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


def example_multi_turn_conversation():
    """Example with multi-turn conversation."""
    print("=" * 60)
    print("Example 4: Multi-turn Conversation")
    print("=" * 60)
    
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"
    )
    
    try:
        messages = [
            {"role": "user", "content": "What is Python?"}
        ]
        
        # First turn
        response = client.chat.completions.create(
            model="perplexity-auto",
            messages=messages
        )
        
        print("User: What is Python?")
        print(f"Assistant: {response.choices[0].message.content[:200]}...")
        
        # Add assistant's response to conversation
        messages.append({
            "role": "assistant",
            "content": response.choices[0].message.content
        })
        
        # Second turn
        messages.append({
            "role": "user",
            "content": "What are its main use cases?"
        })
        
        response = client.chat.completions.create(
            model="perplexity-auto",
            messages=messages
        )
        
        print("\nUser: What are its main use cases?")
        print(f"Assistant: {response.choices[0].message.content[:200]}...")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


def example_different_models():
    """Example using different models."""
    print("=" * 60)
    print("Example 5: Different Models")
    print("=" * 60)
    
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"
    )
    
    models = ["perplexity-auto", "perplexity-pro", "perplexity-reasoning"]
    query = "What is artificial intelligence?"
    
    for model in models:
        try:
            print(f"\nUsing model: {model}")
            print("-" * 40)
            
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": query}],
                max_tokens=100
            )
            
            print(f"Response: {response.choices[0].message.content[:150]}...")
            
        except Exception as e:
            print(f"Error with {model}: {e}")
    
    print()


def example_list_models():
    """Example listing available models."""
    print("=" * 60)
    print("Example 6: List Available Models")
    print("=" * 60)
    
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"
    )
    
    try:
        models = client.models.list()
        
        print("Available models:")
        for model in models.data:
            print(f"  - {model.id} (owned by: {model.owned_by})")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


def example_with_parameters():
    """Example with various parameters."""
    print("=" * 60)
    print("Example 7: With Custom Parameters")
    print("=" * 60)
    
    client = OpenAI(
        base_url="http://localhost:8000/v1",
        api_key="not-needed"
    )
    
    try:
        response = client.chat.completions.create(
            model="perplexity-auto",
            messages=[
                {"role": "user", "content": "Write a short poem about coding"}
            ],
            temperature=0.9,  # Higher temperature for more creative output
            max_tokens=150,
            top_p=0.95
        )
        
        print(f"Response:\n{response.choices[0].message.content}")
        print(f"\nUsage:")
        print(f"  Prompt tokens: {response.usage.prompt_tokens}")
        print(f"  Completion tokens: {response.usage.completion_tokens}")
        print(f"  Total tokens: {response.usage.total_tokens}")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


def main():
    """Run all examples."""
    print("\n")
    print("*" * 60)
    print("Perplexity AI API Server - Client Examples")
    print("*" * 60)
    print("\nMake sure the API server is running:")
    print("  python api_server.py --port 8000")
    print()
    
    # Check if server is accessible
    try:
        client = OpenAI(
            base_url="http://localhost:8000/v1",
            api_key="not-needed"
        )
        # Try to list models as a health check
        client.models.list()
        print("✓ API server is accessible\n")
    except Exception as e:
        print(f"✗ Cannot connect to API server: {e}")
        print("  Please start the server first: python api_server.py\n")
        return
    
    # Run examples
    example_basic_completion()
    example_streaming()
    example_with_system_message()
    example_multi_turn_conversation()
    example_different_models()
    example_list_models()
    example_with_parameters()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
