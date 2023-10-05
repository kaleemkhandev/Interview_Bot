from sqlalchemy import Column, String, Integer, DateTime, ForeignKey,Boolean
from sqlalchemy.orm import relationship
from app.utils.database import Base

class chat_model(Base):
    __tablename__ = "fixed_Questions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    is_quest = Column(Boolean, nullable=False, default=False)  # Added is_quest column
    questions = Column(String,nullable = True)