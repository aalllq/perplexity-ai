"""
OpenAI-compatible API Server for Perplexity AI
This server provides an OpenAI-compatible REST API interface that can be used with any OpenAI client.
"""

import os
import json
import time
import uuid
from typing import Optional, List, Dict, Any
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Import perplexity clients
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import perplexity
import perplexity_async


# Pydantic models for OpenAI-compatible API
class Message(BaseModel):
    role: str
    content: str


class ChatCompletionRequest(BaseModel):
    model: str = Field(default="perplexity-default", description="Model to use")
    messages: List[Message]
    temperature: Optional[float] = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(default=None, ge=1)
    stream: Optional[bool] = Field(default=False)
    top_p: Optional[float] = Field(default=1.0, ge=0.0, le=1.0)
    n: Optional[int] = Field(default=1, ge=1, le=1)
    stop: Optional[List[str]] = None
    presence_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    frequency_penalty: Optional[float] = Field(default=0.0, ge=-2.0, le=2.0)
    user: Optional[str] = None


class CompletionUsage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class CompletionChoice(BaseModel):
    index: int
    message: Message
    finish_reason: str


class ChatCompletionResponse(BaseModel):
    id: str
    object: str = "chat.completion"
    created: int
    model: str
    choices: List[CompletionChoice]
    usage: CompletionUsage


# Initialize FastAPI app
app = FastAPI(
    title="Perplexity AI - OpenAI Compatible API",
    description="OpenAI-compatible API server for Perplexity AI with LiteLLM and OpenAI support",
    version="1.0.0"
)


# Global configuration
class ServerConfig:
    def __init__(self):
        self.backend = os.environ.get("PERPLEXITY_BACKEND", "perplexity")  # perplexity, litellm, or openai
        self.perplexity_cookies = {}
        self.api_key = os.environ.get("OPENAI_API_KEY", "")
        
    def get_client(self, backend: Optional[str] = None):
        """Get the appropriate client based on backend selection."""
        backend = backend or self.backend
        
        if backend == "litellm":
            return perplexity.LiteLLMClient(api_key=self.api_key)
        elif backend == "openai":
            return perplexity.OpenAIClient(api_key=self.api_key)
        else:  # perplexity (default)
            return perplexity.Client(cookies=self.perplexity_cookies)


config = ServerConfig()


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Perplexity AI - OpenAI Compatible API Server",
        "version": "1.0.0",
        "backends": ["perplexity", "litellm", "openai"],
        "current_backend": config.backend,
        "endpoints": {
            "chat_completions": "/v1/chat/completions",
            "models": "/v1/models",
            "health": "/health"
        }
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok", "backend": config.backend}


@app.get("/v1/models")
async def list_models():
    """List available models (OpenAI-compatible endpoint)."""
    models = []
    
    if config.backend == "perplexity":
        models = [
            {"id": "perplexity-auto", "object": "model", "created": int(time.time()), "owned_by": "perplexity"},
            {"id": "perplexity-pro", "object": "model", "created": int(time.time()), "owned_by": "perplexity"},
            {"id": "perplexity-reasoning", "object": "model", "created": int(time.time()), "owned_by": "perplexity"},
            {"id": "perplexity-labs-r1", "object": "model", "created": int(time.time()), "owned_by": "perplexity-labs"},
        ]
    elif config.backend == "litellm":
        models = [
            {"id": "gpt-3.5-turbo", "object": "model", "created": int(time.time()), "owned_by": "openai"},
            {"id": "gpt-4", "object": "model", "created": int(time.time()), "owned_by": "openai"},
            {"id": "claude-3-sonnet-20240229", "object": "model", "created": int(time.time()), "owned_by": "anthropic"},
        ]
    else:  # openai
        models = [
            {"id": "gpt-3.5-turbo", "object": "model", "created": int(time.time()), "owned_by": "openai"},
            {"id": "gpt-4", "object": "model", "created": int(time.time()), "owned_by": "openai"},
            {"id": "gpt-4-turbo", "object": "model", "created": int(time.time()), "owned_by": "openai"},
        ]
    
    return {"object": "list", "data": models}


@app.post("/v1/chat/completions")
async def chat_completions(request: ChatCompletionRequest):
    """
    Create a chat completion (OpenAI-compatible endpoint).
    Supports both streaming and non-streaming responses.
    """
    try:
        # Extract messages
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        # Determine which backend to use
        backend = config.backend
        model = request.model
        
        # Override backend based on model prefix
        if model.startswith("perplexity-"):
            backend = "perplexity"
        elif model.startswith("gpt-") or model.startswith("o1-"):
            backend = "openai"
        
        # Handle streaming response
        if request.stream:
            return StreamingResponse(
                stream_chat_completion(messages, request, backend, model),
                media_type="text/event-stream"
            )
        
        # Handle non-streaming response
        return await generate_chat_completion(messages, request, backend, model)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def generate_chat_completion(messages: List[Dict], request: ChatCompletionRequest, backend: str, model: str):
    """Generate a non-streaming chat completion."""
    try:
        response_text = ""
        
        if backend == "perplexity":
            # Use Perplexity client
            client = perplexity.Client(cookies=config.perplexity_cookies)
            
            # Extract the user query (last message)
            query = messages[-1]["content"]
            
            # Determine mode based on model
            mode = "auto"
            if "pro" in model:
                mode = "pro"
            elif "reasoning" in model:
                mode = "reasoning"
            
            response = client.search(query=query, mode=mode, stream=False)
            response_text = response.get("text", "") if isinstance(response, dict) else str(response)
            
        elif backend == "litellm":
            # Use LiteLLM client
            client = perplexity.LiteLLMClient(model=model if not model.startswith("perplexity-") else "gpt-3.5-turbo")
            response = client.chat(
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            response_text = response["text"]
            
        else:  # openai
            # Use OpenAI client
            client = perplexity.OpenAIClient(model=model if not model.startswith("perplexity-") else "gpt-3.5-turbo")
            response = client.chat(
                messages=messages,
                temperature=request.temperature,
                max_tokens=request.max_tokens
            )
            response_text = response["text"]
        
        # Create OpenAI-compatible response
        completion_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"
        
        return ChatCompletionResponse(
            id=completion_id,
            object="chat.completion",
            created=int(time.time()),
            model=model,
            choices=[
                CompletionChoice(
                    index=0,
                    message=Message(role="assistant", content=response_text),
                    finish_reason="stop"
                )
            ],
            usage=CompletionUsage(
                prompt_tokens=sum(len(m["content"].split()) for m in messages),
                completion_tokens=len(response_text.split()),
                total_tokens=sum(len(m["content"].split()) for m in messages) + len(response_text.split())
            )
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating completion: {str(e)}")


async def stream_chat_completion(messages: List[Dict], request: ChatCompletionRequest, backend: str, model: str):
    """Stream a chat completion response."""
    completion_id = f"chatcmpl-{uuid.uuid4().hex[:8]}"
    created = int(time.time())
    
    try:
        if backend == "perplexity":
            # Use Perplexity client (note: may not support streaming in all modes)
            client = perplexity.Client(cookies=config.perplexity_cookies)
            query = messages[-1]["content"]
            
            mode = "auto"
            if "pro" in model:
                mode = "pro"
            elif "reasoning" in model:
                mode = "reasoning"
            
            # Try to stream if supported
            try:
                for chunk in client.search(query=query, mode=mode, stream=True):
                    text = chunk.get("text", "") if isinstance(chunk, dict) else str(chunk)
                    if text:
                        yield f"data: {json.dumps({'id': completion_id, 'object': 'chat.completion.chunk', 'created': created, 'model': model, 'choices': [{'index': 0, 'delta': {'content': text}, 'finish_reason': None}]})}\n\n"
            except:
                # Fallback to non-streaming
                response = client.search(query=query, mode=mode, stream=False)
                text = response.get("text", "") if isinstance(response, dict) else str(response)
                yield f"data: {json.dumps({'id': completion_id, 'object': 'chat.completion.chunk', 'created': created, 'model': model, 'choices': [{'index': 0, 'delta': {'content': text}, 'finish_reason': 'stop'}]})}\n\n"
            
        elif backend == "litellm":
            client = perplexity.LiteLLMClient(model=model if not model.startswith("perplexity-") else "gpt-3.5-turbo")
            for chunk in client.chat(messages=messages, temperature=request.temperature, max_tokens=request.max_tokens, stream=True):
                text = chunk.get("text", "")
                if text:
                    yield f"data: {json.dumps({'id': completion_id, 'object': 'chat.completion.chunk', 'created': created, 'model': model, 'choices': [{'index': 0, 'delta': {'content': text}, 'finish_reason': None}]})}\n\n"
        
        else:  # openai
            client = perplexity.OpenAIClient(model=model if not model.startswith("perplexity-") else "gpt-3.5-turbo")
            for chunk in client.chat(messages=messages, temperature=request.temperature, max_tokens=request.max_tokens, stream=True):
                text = chunk.get("text", "")
                if text:
                    yield f"data: {json.dumps({'id': completion_id, 'object': 'chat.completion.chunk', 'created': created, 'model': model, 'choices': [{'index': 0, 'delta': {'content': text}, 'finish_reason': None}]})}\n\n"
        
        # Send final chunk
        yield f"data: {json.dumps({'id': completion_id, 'object': 'chat.completion.chunk', 'created': created, 'model': model, 'choices': [{'index': 0, 'delta': {}, 'finish_reason': 'stop'}]})}\n\n"
        yield "data: [DONE]\n\n"
        
    except Exception as e:
        error_msg = f"Error streaming completion: {str(e)}"
        yield f"data: {json.dumps({'error': {'message': error_msg, 'type': 'server_error'}})}\n\n"


def main():
    """Start the API server."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Perplexity AI - OpenAI Compatible API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to (default: 8000)")
    parser.add_argument("--backend", choices=["perplexity", "litellm", "openai"], 
                       default="perplexity", help="Backend to use (default: perplexity)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    
    args = parser.parse_args()
    
    # Set backend
    config.backend = args.backend
    
    print(f"""
╔════════════════════════════════════════════════════════════════╗
║   Perplexity AI - OpenAI Compatible API Server                ║
╚════════════════════════════════════════════════════════════════╝

Backend: {args.backend}
Host: {args.host}
Port: {args.port}

OpenAI Compatible Endpoints:
  - POST http://{args.host}:{args.port}/v1/chat/completions
  - GET  http://{args.host}:{args.port}/v1/models

Usage with OpenAI Python client:
  from openai import OpenAI
  client = OpenAI(
      base_url="http://{args.host}:{args.port}/v1",
      api_key="not-needed"
  )
  
  response = client.chat.completions.create(
      model="perplexity-auto",
      messages=[{{"role": "user", "content": "Hello!"}}]
  )

Press CTRL+C to stop the server.
""")
    
    uvicorn.run(
        "api_server:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level="info"
    )


if __name__ == "__main__":
    main()
