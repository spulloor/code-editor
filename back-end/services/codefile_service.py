from sqlalchemy.orm import Session
from models import CodeFile, User
from schemas import CodeFileCreate, CodeFileResponse
from datetime import datetime
from fastapi import HTTPException

def create_code_file_service(db: Session, file: CodeFileCreate):

    owner = db.query(User).filter(User.id == file.owner_id).first()
    if not owner:
        raise HTTPException(status_code=400, detail="Owner not found")

    new_file = CodeFile(**file.dict(), created_at=datetime.utcnow())
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file

def get_code_file_service(db: Session, file_id: int):
    file = db.query(CodeFile).filter(CodeFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="Code file not found")
    return file

def update_code_file_service(db: Session, file_id: int, file: CodeFileCreate):
    existing_file = db.query(CodeFile).filter(CodeFile.id == file_id).first()
    if not existing_file:
        raise HTTPException(status_code=404, detail="Code file not found")
    
    owner = db.query(User).filter(User.id == file.owner_id).first()
    if not owner:
        raise HTTPException(status_code=400, detail="Owner not found")
    
    for key, value in file.dict().items():
        setattr(existing_file, key, value)
    db.commit()
    db.refresh(existing_file)
    return existing_file

def delete_code_file_service(db: Session, file_id: int):
    file = db.query(CodeFile).filter(CodeFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="Code file not found")
    
    db.delete(file)
    db.commit()
    return {"message": "Code file deleted"}

def get_user_code_files_service(db: Session, user_id: int):
    return db.query(CodeFile).filter(CodeFile.owner_id == user_id).all()