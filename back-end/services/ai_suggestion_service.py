from sqlalchemy.orm import Session
from models import AISuggestion, CodeFile
from schemas import AISuggestionResponse
from datetime import datetime
from fastapi import HTTPException

from config import settings
import requests
import re



def generate_ai_suggestions_service(db: Session, code_file_id: int):
    
    # check if the code file exists
    code_file = db.query(CodeFile).filter(CodeFile.id == code_file_id).first()
    if not code_file:
        raise HTTPException(status_code=404, detail="Code file not found")
    
    # Check if AI suggestions already exist for this code file
    existing_suggestions = db.query(AISuggestion).filter(AISuggestion.code_file_id == code_file_id).all()
    # return only pending suggestions if they exist
    pending_suggestions = [suggestion for suggestion in existing_suggestions if suggestion.status == "pending"]
    
    if existing_suggestions and pending_suggestions:
        return pending_suggestions
    
    # Prepare request for Ollama
    payload = {
        "model": settings.MODEL_NAME,
        "prompt": f'''
                Analyze the following code and look out for any potential syntax errors, bugs or performance issues. 

                The Code: {code_file.content}

                Output should be in the form "Line X: Suggestion text" where X is the current line number you are analysing in the given code and for which you will give a suggestion''',
        "stream": False  # Disable streaming for a single response
    }

    try:
        response = requests.post(settings.OLLAMA_URL, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")

    # Extract AI suggestions
    suggestions_text = response.json().get("response", "").strip()
    if not suggestions_text:
        raise HTTPException(status_code=500, detail="AI returned an empty suggestion list.")

    # Parse suggestions and line numbers
    suggestions = []
    suggestion_pattern = re.compile(r"(Line)?\s*(\d+)\s*[\:\.]?\s*(.+)", re.IGNORECASE)
    
    lines = suggestions_text.split("\n")

    for line in lines:
        match = suggestion_pattern.match(line)
        if match:
            line_number = int(match.group(2))
            suggestion_text = match.group(3).strip()

            # Store each suggestion in the database
            new_suggestion = AISuggestion(
                code_file_id=code_file_id,
                suggestion=suggestion_text,
                line_number=line_number,
                status="pending"
            )
            db.add(new_suggestion)
            suggestions.append(new_suggestion)

    if not suggestions:
        raise HTTPException(status_code=500, detail="AI suggestions could not be parsed.")

    db.commit()
    return suggestions

        

def get_ai_suggestions_service(db: Session, file_id: int):

    # check if the code file exists
    code_file = db.query(CodeFile).filter(CodeFile.id == file_id).first()
    if not code_file:
        raise HTTPException(status_code=404, detail="Code file not found")

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