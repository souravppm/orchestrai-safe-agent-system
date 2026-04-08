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
    },
    {
        "type": "function",
        "function": {
            "name": "refund_order",
            "description": "Initiate a refund for an order. Requires order_id.",
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

# নতুন System Prompt যা এজেন্টকে মাল্টি-স্টেপ লজিক শেখাবে
SYSTEM_PROMPT = """You are OrchestrAI, a safe and logical backend operations agent.
CRITICAL RULES:
1. DO NOT hallucinate data. Ask the user if order ID is missing.
2. MULTI-STEP REASONING: If a user has a conditional request (e.g., "If my order is delayed, refund it"), you MUST FIRST call `get_order_status` to observe the state.
3. Analyze the tool response. If the status justifies a refund (e.g., it's 'Pending' or 'Shipped'), then call `refund_order`. If it's 'Delivered', explain to the user why a refund cannot be processed immediately."""

def get_llm_decision(messages: list):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )
    return response.choices[0].message
