# Dummy database (later replace with real DB)

orders_db = {
    "123": {"status": "processing"},
    "456": {"status": "shipped"},
    "789": {"status": "delivered"}
}


def get_order_status(order_id: str):
    order = orders_db.get(order_id)

    if not order:
        return "not_found"

    return order["status"]


def cancel_order(order_id: str):
    if order_id in orders_db:
        orders_db[order_id]["status"] = "cancelled"
        return {"message": f"Order {order_id} cancelled"}

    return {"error": "Order not found"}


def refund_order(order_id: str):
    if order_id in orders_db:
        return {"message": f"Refund initiated for {order_id}"}

    return {"error": "Order not found"}
