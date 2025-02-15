from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.gemini import gemini_schema, gemini_crud
from domain.user.user_router import get_current_user
from domain.user import user_schema
from models import User

router = APIRouter(
    prefix="/api/gemini",
)

router.get('/user_list', response_model=list[gemini_schema.Gemini])
def gemini_list(
        db: Session = Depends(get_db),
        current_user: user_schema.User = Depends(get_current_user)
):
    _gemini_list = gemini_crud.get_gemini_list(db, user_id = current_user.id)
    return _gemini_list

router.post('/gpt')
async def get_keyword(
    query: gemini_schema.Query,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # create_question 함수를 호출하여 새로운 질문을 생성합니다
    new_question = await gemini_crud.create_question(db, query.question, query.category, user)
    
    return {"category": query.category , "question": new_question.subject, "answer": new_question.content}

@router.post('/text')
async def make_text_gemini(
    query: gemini_schema.Query2,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    # create_text 함수를 호출하여 새로운 질문을 생성합니다
    new_question = await gemini_crud.create_text(db, query.question, query.keyword, user)
    
    return {"question": new_question.subject, "answer": new_question.content}