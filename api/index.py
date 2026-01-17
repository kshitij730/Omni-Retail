import os
import sys
from fastapi import FastAPI
from pydantic import BaseModel

# Add current directory to path so 'src' can be found in Vercel
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.orchestrator_groq import run_omni_query

app = FastAPI()

class QueryRequest(BaseModel):
    message: str
    session_id: str = "default-session"

@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest):
    answer, thoughts = run_omni_query(request.message)
    return {
        "response": answer,
        "thought_process": thoughts
    }

@app.get("/")
async def health_check():
    return {"status": "Omni-Agent API is live"}
