from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.utils.database import Base

class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(String)

    user = relationship("User", back_populates="interviews")
    questions = relationship("Question", back_populates="interview")