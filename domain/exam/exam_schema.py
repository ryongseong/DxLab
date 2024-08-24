from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Choice(BaseModel):
    id: int
    content: str
    is_correct: bool

    class Config:
        from_attributes = True

class ChoiceCreate(BaseModel):
    content: str
    is_correct: bool

class TestQuestion(BaseModel):
    id: int
    content: str
    choices: List[Choice]
    
    class Config:
        from_attributes = True

class TestQuestionCreate(BaseModel):
    content: str
    choices: List[ChoiceCreate]

class Exam(BaseModel):
    id: int
    title: str
    description: Optional[str]
    create_date: datetime
    user_id: int
    questions: List[TestQuestion]

    class Config:
        from_attributes = True

class ExamCreate(BaseModel):
    title: str
    description: Optional[str] = None
    questions: List[TestQuestionCreate]

class Attempt(BaseModel):
    id: int
    user_id: int
    exam_id: int
    score: int
    attempt_date: datetime

    class Config:
        from_attributes = True

class AttemptCreate(BaseModel):
    exam_id: int
    score: int