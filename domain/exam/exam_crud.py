import re
import json
import requests

from fastapi import HTTPException

from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models import Exam, TestQuestion, Choice, Attempt, Answer, User
from domain.exam.exam_schema import ExamCreate, TestQuestionCreate, ChoiceCreate, AttemptCreate, AnswerCreate

llm = OllamaLLM(model="llama3.1", stop=["<|eot_id|>"])

async def create_exam(db: Session, exam_data: ExamCreate, user_id: int) -> Exam:
    db_exam = Exam(
        title=exam_data.title,
        description=exam_data.description,
        user_id=user_id,
        create_date=datetime.now()
    )
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)

    # 모델 서버로 요청 보내기
    response = requests.post("http://host.docker.internal:8001/ollama")
    
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Model server error")

    llama_questions = response.json()['parsed_problems']

    for question_data in llama_questions:
        db_question = TestQuestion(
            content=question_data['question'],
            exam_id=db_exam.exam_id,
            description=question_data['explanation']
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        correct_choice = None
        for i, option in enumerate(question_data['options']):
            existing_choice = db.query(Choice).filter_by(question_id=db_question.question_id, content=option).first()
            if not existing_choice:
                db_choice = Choice(
                    content=option,
                    is_correct=(i + 1 == int(question_data['correct_answer'])),
                    question_id=db_question.question_id
                )
                db.add(db_choice)
                db.commit()
                if db_choice.is_correct:
                    correct_choice = db_choice
            
        if correct_choice:
            db_question.correct_choice_id = correct_choice.choice_id
            db.commit()
            db.refresh(db_question)

    return db_exam

def get_exam(db: Session, exam_id: int):
    exam = db.query(Exam).filter(Exam.exam_id == exam_id).all()
    if not exam:
        return None
    return exam

# Exam ID에 해당하는 TestQuestions와 Choices를 가져오는 함수
def get_exam_with_questions_and_choices(db: Session, exam_id: int):
    # Exam을 먼저 가져오고, Exam에 연결된 TestQuestions와 Choices를 가져옴
    exam = db.query(Exam).filter(Exam.exam_id == exam_id).first()

    if exam is None:
        return None
    
    # Exam에 포함된 모든 TestQuestion 및 Choice 정보 가져오기
    questions = db.query(TestQuestion).filter(TestQuestion.exam_id == exam_id).all()

    for question in questions:
        choices = db.query(Choice).filter(Choice.question_id == question.question_id).all()
        question.choices = choices  # 각 질문에 대해 선택지를 추가
    
    return exam

async def submit_attempt(db: Session, attempt_data: AttemptCreate, user_id: int) -> Attempt:    
    db_attempt = Attempt(
        exam_id=attempt_data.exam_id,
        user_id=user_id,
        score=0,
        attempt_date=datetime.now()
    )
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)

    score = 0

    for answer_data in attempt_data.answers:
        db_answer = Answer(
            attempt_id=db_attempt.attempt_id,
            question_id=answer_data.question_id,
            selected_choice_id=answer_data.selected_choice_id
        )
        db.add(db_answer)
        db.commit()

        # 선택한 답안이 정답인지 확인
        db_choice = db.query(Choice).filter_by(choice_id=answer_data.selected_choice_id).first()
        if db_choice and db_choice.is_correct:
            score += 1

    # 최종 점수 저장
    db_attempt.score = score
    db.commit()

    # 최종적으로 사용자의 시도 데이터를 반환
    return Attempt(
        attempt_id=db_attempt.attempt_id,
        exam_id=db_attempt.exam_id,
        user_id=db_attempt.user_id,
        score=db_attempt.score,
        attempt_date=db_attempt.attempt_date
    )


# 텍스트를 문제별로 나누기 위해 패턴을 사용하여 분리
# 텍스트를 문제별로 나누는 함수
def split_text(text):
    # '**'로 시작하는 텍스트를 기준으로 각 문제를 분리
    problems = re.split(r"\*\*.*?\*\*", text)
    # 첫 번째 빈 항목 제거 (파일 시작에 있는 데이터는 무시)
    return [problem.strip() for problem in problems if problem.strip()]

# 각 문제를 파싱하여 문제, 보기, 정답, 설명으로 나누는 함수
def parse_problem(problem_text):
    # 질문 추출
    question_match = re.search(r"(\d+)\.\s(.*?)(\n\d\))", problem_text)
    question = question_match.group(2) if question_match else "질문 없음"
    
    # 설명 추출
    explanation_match = re.search(r"# 설명 : (.*)", problem_text)
    explanation = explanation_match.group(1) if explanation_match else "설명 없음"
    
    # 보기 추출 (보기는 '숫자)' 형식으로 시작)
    options = re.findall(r"\d\)\s(.*?)\n", problem_text)
    
    # 정답 추출
    answer_match = re.search(r"\* 정답 : (\d)", problem_text)
    answer = answer_match.group(1) if answer_match else None

    return {
        "question": question,
        "options": options,
        "correct_answer": answer,
        "explanation": explanation
    }