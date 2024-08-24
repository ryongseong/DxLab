from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.exam.exam_schema import ExamCreate, Exam, AttemptCreate, Attempt, ChoiceCreate, Choice
from domain.exam.exam_crud import (
    create_exam, get_exam, get_exam_list, update_exam, delete_exam,
    create_question, create_choice, update_choice, delete_choice,
    create_attempt, get_attempt_list
)
from domain.user.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/exam",
)

@router.post('/', response_model=Exam)
def create_exam(exam: ExamCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return create_exam(db, exam, user)

@router.get('/', response_model=list[Exam])
def read_exams(db: Session = Depends(get_db)):
    return get_exam_list(db)

@router.get('/{exam_id}', response_model=Exam)
def read_exam(exam_id: int, db: Session = Depends(get_db)):
    db_exam = get_exam(db, exam_id)
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")

    return db_exam

@router.put('/{exam_id}', response_model=Exam)
def update_exam(exam_id: int, exam: ExamCreate, db: Session = Depends(get_db)):
    db_exam = update_exam(db, exam_id, exam_update=exam)
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return db_exam

@router.delete('/{exam_id}', response_model=Exam)
def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    delete_exam(db, exam_id)
    return {"message" : "Exam deleted successfully"}


@router.post('/questions/{question_id}/choices/', response_model=Choice)
def create_choice_for_question(
    question_id: int,
    choice: ChoiceCreate,
    db: Session = Depends(get_db)):
    return create_choice(db, choice_data=choice, question_id=question_id)

@router.get('/questions/{question_id}/choices/', response_model=list[Choice])
def read_choices_for_question(
    question_id: int,
    db: Session = Depends(get_db)):
    db_question = get_exam(db, question_id)
    if db_question is None:
        raise HTTPException(status_code=404, detail="Question not found")
    
    return db_question.choices

@router.put('/choices/{choice_id}/', response_model=Choice)
def update_choice_for_question(
    choice_id: int,
    choice_update: ChoiceCreate,
    db: Session = Depends(get_db)):
    db_choice = update_choice(db, choice_id, choice_data = choice_update)
    if db_choice is None:
        raise HTTPException(status_code=404, detail="Choice not found")
    return db_choice

@router.delete('/choices/{choice_id}', response_model=dict)
def delete_choice(
    choice_id: int,
    db: Session = Depends(get_db)
):
    delete_choice(db, choice_id)
    return {"message" : "Choice deleted successfully"}



@router.post('/attempts/', response_model=Attempt)
def create_attempt(
    attempt: AttemptCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)):
    return create_attempt(db, attempt, user)

@router.get('/attempts/', response_model=list[Attempt])
def read_attempts(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_attempt_list(db, user_id = user.id)