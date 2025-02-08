from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default='collaborator')  # owner, collaborator
    created_at = Column(DateTime, default=datetime.utcnow)
    
    code_files = relationship("CodeFile", back_populates="owner")
    editing_sessions = relationship("EditingSession", back_populates="user")

class CodeFile(Base):
    __tablename__ = 'code_files'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    content = Column(Text, nullable=False, default='')
    owner_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    language = Column(String, nullable=False)
    description = Column(String)
    
    owner = relationship("User", back_populates="code_files")
    editing_sessions = relationship("EditingSession", back_populates="code_file")
    ai_suggestions = relationship("AISuggestion", back_populates="code_file")

class EditingSession(Base):
    __tablename__ = 'editing_sessions'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    code_file_id = Column(Integer, ForeignKey('code_files.id'))
    role = Column(String, nullable=False, default='collaborator')  # editor, viewer
    joined_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="editing_sessions")
    code_file = relationship("CodeFile", back_populates="editing_sessions")

class AISuggestion(Base):
    __tablename__ = 'ai_suggestions'
    
    id = Column(Integer, primary_key=True, index=True)
    code_file_id = Column(Integer, ForeignKey('code_files.id'))
    suggestion = Column(Text, nullable=False)
    line_number = Column(Integer, nullable=False)
    accepted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    code_file = relationship("CodeFile", back_populates="ai_suggestions")
