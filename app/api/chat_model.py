from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.chat_model import chat_model
from app.utils.database import get_db
from app.dtos.chat_model_dto import ChatDTO

router = APIRouter()

@router.post("/")
def save_fixed_questions(model_info:ChatDTO,db:Session = Depends(get_db)):

    new_model = chat_model(
                           name = model_info.name,
                           is_quest = model_info.is_quest,
                           questions = model_info.questions)
    
    db.add(new_model)
    db.commit()
    db.refresh(new_model)
    return new_model

@router.get("/")
def get_fixed_questions(mode_id:int,db:Session = Depends(get_db)):
    model_info = db.query(chat_model).filter(chat_model.id == mode_id).first()
    if not model_info:
        raise HTTPException(status_code=404, detail="User not found")
    return model_info

    
