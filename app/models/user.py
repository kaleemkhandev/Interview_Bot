from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from app.utils.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String)
    created_at = Column(String)
    status = Column(Integer)

    interviews = relationship("Interview", back_populates="user")
