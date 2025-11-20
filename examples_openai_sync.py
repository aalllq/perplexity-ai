"""
Example script demonstrating synchronous OpenAI API integration.
This script shows various ways to use the OpenAI client.
"""

import os
import perplexity

def example_basic_search():
    """Basic search example with OpenAI."""
    print("=" * 60)
    print("Example 1: Basic Search with OpenAI")
    print("=" * 60)
    
    # Set your API key (you can also use environment variable)
    # os.environ["OPENAI_API_KEY"] = "sk-your-api-key-here"
    
    try:
        # Initialize client with GPT-3.5-turbo (default)
        client = perplexity.OpenAIClient(model="gpt-3.5-turbo")
        
        # Perform a simple search
        response = client.search(
            query="What is machine learning?",
            stream=False
        )
        
        print(f"Query: What is machine learning?")
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
        client = perplexity.OpenAIClient(model="gpt-3.5-turbo")
        
        print("Query: Explain neural networks")
        print("Response (streaming): ", end='', flush=True)
        
        for chunk in client.search(
            query="Explain neural networks",
            stream=True,
            temperature=0.7,
            max_tokens=300
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
        client = perplexity.OpenAIClient(model="gpt-3.5-turbo")
        
        response = client.search(
            query="Write a Python function to reverse a string",
            system_prompt="You are an expert Python programmer. Provide clean, efficient code with proper documentation.",
            temperature=0.5,
            stream=False
        )
        
        print("Query: Write a Python function to reverse a string")
        print(f"Response:\n{response['text']}")
        print(f"\nToken usage:")
        print(f"  Prompt tokens: {response['usage']['prompt_tokens']}")
        print(f"  Completion tokens: {response['usage']['completion_tokens']}")
        print(f"  Total tokens: {response['usage']['total_tokens']}")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


def example_chat_method():
    """Example using the chat method directly."""
    print("=" * 60)
    print("Example 4: Direct Chat Method")
    print("=" * 60)
    
    try:
        client = perplexity.OpenAIClient(model="gpt-3.5-turbo")
        
        # Create a conversation with multiple messages
        messages = [
            {"role": "system", "content": "You are a helpful assistant with expertise in software development."},
            {"role": "user", "content": "What are the best practices for API design?"},
        ]
        
        response = client.chat(
            messages=messages,
            temperature=0.7,
            max_tokens=500
        )
        
        print("Conversation:")
        for msg in messages:
            print(f"  {msg['role'].title()}: {msg['content']}")
        
        print(f"\nAssistant Response: {response['text']}")
        print(f"Model used: {response['model']}")
        print(f"Tokens used: {response['usage']['total_tokens']}")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


def example_temperature_comparison():
    """Example showing the effect of temperature on responses."""
    print("=" * 60)
    print("Example 5: Temperature Comparison")
    print("=" * 60)
    
    query = "Write a creative story opening about space exploration"
    temperatures = [0.3, 0.7, 1.0]
    
    try:
        client = perplexity.OpenAIClient(model="gpt-3.5-turbo")
        
        for temp in temperatures:
            print(f"\nTemperature: {temp}")
            print("-" * 40)
            
            response = client.search(
                query=query,
                stream=False,
                temperature=temp,
                max_tokens=100
            )
            
            print(f"Response: {response['text']}")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


def example_with_gpt4():
    """Example using GPT-4 (requires GPT-4 API access)."""
    print("=" * 60)
    print("Example 6: Using GPT-4")
    print("=" * 60)
    
    try:
        # Initialize client with GPT-4
        client = perplexity.OpenAIClient(model="gpt-4")
        
        response = client.search(
            query="Explain the concept of quantum entanglement in simple terms",
            stream=False,
            temperature=0.7,
            max_tokens=300
        )
        
        print("Query: Explain the concept of quantum entanglement in simple terms")
        print(f"Response: {response['text']}")
        print(f"Model: {response['model']}")
        print(f"Tokens used: {response['usage']['total_tokens']}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: GPT-4 requires specific API access. Using GPT-3.5-turbo if access not available.")
        print()


def example_error_handling():
    """Example demonstrating error handling."""
    print("=" * 60)
    print("Example 7: Error Handling")
    print("=" * 60)
    
    # Example 1: Missing API key
    print("\n1. Testing with invalid API key:")
    try:
        client = perplexity.OpenAIClient(
            model="gpt-3.5-turbo",
            api_key="invalid-key"
        )
        response = client.search(query="Test query", stream=False)
    except Exception as e:
        print(f"   Caught error: {type(e).__name__}: {str(e)[:100]}")
    
    # Example 2: Invalid model
    print("\n2. Testing with invalid model name:")
    try:
        client = perplexity.OpenAIClient(model="invalid-model-name")
        response = client.search(query="Test query", stream=False)
    except Exception as e:
        print(f"   Caught error: {type(e).__name__}: {str(e)[:100]}")
    
    print("\n3. Proper error handling pattern:")
    print("   Always wrap API calls in try-except blocks to handle errors gracefully.")
    print()


def main():
    """Run all examples."""
    print("\n")
    print("*" * 60)
    print("OpenAI API Integration Examples (Synchronous)")
    print("*" * 60)
    print("\nNote: Make sure to set your OPENAI_API_KEY before running these examples.")
    print("You can set it via environment variable or pass it to the client.")
    print()
    
    # Run examples (comment out any you don't want to run)
    example_basic_search()
    example_streaming()
    example_with_system_prompt()
    example_chat_method()
    example_temperature_comparison()
    # example_with_gpt4()  # Uncomment if you have GPT-4 access
    example_error_handling()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
