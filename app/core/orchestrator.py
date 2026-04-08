import json
from sqlalchemy.orm import Session
from app.agent.llm import get_llm_decision, SYSTEM_PROMPT
from app.services.tools import get_order_status, cancel_order, refund_order
from app.db.models import AuditLog
from app.schema.schemas import UserRequest
from app.core.state import save_pending_action, get_pending_action, clear_pending_action

def process_user_request(db: Session, request: UserRequest):
    user_query = request.query.lower()
    session_id = request.session_id

    # 1. Check if there is a pending action in REDIS
    pending_action = get_pending_action(session_id)
    
    if pending_action:
        if user_query in ["yes", "y", "confirm", "sure"]:
            function_name = pending_action["action"]
            arguments = pending_action["args"]
            
            action_result = None
            if function_name == "cancel_order":
                action_result = cancel_order(db, arguments.get("order_id"))
            elif function_name == "refund_order":
                action_result = refund_order(db, arguments.get("order_id"))
            
            # Action executed, now clear memory
            clear_pending_action(session_id)
            
            # Save Audit Log
            log_entry = AuditLog(
                user_input="User confirmed pending action",
                llm_decision=f"Executed confirmed tool: {function_name}",
                action_taken=str(action_result)
            )
            db.add(log_entry)
            db.commit()

            return {
                "status": "success", 
                "action_taken": function_name, 
                "result": action_result
            }
        else:
            clear_pending_action(session_id)
            return {"status": "aborted", "message": "Action cancelled by user."}

    # 2. Multi-step Agentic Reasoning Loop (Plan -> Act -> Observe -> Decide)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": request.query}
    ]

    MAX_STEPS = 3 # এজেন্টকে নিজে নিজে সর্বোচ্চ ৩ বার ভাবার সুযোগ দিচ্ছি
    for step in range(MAX_STEPS):
        llm_response = get_llm_decision(messages)

        # যদি LLM টুল কল না করে নরমাল টেক্সট দেয় (অর্থাৎ ডিসিশন নেওয়া শেষ)
        if not llm_response.tool_calls:
            return {"status": "chat", "message": llm_response.content}

        tool_call = llm_response.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # 3. SAFETY CHECK: লুপ থামিয়ে ইউজারের পারমিশন নাও (Human-in-the-loop)
        SENSITIVE_TOOLS = ["cancel_order", "refund_order"]
        if function_name in SENSITIVE_TOOLS:
            # Redis-এ সেভ করা হচ্ছে
            save_pending_action(session_id, {"action": function_name, "args": arguments})
            
            return {
                "status": "confirmation_required",
                "message": f"Are you sure you want to {function_name.replace('_', ' ')} for order {arguments.get('order_id')}?"
            }

        # 4. Execute safe tools (Observation phase)
        action_result = None
        if function_name == "get_order_status":
            action_result = get_order_status(db, arguments.get("order_id"))
        else:
            action_result = {"error": "Unauthorized tool."}

        # লুপের ভেতরের স্টেপগুলো ডেটাবেসে লগ করে রাখছি
        log_entry = AuditLog(
            user_input=f"Internal Step {step+1}: System observation",
            llm_decision=f"Tool: {function_name}, Args: {arguments}",
            action_taken=str(action_result)
        )
        db.add(log_entry)
        db.commit()

        # 5. টুলের রেজাল্টটা messages-এ ঢুকিয়ে দাও, যাতে এজেন্ট পরের লুপে এটা পড়ে সিদ্ধান্ত নিতে পারে
        messages.append(llm_response) # এজেন্টের আগের কথাটা মনে রাখার জন্য
        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": function_name,
            "content": json.dumps(action_result)
        })

    return {"status": "error", "message": "Task too complex, reached max reasoning steps"}
