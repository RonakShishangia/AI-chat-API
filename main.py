from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import chat_router
from app.services.llm_service import check_ollama_health

app = FastAPI(
    title="LangChain Ollama Demo",
    description="A demo API showing LangChain integration with Ollama",
    version="1.0.0"
)

@app.get("/health")
async def health_check():
    """
    Health check endpoint to verify API and Ollama service status
    Returns detailed health information including model status
    """
    try:
        # Check Ollama connection
        ollama_status = check_ollama_health()
        
        # Determine overall status
        is_healthy = (
            ollama_status["status"] == "healthy" and 
            ollama_status.get("model_ready", False)
        )
        
        return {
            "status": "healthy" if is_healthy else "unhealthy",
            "api": {
                "status": "running",
                "version": "1.0.0"
            },
            "ollama": ollama_status
        }
    except Exception as e:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "unhealthy",
                "error": str(e),
                "api": {
                    "status": "running",
                    "error": "Failed to connect to Ollama service"
                }
            }
        )

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat_router.router, prefix="/api/v1", tags=["chat"])