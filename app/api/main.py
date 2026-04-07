from fastapi import FastAPI
from pydantic import BaseModel
import json
from app.services.llm_service import extract_intent
from app.orchestrator.engine import run_agent

app = FastAPI(title="OrchestrAI API", description="Safe AI Agent System")

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"

@app.get("/")
async def root():
    return {"message": "Welcome to OrchestrAI API. The server is running."}

@app.post("/chat")
def chat(request: ChatRequest):
    user_message = request.message

    # Step 1: Brain (LLM) extracts intent
    llm_output = extract_intent(user_message)

    # Step 2: Parse and Validate Brain output
    try:
        # Sometimes LLM might wrap JSON in backticks, but our service usually handles it
        # If not, we might need a cleanup, but for now simple loads works
        intent_data = json.loads(llm_output)
    except:
        return {"error": "Invalid LLM response", "raw": llm_output}

    # Step 3: Orchestrator executes based on intent
    result = run_agent(intent_data)

    return {
        "intent": intent_data,
        "result": result
    }
