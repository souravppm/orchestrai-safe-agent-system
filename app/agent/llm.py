import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API Key from .env
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define our tools schema for the LLM
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_status",
            "description": "Check the current status of an order using order_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer", "description": "The ID of the order"}
                },
                "required": ["order_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cancel_order",
            "description": "Cancel an order. Requires order_id.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {"type": "integer", "description": "The ID of the order"}
                },
                "required": ["order_id"]
            }
        }
    }
]

def get_llm_decision(user_query: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",  # Cheap and highly reliable for tool calling
        messages=[
            {"role": "system", "content": "You are OrchestrAI, a safe backend operations agent. Your job is to map user requests to the provided tools. Do NOT hallucinate data. If you don't know the order ID, ask for it."},
            {"role": "user", "content": user_query}
        ],
        tools=TOOLS,
        tool_choice="auto"
    )
    return response.choices[0].message
