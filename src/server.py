import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.orchestrator_groq import run_omni_query

app = FastAPI(title="Omni-Retail Enterprise API")

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    message: str
    session_id: str = "default-session"

@app.post("/api/chat")
async def chat_endpoint(request: QueryRequest):
    print(f"Received query: {request.message}")
    answer, thoughts = run_omni_query(request.message)
    return {
        "response": answer,
        "thought_process": thoughts
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
