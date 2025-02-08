from sqlalchemy.orm import Session
from models import AISuggestion
from schemas import AISuggestionBase

def create_ai_suggestion_service(db: Session, suggestion: AISuggestionBase, code_file_id: int):
    new_suggestion = AISuggestion(**suggestion.dict(), code_file_id=code_file_id)
    db.add(new_suggestion)
    db.commit()
    db.refresh(new_suggestion)
    return new_suggestion

def get_ai_suggestions_service(db: Session, code_file_id: int):
    return db.query(AISuggestion).filter(AISuggestion.code_file_id == code_file_id).all()