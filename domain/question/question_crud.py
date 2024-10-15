import os
import httpx
import time

from openai import OpenAI
from datetime import datetime
from fastapi import HTTPException
from database import SessionLocal
from domain.question.question_schema import QuestionCreate, QuestionUpdate
from sqlalchemy.orm import Session
from models import Question, User

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID_Keyword = os.getenv("ASSISTANT_ID_Keyword")
ASSISTANT_ID_GENERATE = os.getenv("ASSISTANT_ID_GENERATE")

def get_question_list(db: Session):
    question_list = db.query(Question)\
        .order_by(Question.create_date.desc())\
        .all()
    return question_list

def get_question(db: Session, question_id: int):
    question = db.query(Question).get(question_id)
    return question

def get_user_question(db: Session, user_id: int):
    return db.query(Question).filter(Question.user_id == user_id).all()

async def create_question(db: Session, question: str, category:str, user: User) -> Question:
    thread_id = user.thread_id

    if not thread_id:
        thread_id = await create_new_thread()
        user.thread_id = thread_id
        db.commit()
        db.refresh(user)

    content = await get_gpt_response(question, thread_id)
    
    new_question = Question(
        category=category,
        subject=question,
        content=content,
        create_date=datetime.now(),
        user=user
    )
    
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    
    return new_question

async def create_text(db: Session, question: str, keyword: list[str], user: User) -> Question:
    thread_id = user.thread_id

    if not thread_id:
        thread_id = await create_new_thread()
        user.thread_id = thread_id
        db.commit()
        db.refresh(User)

    content = await make_generation_text(question, keyword, thread_id )

    new_question = Question(
        subject=question+str(keyword),
        content = content,
        create_date=datetime.now(),
        user=user
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question

async def create_new_thread() -> str:
    client = OpenAI(api_key=f"{OPENAI_API_KEY}")
    thread = client.beta.threads.create()
    return thread.id

async def get_gpt_response(question: str, thread_id: str) -> str:
    client = OpenAI(api_key=f"{OPENAI_API_KEY}")
    assistant_id = f"{ASSISTANT_ID_Keyword}"

    # content에 질문을 입력
    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=question # 이 부분이 이제 사용자가 입력하는 부분이 될 예정
    )

    # 실행시킴
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        # max_prompt_tokens = 500
    )

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(2)
    
    thread_messages = client.beta.threads.messages.list(thread_id)
    answer = thread_messages.data[0].content[0].text.value

    return answer

async def make_generation_text(question: str, keyword:list[str], thread_id: str) -> str:
    client = OpenAI(api_key=f"{OPENAI_API_KEY}")
    assistant_id = f"{ASSISTANT_ID_GENERATE}"

    question = question + str(keyword)

    message = client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content="키워드는 다음과 같아" + str(keyword) + question + "이 키워드를 강조하지 말고 키워드를 풀어써서 자기소개서를 다시 만들어줘"
    )

    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )

    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(2)
    
    thread_messages = client.beta.threads.messages.list(thread_id)
    answer = thread_messages.data[0].content[0].text.value

    return answer

async def update_question(db: Session, db_question: Question, question_update: QuestionUpdate, user: User):
    db_question.subject = question_update.subject

    thread_id = user.thread_id
    
    if not thread_id:
        thread_id = await create_new_thread()
        user.thread_id = thread_id
        db.commit()
        db.refresh(user)

    new_content = await get_gpt_response(question_update.subject, thread_id)
    
    db_question.content = new_content
    db_question.modify_date = datetime.now()
    
    db.add(db_question)
    db.commit()

def delete_question(db: Session, db_question: Question):
    db.delete(db_question)
    db.commit()