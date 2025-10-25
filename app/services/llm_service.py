from langchain.llms import Ollama
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
import os
import requests
import time
from typing import Dict, Optional

# Get Ollama host from environment variable or use default for Docker
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://ollama:11434')
MODEL_NAME = "llama3"  # Using the customized llama3 model

def wait_for_ollama(timeout: int = 300, check_interval: int = 10) -> bool:
    """
    Wait for Ollama service to be ready and have the model loaded
    
    Args:
        timeout (int): Maximum time to wait in seconds
        check_interval (int): Time between checks in seconds
        
    Returns:
        bool: True if Ollama is ready with model, False otherwise
    """
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            health = check_ollama_health()
            if health["status"] == "healthy" and health.get("model_ready", False):
                return True
        except Exception:
            pass
        time.sleep(check_interval)
    return False

def check_ollama_health() -> Dict[str, any]:
    """
    Check if Ollama service is healthy and responsive
    """
    try:
        # Check basic service health
        response = requests.get(f"{OLLAMA_HOST}/api/tags")
        if response.status_code != 200:
            return {
                "status": "unhealthy",
                "error": f"Status code: {response.status_code}",
                "model_ready": False
            }
            
        # Check if our model is loaded
        models = response.json().get("models", [])
        model_loaded = any(model.get("name") == MODEL_NAME for model in models)
        
        return {
            "status": "healthy",
            "models": len(models),
            "model_ready": model_loaded,
            "target_model": MODEL_NAME
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "error": str(e),
            "model_ready": False
        }

# Initialize the Ollama LLM with the llama2 model (will be upgraded to llama3)
llm = Ollama(
    model="llama3",
    base_url=OLLAMA_HOST,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

def get_llm_response(message: str) -> str:
    """
    Get a response from the LLM for the given message.
    
    Args:
        message (str): The input message to send to the LLM
        
    Returns:
        str: The LLM's response
    """
    try:
        # Send the message to the LLM and get the response
        response = llm(message)
        return response.strip()
    except Exception as e:
        print("Exception in get_llm_response:", e)
        raise Exception(f"Error getting LLM response: {str(e)}")