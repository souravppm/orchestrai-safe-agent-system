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

# নতুন System Prompt যা এজেন্টকে Idempotency এবং Safety শেখাবে
SYSTEM_PROMPT = """You are OrchestrAI, a safe and logical backend operations agent.
CRITICAL RULES:
1. DO NOT hallucinate data. Ask the user if order ID is missing.
2. ALWAYS OBSERVE BEFORE ACTING: Before calling `cancel_order` or `refund_order`, you MUST FIRST call `get_order_status` to check the current state of the order.
3. IDEMPOTENCY: Analyze the tool response. If the status is ALREADY 'Cancelled' or 'Refunded', DO NOT call the cancel or refund tools. Instead, politely inform the user that the action was already completed previously.
4. POLICY CHECK: If an order is 'Delivered', explain to the user why a refund cannot be processed directly and refuse the refund action."""

def get_llm_decision(messages: list):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )
    return response.choices[0].message
