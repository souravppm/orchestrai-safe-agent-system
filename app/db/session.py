from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.models import Base

# SQLite Database URL (Development)
SQLALCHEMY_DATABASE_URL = "sqlite:///./orchestrai.db"

# Create Engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
