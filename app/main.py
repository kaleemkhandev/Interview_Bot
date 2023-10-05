from fastapi import FastAPI
from app.api import users, interviews, questions,chat_model
from app.utils.database import create_all_tables

create_all_tables()
app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(interviews.router, prefix="/interviews", tags=["interviews"])
app.include_router(questions.router, prefix="/questions", tags=["questions"])
app.include_router(chat_model.router, prefix="/chat_model", tags=["chat_model"])

# How to start
# uvicorn app.main:app --reload
