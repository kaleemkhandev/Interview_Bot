from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.models.user import User
from app.dtos.user_dto import  CreateUser, UpdateUser
from app.utils.database import get_db

router = APIRouter()

@router.post("/")
def create_user(user: CreateUser, db: Session = Depends(get_db)):
    print("********" , user)
    check_user = db.query(User).filter(User.email == user.email).first()
    print("--------------->" , check_user)
    if check_user is not None :
        print("------- EXISTED USER ---------")
        return check_user
    # Implementation of create user logic using the provided user data and the database session (db).
    new_user = User(name=user.name, email=user.email, created_at=user.created_at, status=user.status)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    # Implementation of get user logic using the provided user_id and the database session (db).
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}")
def update_user(user_id: int, user_update: UpdateUser, db: Session = Depends(get_db)):
    # Implementation of update user logic using the provided user_id, user_update data, and the database session (db).
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.dict().items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # Implementation of delete user logic using the provided user_id and the database session (db).
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return user
