"""
Example script demonstrating asynchronous LiteLLM integration.
This script shows various ways to use the async LiteLLM client.
"""

import os
import asyncio
import perplexity_async


async def example_basic_search():
    """Basic async search example with LiteLLM."""
    print("=" * 60)
    print("Example 1: Basic Async Search with LiteLLM")
    print("=" * 60)
    
    try:
        # Initialize async client
        client = perplexity_async.AsyncLiteLLMClient(model="gpt-3.5-turbo")
        
        # Perform an async search
        response = await client.search(
            query="What is asynchronous programming?",
            stream=False
        )
        
        print(f"Query: What is asynchronous programming?")
        print(f"Response: {response['text']}")
        print(f"Model: {response['model']}")
        print(f"Tokens used: {response['usage']['total_tokens']}")
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        print()


async def example_streaming():
    """Async streaming response example."""
    print("=" * 60)
    print("Example 2: Async Streaming Response")
    print("=" * 60)
    
    try:
        client = perplexity_async.AsyncLiteLLMClient(model="gpt-3.5-turbo")
        
        print("Query: Explain the benefits of async programming")
        print("Response (streaming): ", end='', flush=True)
        
        async for chunk in await client.search(
            query="Explain the benefits of async programming",
            stream=True,
            temperature=0.7
        ):
            if chunk['text']:
                print(chunk['text'], end='', flush=True)
        
        print("\n")
        
    except Exception as e:
        print(f"\nError: {e}\n")


async def example_concurrent_requests():
    """Example demonstrating concurrent async requests."""
    print("=" * 60)
    print("Example 3: Concurrent Async Requests")
    print("=" * 60)
    
    try:
        client = perplexity_async.AsyncLiteLLMClient(model="gpt-3.5-turbo")
        
        # Define multiple queries
        queries = [
            "What is Python?",
            "What is JavaScript?",
            "What is Rust?",
            "What is Go?"
        ]
        
        # Create tasks for concurrent execution
        tasks = [
            client.search(query=query, stream=False, max_tokens=100)
            for query in queries
        ]
        
        print("Running 4 queries concurrently...")
        
        # Execute all queries concurrently
        responses = await asyncio.gather(*tasks)
        
        # Display results
        for query, response in zip(queries, responses):
            print(f"\nQuery: {query}")
            print(f"Response: {response['text'][:100]}...")
            print(f"Tokens: {response['usage']['total_tokens']}")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


async def example_with_system_prompt():
    """Example with custom system prompt."""
    print("=" * 60)
    print("Example 4: Async Search with System Prompt")
    print("=" * 60)
    
    try:
        client = perplexity_async.AsyncLiteLLMClient(model="gpt-3.5-turbo")
        
        response = await client.search(
            query="Write a Python async function to fetch multiple URLs",
            system_prompt="You are an expert Python programmer specializing in async/await patterns.",
            temperature=0.5,
            stream=False
        )
        
        print("Query: Write a Python async function to fetch multiple URLs")
        print(f"Response:\n{response['text']}")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


async def example_chat_method():
    """Example using the async chat method directly."""
    print("=" * 60)
    print("Example 5: Direct Async Chat Method")
    print("=" * 60)
    
    try:
        client = perplexity_async.AsyncLiteLLMClient(model="gpt-3.5-turbo")
        
        # Create a conversation
        messages = [
            {"role": "system", "content": "You are an expert in distributed systems."},
            {"role": "user", "content": "Explain the CAP theorem"},
        ]
        
        response = await client.chat(
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


async def example_mixed_sync_async():
    """Example showing how to mix async and regular operations."""
    print("=" * 60)
    print("Example 6: Mixed Async and Regular Operations")
    print("=" * 60)
    
    try:
        client = perplexity_async.AsyncLiteLLMClient(model="gpt-3.5-turbo")
        
        # Some regular synchronous operations
        queries_data = [
            {"query": "What is Docker?", "max_tokens": 80},
            {"query": "What is Kubernetes?", "max_tokens": 80},
        ]
        
        print("Processing queries with different configurations...")
        
        # Process each query asynchronously
        for i, data in enumerate(queries_data, 1):
            print(f"\n{i}. Query: {data['query']}")
            
            response = await client.search(
                query=data['query'],
                stream=False,
                max_tokens=data['max_tokens']
            )
            
            print(f"   Response: {response['text'][:100]}...")
        
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


async def example_streaming_with_processing():
    """Example showing stream processing with custom logic."""
    print("=" * 60)
    print("Example 7: Streaming with Processing")
    print("=" * 60)
    
    try:
        client = perplexity_async.AsyncLiteLLMClient(model="gpt-3.5-turbo")
        
        print("Query: List 5 programming languages")
        print("Processing stream with character counting...\n")
        
        total_chars = 0
        chunks_received = 0
        
        async for chunk in await client.search(
            query="List 5 programming languages with a brief description of each",
            stream=True,
            temperature=0.7,
            max_tokens=200
        ):
            if chunk['text']:
                text = chunk['text']
                total_chars += len(text)
                chunks_received += 1
                print(text, end='', flush=True)
        
        print(f"\n\nStream Statistics:")
        print(f"  Total characters received: {total_chars}")
        print(f"  Total chunks received: {chunks_received}")
        print()
        
    except Exception as e:
        print(f"\nError: {e}\n")


async def main():
    """Run all async examples."""
    print("\n")
    print("*" * 60)
    print("LiteLLM Integration Examples (Asynchronous)")
    print("*" * 60)
    print("\nNote: Make sure to set your API keys before running these examples.")
    print("You can set them via environment variables or pass them to the client.")
    print()
    
    # Run examples (comment out any you don't want to run)
    await example_basic_search()
    await example_streaming()
    await example_concurrent_requests()
    await example_with_system_prompt()
    await example_chat_method()
    await example_mixed_sync_async()
    await example_streaming_with_processing()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
