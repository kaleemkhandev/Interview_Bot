from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.interview import Interview
from app.dtos.interview_dto import CreateInterview, UpdateInterview
from app.utils.database import get_db

router = APIRouter()

@router.post("/")
def create_interview(interview: CreateInterview, db: Session = Depends(get_db)):
    # Implementation of create interview logic using the provided interview data and the database session (db).
    new_interview = Interview(type=interview.type, user_id=interview.user_id, created_at=interview.created_at)
    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)
    return new_interview

@router.get("/{interview_id}")
def get_interview(interview_id: int , db: Session = Depends(get_db)):
    # Implementation of get interview logic using the provided interview_id and the database session (db).
    interview = db.query(Interview).filter(Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    return interview



@router.get("/all/{user_id}")
def get_interview(user_id: int, db: Session = Depends(get_db)):
    all_interview = db.query(Interview).filter(Interview.user_id == user_id).all()
    if len(all_interview) <= 0:
        raise HTTPException(status_code=404, detail="Interviews not found")
    return all_interview
