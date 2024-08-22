from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

from domain.user.user_schema import User

class Question(BaseModel):
    id: int
    category: Optional[str]
    subject: str
    content: str
    create_date: datetime
    user: User | None

class QuestionCreate(BaseModel):
    category: str | None
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('Field cannot be empty')
        return v

class Query(BaseModel):
    category: str
    question: str

class Query2(BaseModel):
    question: str
    keyword: list[str]

class QuestionUpdate(BaseModel):
    subject: str
    content: Optional[str] = None
    question_id: int

class QuestionDelete(BaseModel):
    question_id: int