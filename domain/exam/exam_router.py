from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.exam.exam_schema import Exam as ExamSchema
from domain.exam.exam_crud import create_exam, get_exam, get_exam_with_questions_and_choices, submit_attempt
from domain.exam.exam_schema import ChoiceCreate, ExamCreate, AttemptCreate, Attempt, TestQuestion, TestQuestionCreate
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
async def create_exam_endpoint(
    exam_data: ExamCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    # 그냥 요청을 받아서 CRUD의 create_exam 함수로 넘겨주는 역할
    return await create_exam(db, exam_data, current_user.id)  # Ollama 호출과 문제 생성은 create_exam에서 처리됨

@router.get("/{exam_id}")
def read_exam(exam_id: int, db: Session = Depends(get_db)):
    db_exam = get_exam(db, exam_id)
    if db_exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    return db_exam

@router.get("/{exam_id}/questions", response_model=ExamSchema)
def read_exam_with_questions_and_choices(exam_id: int, db: Session = Depends(get_db)):
    exam = get_exam_with_questions_and_choices(db, exam_id)
    
    if exam is None:
        raise HTTPException(status_code=404, detail="Exam not found")
    
    # SQLAlchemy ORM 객체를 Pydantic 모델로 수동 변환
    exam_dict = {
        'exam_id': exam.exam_id,
        'title': exam.title,
        'description': exam.description,
        'create_date': exam.create_date,
        'user_id': exam.user_id,
        'questions': [
            {
                'id': question.question_id,
                'content': question.content,
                'description': question.description,
                'choices': [
                    {
                        'id': choice.choice_id,
                        'content': choice.content,
                        'is_correct': choice.is_correct
                    }
                    for choice in question.choices
                ]
            }
            for question in exam.questions
        ]
    }
    
    # 변환된 데이터를 Pydantic 모델로 변환
    return ExamSchema.model_validate(exam_dict)

@router.post("/{exam_id}/attempt", response_model=Attempt)
async def attempt_exam(
    exam_id: int,
    attempt_data: AttemptCreate,
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    attempt_data.exam_id = exam_id
    attempt = await submit_attempt(db, attempt_data, current_user.id)
    return attempt

@router.get("/{exam_id}/attempts", response_model=List[Attempt])
def get_attempts(exam_id: int, db: Session = Depends(get_db), current_user: user_schema.User = Depends(get_current_user)):
    return db.query(Attempt).filter(Attempt.exam_id == exam_id, Attempt.user_id == current_user.id).all()
