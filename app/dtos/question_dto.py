from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CreateQuestion(BaseModel):
    statement: str
    answer: str
    interview_id: int
    created_at: Optional[str] = None

class UpdateQuestion(BaseModel):
    statement: Optional[str] = None
    answer: Optional[str] = None
    interview_id: Optional[int] = None


class CreateMultipleQuestions(BaseModel):
    questions: List[CreateQuestion]