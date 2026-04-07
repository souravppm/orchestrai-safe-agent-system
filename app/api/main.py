from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="OrchestrAI API", description="Safe AI Agent System")

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"

class ChatResponse(BaseModel):
    response: str
    status: str

@app.get("/")
async def root():
    return {"message": "Welcome to OrchestrAI API. The server is running."}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Basic /chat endpoint for the request/response flow.
    Currently returns a static acknowledgment.
    """
    user_message = request.message
    
    # TODO: Connect with the orchestrator layer
    
    return ChatResponse(
        response=f"Received: '{user_message}'. This is a placeholder response.",
        status="success"
    )
