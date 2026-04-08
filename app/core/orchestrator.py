import json
from sqlalchemy.orm import Session
from app.agent.llm import get_llm_decision
from app.services.tools import get_order_status, cancel_order
from app.db.models import AuditLog
from app.schema.schemas import UserRequest

def process_user_request(db: Session, request: UserRequest):
    user_query = request.query.lower()

    # 1. Check if this is a response to a pending confirmation
    if request.pending_action:
        if user_query in ["yes", "y", "confirm", "sure"]:
            # ইউজার কনফার্ম করেছে, এবার এক্সিকিউট কর
            function_name = request.pending_action.action
            arguments = request.pending_action.args
            
            action_result = None
            if function_name == "cancel_order":
                action_result = cancel_order(db, arguments.get("order_id"))
            
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
            return {"status": "aborted", "message": "Action cancelled by user."}

    # 2. Get decision from LLM (Normal Flow)
    llm_response = get_llm_decision(request.query)

    # 3. Check if LLM decided to call a tool
    if llm_response.tool_calls:
        tool_call = llm_response.tool_calls[0]
        function_name = tool_call.function.name
        arguments = json.loads(tool_call.function.arguments)

        # 4. SAFETY CHECK: Sensitive actions require confirmation
        SENSITIVE_TOOLS = ["cancel_order", "refund_order"]
        
        if function_name in SENSITIVE_TOOLS:
            return {
                "status": "confirmation_required",
                "message": f"Are you sure you want to {function_name.replace('_', ' ')} for order {arguments.get('order_id')}?",
                "pending_action": {
                    "action": function_name,
                    "args": arguments
                }
            }

        # 5. Non-sensitive tools (like get_order_status) execute immediately
        action_result = None
        if function_name == "get_order_status":
            action_result = get_order_status(db, arguments.get("order_id"))
        else:
            action_result = {"error": "Unauthorized tool."}

        # Save Audit Log
        log_entry = AuditLog(
            user_input=request.query,
            llm_decision=f"Tool: {function_name}, Args: {arguments}",
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
        # LLM just replied with text
        return {"status": "chat", "message": llm_response.content}
