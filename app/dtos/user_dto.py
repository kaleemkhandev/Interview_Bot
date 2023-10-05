from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ResponseUser(BaseModel):
    id: int
    name: str
    email: Optional[str] = None
    created_at: Optional[str] = None
    status: int

class CreateUser(BaseModel):
    name: str
    email: Optional[str] = None
    created_at: Optional[str] = None
    status: int

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    status: Optional[int] = None