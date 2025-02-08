from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserResponse
from services.user_service import create_user_service, get_user_service
from security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return create_user_service(db, user)

@router.get("/me", response_model=UserResponse)
def get_current_user_profile(user=Depends(get_current_user)):
    return user

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_user_service(db, user_id)