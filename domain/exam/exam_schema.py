from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ChoiceCreate(BaseModel):
    content: str
    is_correct: bool

class Choice(BaseModel):
    id: int
    content: str
    is_correct: bool

    class Config:
        from_attributes = True

class TestQuestionCreate(BaseModel):
    content: str
    choices: List[ChoiceCreate]
    correct_choice_id: int
    description: str

class TestQuestion(BaseModel):
    id: int
    content: str
    description: Optional[str]
    choices: List[Choice]

    class Config:
        from_attributes = True

class ExamCreate(BaseModel):
    title: str
    description: Optional[str]
    user_id: int

class Exam(BaseModel):
    exam_id: int
    title: str
    description: Optional[str]
    create_date: datetime
    user_id: int
    questions: List[TestQuestion]

    class Config:
        from_attributes = True

class AnswerCreate(BaseModel):
    question_id: int
    selected_choice_id: int

class AttemptCreate(BaseModel):
    exam_id: int
    user_id: int
    answers: List[AnswerCreate]

class Attempt(BaseModel):
    id: int
    exam_id: int
    user_id: int
    score: int
    attempt_date: datetime

    class Config:
        from_attributes = True
