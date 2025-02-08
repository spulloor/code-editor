from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str  # Password is required only when creating a user

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True  # Allows ORM compatibility

class CodeFileBase(BaseModel):
    name: str
    content: Optional[str] = ""

class CodeFileCreate(CodeFileBase):
    owner_id: int  # ID of the user creating the file
    language: str  # Programming language of the code file
    description: Optional[str] = None  # Optional description of the file

class CodeFileResponse(CodeFileBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AISuggestionBase(BaseModel):
    suggestion: str
    line_number: int

class AISuggestionResponse(AISuggestionBase):
    id: int
    code_file_id: int
    accepted: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

class UserLogin(BaseModel):
    email: str
    password: str