from sqlalchemy.orm import Session
from models import AISuggestion, CodeFile
from schemas import AISuggestionResponse
from datetime import datetime
from fastapi import HTTPException

def generate_ai_suggestions_service(db: Session, file_id: int):
    file = db.query(CodeFile).filter(CodeFile.id == file_id).first()
    if not file:
        raise HTTPException(status_code=404, detail="Code file not found")
    
    # Mock AI analysis (to be replaced with actual AI model integration)
    suggestions = [
        AISuggestion(code_file_id=file_id, suggestion="Optimize loop", line_number=5, accepted=False, created_at=datetime.utcnow()),
        AISuggestion(code_file_id=file_id, suggestion="Use list comprehension", line_number=8, accepted=False, created_at=datetime.utcnow())
    ]
    
    db.add_all(suggestions)
    db.commit()
    return suggestions

def get_ai_suggestions_service(db: Session, file_id: int):
    return db.query(AISuggestion).filter(AISuggestion.code_file_id == file_id).all()

def accept_ai_suggestion_service(db: Session, suggestion_id: int):
    
    suggestion = db.query(AISuggestion).filter(AISuggestion.id == suggestion_id).first()
    
    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    
    if suggestion.status in ["accepted", "rejected"]:
        raise HTTPException(status_code=400, detail="Suggestion has already been processed")

    suggestion.status = "accepted"

    db.commit()
    return {"message": "Suggestion accepted"}

def reject_ai_suggestion_service(db: Session, suggestion_id: int):
    suggestion = db.query(AISuggestion).filter(AISuggestion.id == suggestion_id).first()

    if not suggestion:
        raise HTTPException(status_code=404, detail="Suggestion not found")
    
    if suggestion.status in ["accepted", "rejected"]:
        raise HTTPException(status_code=400, detail="Suggestion has already been processed")

    suggestion.status = "rejected"
    
    db.commit()
    return {"message": "Suggestion rejected"}