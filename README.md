# Perplexity AI

Perplexity AI is a Python module that leverages [Emailnator](https://emailnator.com/) to generate new accounts for unlimited pro queries. It supports both synchronous and asynchronous APIs, as well as a web interface for users who prefer a GUI-based approach. **Now with integrated support for LiteLLM and OpenAI API!**

## Features

- **Account Generation**: Automatically generate Gmail accounts using Emailnator.
- **Unlimited Pro Queries**: Bypass query limits by creating new accounts.
- **Web Interface**: Automate account creation and usage via a browser.
- **API Support**: Synchronous and asynchronous APIs for programmatic access.
- **LiteLLM Integration**: Unified interface to 100+ LLM APIs (OpenAI, Anthropic, Cohere, etc.)
- **OpenAI API Support**: Direct integration with OpenAI's GPT models.
- **Enhanced Error Handling**: Comprehensive error handling for API failures.

## Installation

Install the required packages:

```bash
pip install perplexity-api perplexity-api-async
```

For the web interface, install additional dependencies:

```bash
pip install patchright playwright && patchright install chromium
```

For LiteLLM and OpenAI API support, install additional dependencies:

```bash
pip install litellm openai
```

## Usage

### Web Interface

The web interface automates account creation and usage in a browser. [Patchright](https://github.com/Kaliiiiiiiiii-Vinyzu/patchright-python#best-practices) uses ["Chrome User Data Directory"](https://www.google.com/search?q=chrome+user+data+directory) to be completely undetected, it's ``C:\Users\YourName\AppData\Local\Google\Chrome\User Data`` for Windows, as shown below:

```python
import os
from perplexity.driver import Driver

cli = Driver()
cli.run(rf'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data')
```

To use your own Chrome instance, enable remote debugging (it may enter dead loop in Cloudflare):

1. Add `--remote-debugging-port=9222` to Chrome's shortcut target.
2. Pass the port to the `Driver.run()` method:

```python
cli.run(rf'C:\\Users\\{os.getlogin()}\\AppData\\Local\\Google\\Chrome\\User Data', port=9222)
```

### API Usage

#### Synchronous API

Below is an example code for simple usage, without using your own account or generating new accounts.

```python3
import perplexity

perplexity_cli = perplexity.Client()

# mode = ['auto', 'pro', 'reasoning', 'deep research']
# model = model for mode, which can only be used in own accounts, that is {
#     'auto': [None],
#     'pro': [None, 'sonar', 'gpt-4.5', 'gpt-4o', 'claude 3.7 sonnet', 'gemini 2.0 flash', 'grok-2'],
#     'reasoning': [None, 'r1', 'o3-mini', 'claude 3.7 sonnet'],
#     'deep research': [None]
# }
# sources = ['web', 'scholar', 'social']
# files = a dictionary which has keys as filenames and values as file data
# stream = returns a generator when enabled and just final response when disabled
# language = ISO 639 code of language you want to use
# follow_up = last query info for follow-up queries, you can directly pass response from a query, look at second example below
# incognito = Enables incognito mode, for people who are using their own account
resp = perplexity_cli.search('Your query here', mode='auto', model=None, sources=['web'], files={}, stream=False, language='en-US', follow_up=None, incognito=False)
print(resp)

# second example to show how to use follow-up queries and stream response
for i in perplexity_cli.search('Your query here', stream=True, follow_up=resp):
    print(i)
```

And this is how you use your own account, you need to get your cookies in order to use your own account. Look at [How To Get Cookies](#how-to-get-cookies),

```python3
import perplexity

perplexity_cookies = { 
    <your cookies here>
}

perplexity_cli = perplexity.Client(perplexity_cookies)

resp = perplexity_cli.search('Your query here', mode='reasoning', model='o3-mini', sources=['web'], files={'myfile.txt': open('file.txt').read()}, stream=False, language='en-US', follow_up=None, incognito=False)
print(resp)
```

And finally account generating, you need to get cookies for [Emailnator](https://emailnator.com/) to use this feature. Look at [How To Get Cookies](#how-to-get-cookies),

```python3
import perplexity

emailnator_cookies = { 
    <your cookies here>
}

perplexity_cli = perplexity.Client()
perplexity_cli.create_account(emailnator_cookies) # Creates a new gmail, so your 5 pro queries will be renewed.

resp = perplexity_cli.search('Your query here', mode='reasoning', model=None, sources=['web'], files={'myfile.txt': open('file.txt').read()}, stream=False, language='en-US', follow_up=None, incognito=False)
print(resp)
```

#### Asynchronous API

Below is an example code for simple usage, without using your own account or generating new accounts.

```python3
import asyncio
import perplexity_async

async def test():
    perplexity_cli = await perplexity_async.Client()

    # mode = ['auto', 'pro', 'reasoning', 'deep research']
    # model = model for mode, which can only be used in own accounts, that is {
    #     'auto': [None],
    #     'pro': [None, 'sonar', 'gpt-4.5', 'gpt-4o', 'claude 3.7 sonnet', 'gemini 2.0 flash', 'grok-2'],
    #     'reasoning': [None, 'r1', 'o3-mini', 'claude 3.7 sonnet'],
    #     'deep research': [None]
    # }
    # sources = ['web', 'scholar', 'social']
    # files = a dictionary which has keys as filenames and values as file data
    # stream = returns a generator when enabled and just final response when disabled
    # language = ISO 639 code of language you want to use
    # follow_up = last query info for follow-up queries, you can directly pass response from a query, look at second example below
    # incognito = Enables incognito mode, for people who are using their own account
    resp = await perplexity_cli.search('Your query here', mode='auto', model=None, sources=['web'], files={}, stream=False, language='en-US', follow_up=None, incognito=False)
    print(resp)

    # second example to show how to use follow-up queries and stream response
    async for i in await perplexity_cli.search('Your query here', stream=True, follow_up=resp):
        print(i)

asyncio.run(test())
```

And this is how you use your own account, you need to get your cookies in order to use your own account. Look at [How To Get Cookies](#how-to-get-cookies),

```python3
import asyncio
import perplexity_async

perplexity_cookies = { 
    <your cookies here>
}

async def test():
    perplexity_cli = await perplexity_async.Client(perplexity_cookies)

    resp = await perplexity_cli.search('Your query here', mode='reasoning', model='o3-mini', sources=['web'], files={'myfile.txt': open('file.txt').read()}, stream=False, language='en-US', follow_up=None, incognito=False)
    print(resp)

asyncio.run(test())
```

And finally account generating, you need to get cookies for [emailnator](https://emailnator.com/) to use this feature. Look at [How To Get Cookies](#how-to-get-cookies),

```python3
import asyncio
import perplexity_async

emailnator_cookies = { 
    <your cookies here>
}

async def test():
    perplexity_cli = await perplexity_async.Client()
    await perplexity_cli.create_account(emailnator_cookies) # Creates a new gmail, so your 5 pro queries will be renewed.

    resp = await perplexity_cli.search('Your query here', mode='reasoning', model=None, sources=['web'], files={'myfile.txt': open('file.txt').read()}, stream=False, language='en-US', follow_up=None, incognito=False)
    print(resp)

asyncio.run(test())
```

## How to Get Cookies

### Perplexity (to use your own account)
* Open [Perplexity.ai](https://perplexity.ai/) website and login to your account.
* Click F12 or ``Ctrl + Shift + I`` to open inspector.
* Go to the "Network" tab in the inspector.
* Refresh the page, right click the first request, hover on "Copy" and click to "Copy as cURL (bash)".
* Now go to the [CurlConverter](https://curlconverter.com/python/) and paste your code here. The cookies dictionary will appear, copy and use it in your codes.

<img src="images/perplexity.png">

### Emailnator (for account generating)
* Open [Emailnator](https://emailnator.com/) website and verify you're human.
* Click F12 or ``Ctrl + Shift + I`` to open inspector.
* Go to the "Network" tab in the inspector.
* Refresh the page, right click the first request, hover on "Copy" and click to "Copy as cURL (bash)".
* Now go to the [CurlConverter](https://curlconverter.com/python/) and paste your code here. The cookies dictionary will appear, copy and use it in your codes.
* Cookies for [Emailnator](https://emailnator.com/) are temporary, you need to renew them continuously.

<img src="images/emailnator.png">

## LiteLLM Integration

LiteLLM provides a unified interface to interact with 100+ LLM APIs including OpenAI, Anthropic, Cohere, Hugging Face, and more. This integration allows you to easily switch between different AI providers with minimal code changes.

### Synchronous LiteLLM Usage

```python
import perplexity
import os

# Set your API key (or use environment variable)
os.environ["OPENAI_API_KEY"] = "your-api-key-here"

# Initialize LiteLLM client
litellm_client = perplexity.LiteLLMClient(
    model="gpt-3.5-turbo",  # or any other supported model
    api_key="your-api-key-here"  # optional if using env var
)

# Simple search/query
response = litellm_client.search(
    query="What is the capital of France?",
    stream=False
)
print(response['text'])

# With streaming
for chunk in litellm_client.search(
    query="Explain quantum computing",
    stream=True,
    temperature=0.7
):
    print(chunk['text'], end='', flush=True)

# Advanced chat with custom messages
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Tell me a joke about programming."}
]
response = litellm_client.chat(
    messages=messages,
    temperature=0.8,
    max_tokens=150
)
print(response['text'])
print(f"Tokens used: {response['usage']['total_tokens']}")
```

### Asynchronous LiteLLM Usage

```python
import asyncio
import perplexity_async
import os

async def main():
    # Set your API key
    os.environ["OPENAI_API_KEY"] = "your-api-key-here"
    
    # Initialize async LiteLLM client
    litellm_client = perplexity_async.AsyncLiteLLMClient(
        model="gpt-4",
        api_key="your-api-key-here"  # optional if using env var
    )
    
    # Simple async search
    response = await litellm_client.search(
        query="What are the benefits of async programming?",
        stream=False
    )
    print(response['text'])
    
    # Async streaming
    async for chunk in await litellm_client.search(
        query="Explain machine learning",
        stream=True,
        temperature=0.7
    ):
        print(chunk['text'], end='', flush=True)

asyncio.run(main())
```

### Supported Models with LiteLLM

LiteLLM supports 100+ models from various providers:

- **OpenAI**: `gpt-4`, `gpt-4-turbo`, `gpt-3.5-turbo`, etc.
- **Anthropic**: `claude-3-opus-20240229`, `claude-3-sonnet-20240229`, etc.
- **Cohere**: `command-r-plus`, `command-r`, etc.
- **Google**: `gemini-pro`, `gemini-pro-vision`, etc.
- **Azure OpenAI**: `azure/gpt-4`, `azure/gpt-35-turbo`, etc.
- **And many more**: Hugging Face, Replicate, Together AI, Ollama, etc.

Set appropriate API keys as environment variables for each provider:
```python
os.environ["OPENAI_API_KEY"] = "sk-..."
os.environ["ANTHROPIC_API_KEY"] = "sk-ant-..."
os.environ["COHERE_API_KEY"] = "..."
```

## OpenAI API Integration

Direct integration with OpenAI's GPT models for those who prefer to use OpenAI specifically.

### Synchronous OpenAI Usage

```python
import perplexity
import os

# Set your OpenAI API key
os.environ["OPENAI_API_KEY"] = "sk-your-api-key-here"

# Initialize OpenAI client
openai_client = perplexity.OpenAIClient(
    model="gpt-3.5-turbo",
    api_key="sk-your-api-key-here"  # optional if using env var
)

# Simple search/query
response = openai_client.search(
    query="What is machine learning?",
    stream=False
)
print(response['text'])
print(f"Model used: {response['model']}")
print(f"Tokens: {response['usage']['total_tokens']}")

# With streaming
for chunk in openai_client.search(
    query="Explain neural networks",
    stream=True,
    temperature=0.7,
    max_tokens=500
):
    print(chunk['text'], end='', flush=True)

# Advanced chat with system prompt
response = openai_client.search(
    query="Write a Python function to calculate fibonacci numbers",
    system_prompt="You are an expert Python programmer. Provide clean, well-documented code.",
    temperature=0.5
)
print(response['text'])

# Direct chat method with full control
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What are the best practices for API design?"}
]
response = openai_client.chat(
    messages=messages,
    temperature=0.7,
    max_tokens=800
)
print(response['text'])
```

### Asynchronous OpenAI Usage

```python
import asyncio
import perplexity_async
import os

async def main():
    # Set your OpenAI API key
    os.environ["OPENAI_API_KEY"] = "sk-your-api-key-here"
    
    # Initialize async OpenAI client
    openai_client = perplexity_async.AsyncOpenAIClient(
        model="gpt-4",
        api_key="sk-your-api-key-here"  # optional if using env var
    )
    
    # Simple async search
    response = await openai_client.search(
        query="What is the future of AI?",
        stream=False
    )
    print(response['text'])
    
    # Async streaming
    async for chunk in await openai_client.search(
        query="Explain deep learning architectures",
        stream=True,
        temperature=0.7
    ):
        print(chunk['text'], end='', flush=True)
    
    # Multiple concurrent requests
    tasks = [
        openai_client.search("What is Python?", stream=False),
        openai_client.search("What is JavaScript?", stream=False),
        openai_client.search("What is Rust?", stream=False)
    ]
    responses = await asyncio.gather(*tasks)
    for resp in responses:
        print(resp['text'])
        print("---")

asyncio.run(main())
```

### Configuration and Error Handling

Both LiteLLM and OpenAI clients include comprehensive error handling:

```python
import perplexity

try:
    # Initialize client
    client = perplexity.OpenAIClient(
        model="gpt-3.5-turbo",
        api_key="your-api-key"
    )
    
    # Make request
    response = client.search(
        query="Your question here",
        temperature=0.7,
        max_tokens=1000
    )
    
    print(f"Response: {response['text']}")
    print(f"Finish reason: {response['finish_reason']}")
    print(f"Total tokens: {response['usage']['total_tokens']}")
    
except ValueError as e:
    print(f"Configuration error: {e}")
except ImportError as e:
    print(f"Missing dependency: {e}")
except Exception as e:
    print(f"API error: {e}")
```

### Environment Variables

The integrations support the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key
- `ANTHROPIC_API_KEY`: Your Anthropic API key (for Claude models via LiteLLM)
- `COHERE_API_KEY`: Your Cohere API key (for Command models via LiteLLM)
- `HUGGINGFACE_API_KEY`: Your Hugging Face API key (for HF models via LiteLLM)

You can also pass API keys directly when initializing clients for better security:

```python
client = perplexity.OpenAIClient(api_key="sk-...")
# or
client = perplexity.LiteLLMClient(api_key="sk-...", model="gpt-4")
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
