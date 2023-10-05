from sqlalchemy import Column, Text, Integer, DateTime, ForeignKey,String
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    statement = Column(String)
    answer = Column(String)
    interview_id = Column(Integer, ForeignKey("interviews.id"))
    created_at = Column(String)

    interview = relationship("Interview", back_populates="questions")