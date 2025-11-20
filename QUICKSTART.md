# Quick Start Guide

This guide will help you get started with Perplexity AI's new API server and LiteLLM integration features.

## Installation

```bash
# Clone the repository
git clone https://github.com/aalllq/perplexity-ai.git
cd perplexity-ai

# Install dependencies
pip install -r requirements.txt
```

## Option 1: Using as OpenAI-Compatible API Server

### Start the Server

```bash
# Simple start
python api_server.py

# Or use the convenience script
./start_server.sh

# Or with Docker
docker-compose up
```

### Use with OpenAI Client

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8000/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="perplexity-auto",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

### Test with cURL

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "perplexity-auto",
    "messages": [{"role": "user", "content": "What is AI?"}]
  }'
```

## Option 2: Using as LiteLLM Module

### Direct Usage

```python
import perplexity

# Use as standard LiteLLM client
client = perplexity.LiteLLMClient(model="gpt-3.5-turbo")

response = client.search(
    query="What is Python?",
    stream=False
)

print(response['text'])
```

### Register as LiteLLM Provider

```python
from perplexity import register_perplexity_provider
import litellm

# Register Perplexity
register_perplexity_provider()

# Use through LiteLLM
response = litellm.completion(
    model="perplexity-auto",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

## Option 3: Use with LiteLLM Proxy

### Step 1: Start Perplexity API Server

```bash
python api_server.py --port 8000
```

### Step 2: Start LiteLLM Proxy

```bash
litellm --config litellm_proxy_config.yaml
```

### Step 3: Use the Proxy

```python
import litellm

response = litellm.completion(
    model="perplexity/auto",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## Configuration

### Environment Variables

```bash
# API Server Backend
export PERPLEXITY_BACKEND=perplexity  # or litellm, or openai

# API Keys (for litellm/openai backends)
export OPENAI_API_KEY=sk-your-key
export ANTHROPIC_API_KEY=sk-ant-your-key
export COHERE_API_KEY=your-key
```

### Using .env File

```bash
# Copy the example
cp .env.example .env

# Edit .env and add your API keys
nano .env
```

## Available Backends

### 1. Perplexity (Default)
- Direct access to Perplexity AI
- Models: perplexity-auto, perplexity-pro, perplexity-reasoning

### 2. LiteLLM
- Access to 100+ LLM providers
- Models: gpt-3.5-turbo, gpt-4, claude-3-sonnet, etc.

### 3. OpenAI
- Direct OpenAI API access
- Models: gpt-3.5-turbo, gpt-4, gpt-4-turbo

## Docker Deployment

### Using Docker Compose

```bash
# Start the service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the service
docker-compose down
```

### Using Docker Directly

```bash
# Build
docker build -t perplexity-api .

# Run
docker run -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-key \
  -e PERPLEXITY_BACKEND=litellm \
  perplexity-api
```

## Integration Examples

### LangChain

```python
from langchain.chat_models import ChatOpenAI

chat = ChatOpenAI(
    openai_api_base="http://localhost:8000/v1",
    openai_api_key="not-needed",
    model_name="perplexity-auto"
)

response = chat.predict("What is LangChain?")
print(response)
```

### LlamaIndex

```python
from llama_index.llms import OpenAI

llm = OpenAI(
    api_base="http://localhost:8000/v1",
    api_key="not-needed",
    model="perplexity-auto"
)

response = llm.complete("What is LlamaIndex?")
print(response)
```

## Examples

Run the provided example scripts:

```bash
# OpenAI API examples
python examples_openai_sync.py
python examples_openai_async.py

# LiteLLM examples
python examples_litellm_sync.py
python examples_litellm_async.py

# API server client example
python example_api_server_client.py
```

## Troubleshooting

### Server won't start
- Check if port 8000 is already in use
- Install dependencies: `pip install -r requirements.txt`
- Check logs for specific error messages

### Cannot connect to server
- Verify server is running: `curl http://localhost:8000/health`
- Check firewall settings
- Try using 127.0.0.1 instead of localhost

### API key errors
- Ensure environment variables are set correctly
- Check .env file is in the correct location
- For local Perplexity backend, API key is not required

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Explore the [examples](.) directory
- Check out the [API server code](api_server.py) for customization
- Join the discussion on GitHub

## Support

For issues, questions, or contributions, please visit:
https://github.com/aalllq/perplexity-ai
