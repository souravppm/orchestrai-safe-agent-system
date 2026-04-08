from pydantic import BaseModel
from typing import Optional, Dict, Any

# কনফার্মেশনের জন্য পেন্ডিং অ্যাকশন স্কিমা
class PendingAction(BaseModel):
    action: str
    args: Dict[str, Any]

# ইউজারের ইনপুট ভ্যালিডেশন
class UserRequest(BaseModel):
    query: str
    session_id: str = "default_session"

# টুলের আউটপুট ভ্যালিডেশন
class OrderResponse(BaseModel):
    order_id: int
    status: str
    message: Optional[str] = None
