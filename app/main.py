from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.db.session import engine, get_db
from app.db.models import Base, Order
from app.schema.schemas import UserRequest
from app.core.orchestrator import process_user_request

# Create DB Tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="OrchestrAI - Safe Agent System")

@app.get("/")
def read_root():
    return {"message": "Welcome to OrchestrAI! System is online."}

@app.post("/seed")
def seed_database(db: Session = Depends(get_db)):
   
    existing = db.query(Order).first()
    if existing:
        return {"message": "Database already seeded!"}
    
    
    orders = [
        Order(user_id=101, status="Pending", item_name="Mechanical Keyboard"),
        Order(user_id=102, status="Shipped", item_name="Wireless Mouse"),
        Order(user_id=103, status="Delivered", item_name="Gaming Monitor")
    ]
    db.add_all(orders)
    db.commit()
    
    return {"message": "Dummy orders injected successfully! Order IDs: 1, 2, 3"}

@app.post("/chat")
def chat_with_agent(request: UserRequest, db: Session = Depends(get_db)):
    try:
        
        response = process_user_request(db, request)
        return response
    except Exception as e:
        return {"status": "error", "message": str(e)}
