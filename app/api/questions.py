from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.question import Question
from app.dtos.question_dto import CreateQuestion, CreateMultipleQuestions, UpdateQuestion
from app.utils.database import get_db

router = APIRouter()

@router.post("/")
def create_question(question: CreateQuestion, db: Session = Depends(get_db)):
    # Implementation of create question logic using the provided question data and the database session (db).
    new_question = Question(
        statement=question.statement,
        answer=question.answer,
        interview_id=question.interview_id,
        created_at=question.created_at,
    )
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    return new_question

@router.post("/bulk")
def create_multiple_questions(questions: CreateMultipleQuestions, db: Session = Depends(get_db)):
    # Implementation of create multiple questions logic using the provided questions data and the database session (db).
    new_questions = []
    for question_data in questions.questions:
        new_question = Question(
            statement=question_data.statement,
            answer=question_data.answer,
            interview_id=question_data.interview_id,
            created_at=question_data.created_at,
        )
        db.add(new_question)
        new_questions.append(new_question)

    db.commit()
    # db.refresh(new_questions)
    # Refresh each new question individually
    for question in new_questions:
        db.refresh(question)

    return new_questions




@router.get("/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):
    # Implementation of get question logic using the provided question_id and the database session (db).
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    return question


@router.get("/interview/{interview_id}")
def get_questions(interview_id: int, db: Session = Depends(get_db)):
    # Implementation of get question logic using the provided interview_id and the database session (db).
    questions = db.query(Question).filter(Question.interview_id == interview_id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="Question not found")
    return questions


@router.put("/{question_id}")
def update_question(question_id: int, question_update: UpdateQuestion, db: Session = Depends(get_db)):
    # Implementation of update question logic using the provided question_id, question_update data, and the database session (db).
    question = db.query(Question).filter(Question.id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    for key, value in question_update.dict(exclude_unset=True).items():
        setattr(question, key, value)

    db.commit()
    db.refresh(question)
    return question