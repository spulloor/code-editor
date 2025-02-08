from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import AISuggestionResponse
from services.ai_suggestion_service import (
    generate_ai_suggestions_service, get_ai_suggestions_service, accept_ai_suggestion_service, reject_ai_suggestion_service
)

router = APIRouter(prefix="/ai-suggestions", tags=["ai_suggestions"])

@router.post("/{file_id}", response_model=list[AISuggestionResponse])
def generate_ai_suggestions(file_id: int, db: Session = Depends(get_db)):
    return generate_ai_suggestions_service(db, file_id)

@router.get("/{file_id}", response_model=list[AISuggestionResponse])
def get_ai_suggestions(file_id: int, db: Session = Depends(get_db)):
    return get_ai_suggestions_service(db, file_id)

@router.post("/{suggestion_id}/accept")
def accept_ai_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    return accept_ai_suggestion_service(db, suggestion_id)

@router.post("/{suggestion_id}/reject")
def reject_ai_suggestion(suggestion_id: int, db: Session = Depends(get_db)):
    return reject_ai_suggestion_service(db, suggestion_id)