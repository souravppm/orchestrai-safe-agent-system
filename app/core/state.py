import redis
import os
import json

# Redis Connection
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def save_pending_action(session_id: str, action_data: dict):
    # ৫ মিনিটের জন্য অ্যাকশনটা মেমরিতে সেভ থাকবে (300 seconds)
    redis_client.setex(f"pending_{session_id}", 300, json.dumps(action_data))

def get_pending_action(session_id: str):
    data = redis_client.get(f"pending_{session_id}")
    return json.loads(data) if data else None

def clear_pending_action(session_id: str):
    redis_client.delete(f"pending_{session_id}")
