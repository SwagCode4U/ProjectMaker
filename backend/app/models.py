from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    description = Column(Text)
    backend_framework = Column(String(50))
    frontend_framework = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
