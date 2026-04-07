from app.tools.order_tools import (
    cancel_order,
    get_order_status,
    refund_order
)


def run_agent(intent_data: dict):
    intent = intent_data.get("intent")
    entities = intent_data.get("entities", {})

    order_id = entities.get("order_id")

    # 🧠 Decision layer
    if intent == "cancel_order":
        if not order_id:
            return {"error": "order_id missing"}

        # validation (dummy এখন)
        status = get_order_status(order_id)

        if status == "shipped":
            return {"message": "Cannot cancel shipped order"}

        return cancel_order(order_id)

    elif intent == "get_order_status":
        return get_order_status(order_id)

    elif intent == "refund_order":
        return refund_order(order_id)

    else:
        return {"message": "Unknown intent"}
