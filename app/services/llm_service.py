import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def extract_intent(message: str):
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """
You are an AI that extracts structured intent from user input.

Return ONLY JSON.
No explanation.

Format:
{
  "intent": "...",
  "entities": {
    "order_id": "..."
  }
}
"""
            },
            {
                "role": "user",
                "content": message
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content
