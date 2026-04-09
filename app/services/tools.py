from sqlalchemy.orm import Session
from app.db.models import Order

def get_order_status(db: Session, order_id: int) -> dict:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return {"error": f"Order {order_id} not found in system."}
    return {"order_id": order.id, "status": order.status, "item": order.item_name}

def cancel_order(db: Session, order_id: int) -> dict:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return {"error": f"Order {order_id} not found."}
    
    # নতুন চেক: যদি আগে থেকেই ক্যানসেলড থাকে
    if order.status == "Cancelled":
        return {"error": f"Action Denied: Order {order_id} is already cancelled."}

    # আগের চেক: Shipped order cancel করা যাবে না
    if order.status == "Shipped":
        return {"error": "Action Denied: Cannot cancel an order that is already shipped."}
    
    # Cancellation execution
    order.status = "Cancelled"
    db.commit()
    return {"message": f"Order {order_id} successfully cancelled.", "status": "Cancelled"}

def refund_order(db: Session, order_id: int) -> dict:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return {"error": f"Order {order_id} not found."}
    
    # Business Logic / Safety Check
    if order.status == "Delivered":
        return {"error": "Action Denied: Cannot refund a delivered order directly. Please initiate a return first."}
    if order.status == "Refunded":
        return {"error": "Order is already refunded."}
    
    # Refund execution
    order.status = "Refunded"
    db.commit()
    return {"message": f"Refund processed successfully for order {order_id}.", "status": "Refunded"}
