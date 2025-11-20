"""
Example script demonstrating asynchronous OpenAI API integration.
This script shows various ways to use the async OpenAI client.
"""

import os
import asyncio
import perplexity_async


async def example_basic_search():
    """Basic async search example with OpenAI."""
    print("=" * 60)
    print("Example 1: Basic Async Search with OpenAI")
    print("=" * 60)
    
    try:
        # Initialize async client
        client = perplexity_async.AsyncOpenAIClient(model="gpt-3.5-turbo")
        
        # Perform an async search
        response = await client.search(
            query="What is deep learning?",
            stream=False
        )
        
        print(f"Query: What is deep learning?")
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
        client = perplexity_async.AsyncOpenAIClient(model="gpt-3.5-turbo")
        
        print("Query: Explain transformer architecture in AI")
        print("Response (streaming): ", end='', flush=True)
        
        async for chunk in await client.search(
            query="Explain transformer architecture in AI",
            stream=True,
            temperature=0.7,
            max_tokens=300
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
        client = perplexity_async.AsyncOpenAIClient(model="gpt-3.5-turbo")
        
        # Define multiple queries
        queries = [
            "What is TensorFlow?",
            "What is PyTorch?",
            "What is scikit-learn?",
            "What is Keras?"
        ]
        
        # Create tasks for concurrent execution
        tasks = [
            client.search(query=query, stream=False, max_tokens=100)
            for query in queries
        ]
        
        print("Running 4 queries concurrently...")
        start_time = asyncio.get_event_loop().time()
        
        # Execute all queries concurrently
        responses = await asyncio.gather(*tasks)
        
        elapsed_time = asyncio.get_event_loop().time() - start_time
        
        # Display results
        for query, response in zip(queries, responses):
            print(f"\nQuery: {query}")
            print(f"Response: {response['text'][:100]}...")
            print(f"Tokens: {response['usage']['total_tokens']}")
        
        print(f"\nTotal time for 4 concurrent requests: {elapsed_time:.2f} seconds")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


async def example_with_system_prompt():
    """Example with custom system prompt."""
    print("=" * 60)
    print("Example 4: Async Search with System Prompt")
    print("=" * 60)
    
    try:
        client = perplexity_async.AsyncOpenAIClient(model="gpt-3.5-turbo")
        
        response = await client.search(
            query="Write an async Python function to process a queue of tasks",
            system_prompt="You are an expert Python developer specializing in asyncio and concurrent programming.",
            temperature=0.5,
            stream=False
        )
        
        print("Query: Write an async Python function to process a queue of tasks")
        print(f"Response:\n{response['text']}")
        print(f"\nToken usage:")
        print(f"  Prompt: {response['usage']['prompt_tokens']}")
        print(f"  Completion: {response['usage']['completion_tokens']}")
        print(f"  Total: {response['usage']['total_tokens']}")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


async def example_chat_method():
    """Example using the async chat method directly."""
    print("=" * 60)
    print("Example 5: Direct Async Chat Method")
    print("=" * 60)
    
    try:
        client = perplexity_async.AsyncOpenAIClient(model="gpt-3.5-turbo")
        
        # Create a multi-turn conversation
        messages = [
            {"role": "system", "content": "You are an AI expert explaining concepts clearly."},
            {"role": "user", "content": "What is the difference between supervised and unsupervised learning?"},
        ]
        
        response = await client.chat(
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )
        
        print("Conversation:")
        for msg in messages:
            print(f"  {msg['role'].title()}: {msg['content']}")
        
        print(f"\nAssistant Response: {response['text']}")
        print(f"Model: {response['model']}")
        print(f"Tokens used: {response['usage']['total_tokens']}")
        print()
        
    except Exception as e:
        print(f"Error: {e}\n")


async def example_batch_processing():
    """Example showing batch processing of multiple items."""
    print("=" * 60)
    print("Example 6: Batch Processing")
    print("=" * 60)
    
    try:
        client = perplexity_async.AsyncOpenAIClient(model="gpt-3.5-turbo")
        
        # Simulate processing a batch of items
        items = [
            "artificial intelligence",
            "blockchain technology",
            "quantum computing"
        ]
        
        print(f"Processing {len(items)} items in batch...\n")
        
        async def process_item(item):
            response = await client.search(
                query=f"Define {item} in one sentence",
                stream=False,
                max_tokens=50
            )
            return item, response['text']
        
        # Process all items concurrently
        results = await asyncio.gather(*[process_item(item) for item in items])
        
        # Display results
        for item, definition in results:
            print(f"{item.title()}:")
            print(f"  {definition}")
            print()
        
    except Exception as e:
        print(f"Error: {e}\n")


async def example_streaming_with_aggregation():
    """Example showing stream aggregation."""
    print("=" * 60)
    print("Example 7: Streaming with Aggregation")
    print("=" * 60)
    
    try:
        client = perplexity_async.AsyncOpenAIClient(model="gpt-3.5-turbo")
        
        print("Query: Write a haiku about technology")
        print("Streaming response...\n")
        
        full_response = []
        word_count = 0
        
        async for chunk in await client.search(
            query="Write a haiku about technology",
            stream=True,
            temperature=0.9,
            max_tokens=100
        ):
            if chunk['text']:
                text = chunk['text']
                full_response.append(text)
                word_count += len(text.split())
                print(text, end='', flush=True)
        
        print(f"\n\nAggregated Response:")
        print(f"  Full text: {''.join(full_response)}")
        print(f"  Word count: {word_count}")
        print()
        
    except Exception as e:
        print(f"\nError: {e}\n")


async def example_with_retry_logic():
    """Example showing retry logic for handling transient errors."""
    print("=" * 60)
    print("Example 8: Request with Retry Logic")
    print("=" * 60)
    
    async def search_with_retry(client, query, max_retries=3):
        """Helper function with retry logic."""
        for attempt in range(max_retries):
            try:
                response = await client.search(query=query, stream=False)
                return response
            except Exception as e:
                if attempt < max_retries - 1:
                    wait_time = 2 ** attempt  # Exponential backoff
                    print(f"  Attempt {attempt + 1} failed: {str(e)[:50]}")
                    print(f"  Retrying in {wait_time} seconds...")
                    await asyncio.sleep(wait_time)
                else:
                    raise
    
    try:
        client = perplexity_async.AsyncOpenAIClient(model="gpt-3.5-turbo")
        
        print("Making request with retry logic...")
        response = await search_with_retry(
            client,
            query="What is the future of AI?",
            max_retries=3
        )
        
        print(f"Success! Response: {response['text'][:100]}...")
        print()
        
    except Exception as e:
        print(f"All retries failed: {e}\n")


async def main():
    """Run all async examples."""
    print("\n")
    print("*" * 60)
    print("OpenAI API Integration Examples (Asynchronous)")
    print("*" * 60)
    print("\nNote: Make sure to set your OPENAI_API_KEY before running these examples.")
    print("You can set it via environment variable or pass it to the client.")
    print()
    
    # Run examples (comment out any you don't want to run)
    await example_basic_search()
    await example_streaming()
    await example_concurrent_requests()
    await example_with_system_prompt()
    await example_chat_method()
    await example_batch_processing()
    await example_streaming_with_aggregation()
    await example_with_retry_logic()
    
    print("=" * 60)
    print("Examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
