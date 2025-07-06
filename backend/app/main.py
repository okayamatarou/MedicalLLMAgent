from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import json
import logging
from .config import config_manager
from .services.llm_service import llm_service
from .services.session_service import session_service
from .utils.emotion_parser import parse_emotion_status, get_default_emotion_status

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="遺伝カウンセリング教育システム",
    description="ローカルLLMを使用した遺伝カウンセリング教育システム",
    version="1.0.0"
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    session_id: str
    message: str
    stream: bool = False

class SessionCreateRequest(BaseModel):
    user_id: str
    prompt_config: str = "default_patient"
    model_name: str = "llama2"

class ConfigUpdateRequest(BaseModel):
    overrides: Dict[str, Any]

class ModelSwitchRequest(BaseModel):
    model_name: str

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.get("/")
def read_root():
    return {
        "message": "遺伝カウンセリング教育システム API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    try:
        model_healthy = await llm_service.health_check()
        return {
            "status": "healthy" if model_healthy else "degraded",
            "model_status": "healthy" if model_healthy else "unhealthy",
            "model_info": llm_service.get_model_info()
        }
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return {
            "status": "degraded",
            "model_status": "error",
            "error": str(e)
        }

@app.get("/config")
def get_config():
    """Get current configuration"""
    from omegaconf import OmegaConf
    config = config_manager.get_config()
    
    config_dict = OmegaConf.to_container(config, resolve=True)
    
    return {
        "config": config_dict,
        "available_models": config_manager.get_available_models(),
        "available_prompts": config_manager.get_available_prompts(),
        "available_ui_configs": config_manager.get_available_ui_configs()
    }

@app.post("/config/update")
def update_config(request: ConfigUpdateRequest):
    """Update configuration"""
    try:
        new_config = config_manager.update_config(request.overrides)
        return {"status": "success", "config": new_config}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/models")
def get_available_models():
    """Get available models"""
    return {
        "models": llm_service.get_available_models(),
        "current_model": llm_service.get_model_info()
    }

@app.post("/models/switch")
async def switch_model(request: ModelSwitchRequest):
    """Switch to a different model"""
    success = await llm_service.switch_model(request.model_name)
    if success:
        return {
            "status": "success",
            "model_info": llm_service.get_model_info()
        }
    else:
        raise HTTPException(status_code=400, detail="Failed to switch model")

@app.post("/sessions")
def create_session(request: SessionCreateRequest):
    """Create a new counseling session"""
    try:
        logger.info(f"Creating session for user: {request.user_id}, prompt: {request.prompt_config}, model: {request.model_name}")
        
        session_id = session_service.create_session(
            request.user_id,
            request.prompt_config,
            request.model_name
        )
        logger.info(f"Session created with ID: {session_id}")
        
        config = config_manager.get_config()
        logger.info(f"Config loaded: {type(config)}")
        logger.info(f"Config prompt: {config.prompt if hasattr(config, 'prompt') else 'NO PROMPT'}")
        
        if hasattr(config, 'prompt') and hasattr(config.prompt, 'prompt') and hasattr(config.prompt.prompt, 'system_prompt'):
            system_prompt = config.prompt.prompt.system_prompt
            logger.info(f"System prompt found: {len(system_prompt)} characters")
        else:
            logger.error(f"System prompt not found in config structure")
            logger.error(f"Config structure: {config}")
            system_prompt = "You are a helpful assistant for genetic counseling education."
        
        session_service.add_message(session_id, "system", system_prompt)
        logger.info(f"System message added to session")
        
        return {
            "session_id": session_id,
            "status": "created"
        }
    except Exception as e:
        logger.error(f"Session creation error: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sessions/{session_id}")
def get_session(session_id: str):
    """Get session information"""
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session

@app.get("/sessions/{session_id}/messages")
def get_session_messages(session_id: str):
    """Get session messages"""
    messages = session_service.get_messages(session_id)
    return {"messages": messages}

@app.delete("/sessions/{session_id}")
def end_session(session_id: str):
    """End a counseling session"""
    try:
        session_service.end_session(session_id)
        return {"status": "ended"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users/{user_id}/sessions")
def get_user_sessions(user_id: str):
    """Get all sessions for a user"""
    sessions = session_service.get_user_sessions(user_id)
    return {"sessions": sessions}

@app.post("/chat")
async def chat(request: ChatRequest):
    """Send a message and get response"""
    try:
        session = session_service.get_session(request.session_id)
        if not session:
            raise HTTPException(status_code=404, detail="Session not found")
        
        session_service.add_message(request.session_id, "user", request.message)
        
        messages = session_service.get_messages(request.session_id)
        
        llm_messages = []
        for msg in messages:
            if msg["role"] in ["system", "user", "assistant"]:
                llm_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        if request.stream:
            async def generate():
                response_content = ""
                async for chunk in await llm_service.generate_response(llm_messages, stream=True):
                    response_content += chunk
                    yield f"data: {json.dumps({'chunk': chunk})}\n\n"
                
                session_service.add_message(request.session_id, "assistant", response_content)
                yield f"data: {json.dumps({'done': True})}\n\n"
            
            return StreamingResponse(generate(), media_type="text/plain")
        else:
            response = await llm_service.generate_response(llm_messages, stream=False)
            
            cleaned_response, emotion_status = parse_emotion_status(response)
            
            metadata = {"emotion_status": emotion_status} if emotion_status else {}
            session_service.add_message(request.session_id, "assistant", cleaned_response, metadata)
            
            return {
                "response": cleaned_response,
                "emotion_status": emotion_status
            }
            
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/{session_id}")
async def websocket_endpoint(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    try:
        session = session_service.get_session(session_id)
        if not session:
            await websocket.send_text(json.dumps({"error": "Session not found"}))
            await websocket.close()
            return
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "chat":
                user_message = message_data.get("message", "")
                
                session_service.add_message(session_id, "user", user_message)
                
                messages = session_service.get_messages(session_id)
                
                llm_messages = []
                for msg in messages:
                    if msg["role"] in ["system", "user", "assistant"]:
                        llm_messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
                
                response_content = ""
                async for chunk in await llm_service.generate_response(llm_messages, stream=True):
                    response_content += chunk
                    await websocket.send_text(json.dumps({
                        "type": "chunk",
                        "content": chunk
                    }))
                
                cleaned_response, emotion_status = parse_emotion_status(response_content)
                
                metadata = {"emotion_status": emotion_status} if emotion_status else {}
                session_service.add_message(session_id, "assistant", cleaned_response, metadata)
                
                await websocket.send_text(json.dumps({
                    "type": "complete",
                    "full_response": cleaned_response,
                    "emotion_status": emotion_status
                }))
                
    except WebSocketDisconnect:
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await websocket.send_text(json.dumps({"error": str(e)}))

@app.get("/prompts")
def get_available_prompts():
    """Get available prompt configurations"""
    return {
        "prompts": config_manager.get_available_prompts(),
        "current_prompt": config_manager.get_config().prompt.name
    }

@app.get("/ui-configs")
def get_ui_configs():
    """Get available UI configurations"""
    return {
        "ui_configs": config_manager.get_available_ui_configs(),
        "current_ui": config_manager.get_config().ui.name
    }

@app.on_event("startup")
async def startup_event():
    """Startup tasks"""
    logger.info("Starting 遺伝カウンセリング教育システム")
    
    try:
        model_healthy = await llm_service.health_check()
        if model_healthy:
            logger.info("LLM model is healthy and ready")
        else:
            logger.warning("LLM model health check failed")
    except Exception as e:
        logger.error(f"Failed to check model health: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown tasks"""
    logger.info("Shutting down 遺伝カウンセリング教育システム")
    
    session_service.cleanup_expired_sessions()
