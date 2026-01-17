from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys
from dotenv import load_dotenv

# Load .env file immediately
load_dotenv()

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src.orchestrator_groq import run_omni_query

app = FastAPI(title="Omni-Retail Groq API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class ChatResponse(BaseModel):
    response: str
    thought_process: List[str]

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(req: ChatRequest):
    print(f"Starting Groq Orchestrator for query: {req.message}")
    
    try:
        final_answer, thoughts = run_omni_query(req.message)
        
        return ChatResponse(
            response=final_answer,
            thought_process=thoughts
        )
        
    except Exception as e:
        print(f"Error: {e}")
        return ChatResponse(response=f"Error executing Groq: {str(e)}", thought_process=["Error encountered."])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
