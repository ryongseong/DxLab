from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.question import question_schema, question_crud
from domain.user.user_router import get_current_user
from domain.user import user_schema 
from models import User

router = APIRouter(
    prefix="/api/question",
)

@router.get("/list", response_model=list[question_schema.Question])
def question_list(db: Session = Depends(get_db)):
    _question_list = question_crud.get_question_list(db)
    return _question_list

@router.get("/user_list", response_model=list[question_schema.Question])
def user_list(
    db: Session = Depends(get_db),
    current_user: user_schema.User = Depends(get_current_user)
):
    _question_list = question_crud.get_user_question(db, user_id = current_user.id)
    return _question_list

@router.post('/create', status_code=status.HTTP_204_NO_CONTENT)
def question_create(_question_create: question_schema.QuestionCreate,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    question_crud.create_question(db=db, question_create=_question_create,
                                  user=current_user)

@router.post("/gpt")
async def ask_gpt(
    query: question_schema.Query,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # create_question 함수를 호출하여 새로운 질문을 생성합니다
    new_question = await question_crud.create_question(db, query.question, query.category, user)
    
    return {"category": query.category , "question": new_question.subject, "answer": new_question.content}

@router.post("/text")
async def make_text(
    query: question_schema.Query2,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # create_text 함수를 호출하여 새로운 질문을 생성합니다
    new_question = await question_crud.create_text(db, query.question, query.keyword, user)
    
    return {"question": new_question.subject, "answer": new_question.content}

@router.get("/detail/{question_id}", response_model=question_schema.Question)
def question_detail(question_id: int, db: Session = Depends(get_db)):
    question = question_crud.get_question(db, question_id=question_id)
    return question

@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def question_update(
    _question_update: question_schema.QuestionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_question = question_crud.get_question(db, question_id=_question_update.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="수정 권한이 없습니다.")
    
    # 비동기 update_question 호출
    await question_crud.update_question(db=db, db_question=db_question, question_update=_question_update, user=current_user)

@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def question_delete(_question_delete: question_schema.QuestionDelete,
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_user)):
    db_question = question_crud.get_question(db, question_id=_question_delete.question_id)
    if not db_question:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을 수 없습니다.")
    if current_user.id != db_question.user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="삭제 권한이 없습니다.")
    question_crud.delete_question(db=db, db_question=db_question)