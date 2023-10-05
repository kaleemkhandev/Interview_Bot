from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CreateInterview(BaseModel):
    type: str
    user_id: int
    created_at: Optional[str] = None

class UpdateInterview(BaseModel):
    type: Optional[str] = None
    user_id: Optional[int] = None