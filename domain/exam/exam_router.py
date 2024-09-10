from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from domain.exam.exam_crud import Ollama, create_exam, get_exam, get_exam_choices, get_exam_question_id, submit_attempt, get_exam_questions
from domain.exam.exam_schema import ChoiceCreate, ExamCreate, Exam, AttemptCreate, Attempt, TestQuestion, TestQuestionCreate
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

# @router.post("/")
# def create_exam_endpoint(
#     exam: ExamCreate,
#     db: Session = Depends(get_db),
#     current_user: user_schema.User = Depends(get_current_user)
# ):
#     return create_exam(db, exam, current_user.id)

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

# @router.get('/{exam_id}/questions')
# def read_exam_questions(exam_id: int, db: Session = Depends(get_db)):
#     db_exam_questions = get_exam(db, exam_id)
#     if db_exam_questions is None:
#         raise HTTPException(status_code=404, detail="Exam Questions Not Found")
#     return db_exam_questions

# 시험에 대한 문제 목록을 반환하는 엔드포인트
@router.get('/{exam_id}/questions', response_model=List[TestQuestion])
def read_exam_questions(exam_id: int, db: Session = Depends(get_db)):
    try:
        db_exam_questions = get_exam_questions(db, exam_id)

        if db_exam_questions is None or len(db_exam_questions) == 0:
            raise HTTPException(status_code=404, detail="Questions not found")

        # Pydantic 모델로 직렬화
        return [TestQuestion.from_orm(q) for q in db_exam_questions]
    
    except Exception as e:
        print(f"Error fetching exam questions: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")



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
