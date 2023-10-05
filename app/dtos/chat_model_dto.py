from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ChatDTO(BaseModel):
    id: int
    name: str
    is_quest: bool
    questions: str

    class Config:
        orm_mode = True
