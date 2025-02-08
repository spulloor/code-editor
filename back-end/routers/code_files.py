from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import CodeFile
from schemas import CodeFileCreate, CodeFileResponse
from services.codefile_service import (
    create_code_file_service, get_code_file_service, update_code_file_service, delete_code_file_service, get_user_code_files_service
)
from security import get_current_user

router = APIRouter(prefix="/code-files", tags=["code_files"])

@router.post("/", response_model=CodeFileResponse)
def create_code_file(file: CodeFileCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return create_code_file_service(db, file)

@router.get("/{file_id}", response_model=CodeFileResponse)
def get_code_file(file_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_code_file_service(db, file_id)

@router.put("/{file_id}", response_model=CodeFileResponse)
def update_code_file(file_id: int, file: CodeFileCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return update_code_file_service(db, file_id, file)

@router.delete("/{file_id}")
def delete_code_file(file_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return delete_code_file_service(db, file_id)

@router.get("/user/{user_id}", response_model=list[CodeFileResponse])
def get_user_code_files(user_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return get_user_code_files_service(db, user_id)