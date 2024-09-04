# Import Libraries
import json
import os
import torch
import warnings
import time

from IPython.display import Markdown
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_google_genai import GoogleGenerativeAI
from langchain_community.retrievers import BM25Retriever
from langchain_community.vectorstores import Chroma
from sentence_transformers import SentenceTransformer, util
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema.runnable import RunnableMap
from transformers import AutoTokenizer
from openai import OpenAI
from datetime import datetime
from fastapi import HTTPException
from database import SessionLocal
from domain.gemini.gemini_schema import GeminiCreate
from sqlalchemy.orm import Session
from models import Gemini, User


# Suppress specific FutureWarning related to tokenization spaces
# warnings.filterwarnings("ignore", category=FutureWarning, message="`clean_up_tokenization_spaces` was not set")
warnings.filterwarnings("ignore", category=FutureWarning)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ASSISTANT_ID_Keyword = os.getenv("ASSISTANT_ID_Keyword")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

async def create_question(db: Session, question:str, category: str, user: User) -> Gemini:
    thread_id = user.thread_id
    
    if not thread_id:
        thread_id = await create_new_thread()
        user.thread_id = thread_id
        db.commit()
        db.refresh(user)

    content = await get_gpt_response(question, thread_id)

    new_question = Gemini(
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

async def create_text(db: Session, question: str, keyword:list[str], user: User) -> str:
    
    content = await make_gemini_text(question, keyword)

    new_question = Gemini(
        subject=question+str(keyword),
        content=content,
        create_date=datetime.now(),
        user=user
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return new_question

async def make_gemini_text(question: str, keyword: list[str]) -> str:
    pass