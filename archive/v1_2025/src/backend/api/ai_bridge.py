#!/usr/bin/env python3
"""
ELWOSA AI Bridge Service
========================

Multi-model AI integration service supporting OpenAI, Ollama, and Claude.
Provides unified interface for various AI models with streaming support.

Features:
- Multiple AI provider support
- Streaming responses
- Context management
- Load balancing
- Model selection logic
"""

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, AsyncGenerator
import asyncio
import aiohttp
import json
import os
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="ELWOSA AI Bridge Service",
    description="Unified AI model integration with multi-provider support",
    version="1.0.0",
)

# Model configuration
MODEL_CONFIG = {
    "openai": {
        "endpoint": "https://api.openai.com/v1/chat/completions",
        "api_key": os.getenv("OPENAI_API_KEY"),
        "models": ["gpt-4", "gpt-3.5-turbo", "gpt-4-vision-preview"],
        "default": "gpt-4"
    },
    "ollama": {
        "endpoint": os.getenv("OLLAMA_HOST", "http://localhost:11434"),
        "models": ["llama2", "mistral", "codellama", "neural-chat"],
        "default": "llama2"
    },
    "anthropic": {
        "endpoint": "https://api.anthropic.com/v1/messages",
        "api_key": os.getenv("ANTHROPIC_API_KEY"),
        "models": ["claude-3-opus", "claude-3-sonnet", "claude-2.1"],
        "default": "claude-3-sonnet"
    }
}


class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., description="Message role: user, assistant, or system")
    content: str = Field(..., description="Message content")


class ChatRequest(BaseModel):
    """Chat completion request"""
    messages: List[ChatMessage]
    model: Optional[str] = Field(None, description="Specific model to use")
    provider: Optional[str] = Field(None, description="AI provider (openai, ollama, anthropic)")
    temperature: Optional[float] = Field(0.7, ge=0, le=2)
    max_tokens: Optional[int] = Field(None, ge=1)
    stream: Optional[bool] = Field(False, description="Enable streaming response")
    context_id: Optional[str] = Field(None, description="Context session ID")


class ModelInfo(BaseModel):
    """Model information"""
    provider: str
    model: str
    available: bool
    features: List[str]


class AIResponse(BaseModel):
    """Standard AI response"""
    content: str
    model: str
    provider: str
    usage: Optional[Dict[str, int]] = None
    context_id: Optional[str] = None


# Context management
class ContextManager:
    """Manages conversation contexts across sessions"""
    def __init__(self):
        self.contexts: Dict[str, List[ChatMessage]] = {}
    
    def get_context(self, context_id: str) -> List[ChatMessage]:
        return self.contexts.get(context_id, [])
    
    def update_context(self, context_id: str, messages: List[ChatMessage]):
        if context_id not in self.contexts:
            self.contexts[context_id] = []
        self.contexts[context_id].extend(messages)
        # Keep only last 20 messages for memory efficiency
        self.contexts[context_id] = self.contexts[context_id][-20:]
    
    def clear_context(self, context_id: str):
        if context_id in self.contexts:
            del self.contexts[context_id]


context_manager = ContextManager()


# Provider-specific implementations
async def call_openai(messages: List[ChatMessage], **kwargs) -> Dict[str, Any]:
    """Call OpenAI API"""
    headers = {
        "Authorization": f"Bearer {MODEL_CONFIG['openai']['api_key']}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": kwargs.get("model", MODEL_CONFIG["openai"]["default"]),
        "messages": [msg.dict() for msg in messages],
        "temperature": kwargs.get("temperature", 0.7),
        "stream": kwargs.get("stream", False)
    }
    
    if kwargs.get("max_tokens"):
        payload["max_tokens"] = kwargs["max_tokens"]
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            MODEL_CONFIG["openai"]["endpoint"],
            headers=headers,
            json=payload
        ) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=await response.text())
            return await response.json()


async def call_ollama(messages: List[ChatMessage], **kwargs) -> Dict[str, Any]:
    """Call Ollama API"""
    # Convert messages to Ollama format
    prompt = "\n".join([f"{msg.role}: {msg.content}" for msg in messages])
    
    payload = {
        "model": kwargs.get("model", MODEL_CONFIG["ollama"]["default"]),
        "prompt": prompt,
        "stream": kwargs.get("stream", False),
        "options": {
            "temperature": kwargs.get("temperature", 0.7)
        }
    }
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{MODEL_CONFIG['ollama']['endpoint']}/api/generate",
            json=payload
        ) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail="Ollama service unavailable")
            return await response.json()


async def call_anthropic(messages: List[ChatMessage], **kwargs) -> Dict[str, Any]:
    """Call Anthropic Claude API"""
    headers = {
        "x-api-key": MODEL_CONFIG["anthropic"]["api_key"],
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    
    # Convert to Anthropic format
    system_msg = next((msg.content for msg in messages if msg.role == "system"), None)
    user_messages = [msg for msg in messages if msg.role != "system"]
    
    payload = {
        "model": kwargs.get("model", MODEL_CONFIG["anthropic"]["default"]),
        "messages": [{"role": msg.role, "content": msg.content} for msg in user_messages],
        "max_tokens": kwargs.get("max_tokens", 1024),
        "temperature": kwargs.get("temperature", 0.7)
    }
    
    if system_msg:
        payload["system"] = system_msg
    
    async with aiohttp.ClientSession() as session:
        async with session.post(
            MODEL_CONFIG["anthropic"]["endpoint"],
            headers=headers,
            json=payload
        ) as response:
            if response.status != 200:
                raise HTTPException(status_code=response.status, detail=await response.text())
            return await response.json()


# API endpoints
@app.get("/", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "service": "ELWOSA AI Bridge",
        "status": "healthy",
        "version": "1.0.0",
        "providers": list(MODEL_CONFIG.keys()),
        "timestamp": datetime.now().isoformat()
    }


@app.get("/models", response_model=List[ModelInfo], tags=["Models"])
async def list_models():
    """List all available models across providers"""
    models = []
    
    for provider, config in MODEL_CONFIG.items():
        for model in config.get("models", []):
            # Check availability (simplified - in production, actually test endpoints)
            available = bool(config.get("api_key") or provider == "ollama")
            
            features = []
            if "vision" in model:
                features.append("vision")
            if "code" in model:
                features.append("code")
            if provider == "ollama":
                features.append("local")
            
            models.append(ModelInfo(
                provider=provider,
                model=model,
                available=available,
                features=features
            ))
    
    return models


@app.post("/chat", response_model=AIResponse, tags=["Chat"])
async def chat_completion(request: ChatRequest):
    """
    Unified chat completion endpoint.
    Automatically selects the best model based on availability and request.
    """
    # Add context if provided
    if request.context_id:
        context_messages = context_manager.get_context(request.context_id)
        request.messages = context_messages + request.messages
    
    # Determine provider
    provider = request.provider
    if not provider:
        # Auto-select based on availability and features
        if MODEL_CONFIG["openai"].get("api_key"):
            provider = "openai"
        elif "localhost" in MODEL_CONFIG["ollama"]["endpoint"]:
            provider = "ollama"
        elif MODEL_CONFIG["anthropic"].get("api_key"):
            provider = "anthropic"
        else:
            raise HTTPException(status_code=503, detail="No AI providers available")
    
    # Call appropriate provider
    try:
        if provider == "openai":
            response = await call_openai(request.messages, **request.dict())
            content = response["choices"][0]["message"]["content"]
            usage = response.get("usage")
            
        elif provider == "ollama":
            response = await call_ollama(request.messages, **request.dict())
            content = response["response"]
            usage = {"total_tokens": len(content.split())}  # Approximate
            
        elif provider == "anthropic":
            response = await call_anthropic(request.messages, **request.dict())
            content = response["content"][0]["text"]
            usage = response.get("usage")
            
        else:
            raise HTTPException(status_code=400, detail=f"Unknown provider: {provider}")
        
        # Update context if needed
        if request.context_id:
            context_manager.update_context(
                request.context_id,
                request.messages + [ChatMessage(role="assistant", content=content)]
            )
        
        return AIResponse(
            content=content,
            model=request.model or MODEL_CONFIG[provider]["default"],
            provider=provider,
            usage=usage,
            context_id=request.context_id
        )
        
    except Exception as e:
        logger.error(f"AI call failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")


@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for streaming chat"""
    await websocket.accept()
    
    try:
        while True:
            # Receive message
            data = await websocket.receive_json()
            request = ChatRequest(**data)
            
            # Stream response
            async for chunk in stream_ai_response(request):
                await websocket.send_json({
                    "type": "chunk",
                    "content": chunk,
                    "timestamp": datetime.now().isoformat()
                })
            
            # Send completion signal
            await websocket.send_json({
                "type": "complete",
                "timestamp": datetime.now().isoformat()
            })
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close()


async def stream_ai_response(request: ChatRequest) -> AsyncGenerator[str, None]:
    """Stream AI response in chunks"""
    # Simplified streaming - in production, implement proper streaming for each provider
    response = await chat_completion(request)
    
    # Simulate streaming by yielding words
    words = response.content.split()
    for word in words:
        yield word + " "
        await asyncio.sleep(0.05)  # Simulate streaming delay


@app.delete("/context/{context_id}", tags=["Context"])
async def clear_context(context_id: str):
    """Clear a specific context session"""
    context_manager.clear_context(context_id)
    return {"message": f"Context {context_id} cleared"}


@app.get("/status", tags=["Status"])
async def get_service_status():
    """Get detailed service status"""
    status = {
        "service": "ELWOSA AI Bridge",
        "timestamp": datetime.now().isoformat(),
        "providers": {}
    }
    
    for provider, config in MODEL_CONFIG.items():
        status["providers"][provider] = {
            "configured": bool(config.get("api_key") or provider == "ollama"),
            "endpoint": config["endpoint"],
            "models": config["models"],
            "default_model": config["default"]
        }
    
    status["active_contexts"] = len(context_manager.contexts)
    
    return status


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8006, log_level="info")