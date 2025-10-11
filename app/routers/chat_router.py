from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_service import get_llm_response

router = APIRouter()

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Send a message to the LLM and get a response.
    
    Parameters:
    - message: The input text message to send to the LLM
    
    Returns:
    - response: The LLM's response to the input message
    """
    try:
        response = get_llm_response(request.message)
        return ChatResponse(response=response)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))