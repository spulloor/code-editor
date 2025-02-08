from sqlalchemy.orm import Session
from models import User, CodeFile, AISuggestion
from schemas import UserCreate, CodeFileCreate, AISuggestionBase

def create_user(db: Session, user: UserCreate):
    new_user = User(username=user.username, email=user.email, password_hash=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_code_file(db: Session, file: CodeFileCreate):
    new_file = CodeFile(**file.dict())
    db.add(new_file)
    db.commit()
    db.refresh(new_file)
    return new_file

def get_code_file(db: Session, file_id: int):
    return db.query(CodeFile).filter(CodeFile.id == file_id).first()

def create_ai_suggestion(db: Session, suggestion: AISuggestionBase, code_file_id: int):
    new_suggestion = AISuggestion(**suggestion.dict(), code_file_id=code_file_id)
    db.add(new_suggestion)
    db.commit()
    db.refresh(new_suggestion)
    return new_suggestion

def get_ai_suggestions(db: Session, code_file_id: int):
    return db.query(AISuggestion).filter(AISuggestion.code_file_id == code_file_id).all()