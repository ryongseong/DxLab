from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.exam.exam_crud import create_exam, get_exam, submit_attempt
from domain.exam.exam_schema import ExamCreate, Exam, AttemptCreate, Attempt
from domain.user import user_schema
from domain.user.user_router import get_current_user
from models import Exam as EX

router = APIRouter(
    prefix="/api/exam",
)

@router.get('/')
def list_exams(db: Session = Depends(get_db)):
    exams = db.query(EX).all()
    return exams

@router.post("/")
def create_exam_endpoint(
    exam: ExamCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    return create_exam(db, exam, current_user.id)

@router.get("/{exam_id}")
def read_exam(exam_id: int, db: Session = Depends(get_db)):
    db_exam = get_exam(db, exam_id)
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return db_exam

@router.post("/{exam_id}/attempt", response_model=Attempt)
def attempt_exam(
    exam_id: int,
    attempt_data: AttemptCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    attempt_data.exam_id = exam_id
    return submit_attempt(db, attempt_data, current_user.id)

@router.get("/{exam_id}/attempts", response_model=List[Attempt])
def get_attempts(exam_id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return db.query(Attempt).filter(Attempt.exam_id == exam_id, Attempt.user_id == current_user.id).all()
