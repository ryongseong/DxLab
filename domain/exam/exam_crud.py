import re
import json

from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError

from models import Exam, TestQuestion, Choice, Attempt, Answer, User
from domain.exam.exam_schema import ExamCreate, TestQuestionCreate, ChoiceCreate, AttemptCreate, AnswerCreate

llm = OllamaLLM(model="llama3.1", stop=["<|eot_id|>"])

async def Ollama():
    prompts = await load_prompts(filename="data/prompts.json")
    data = await get_model_response(prompts['system_prompt'], prompts['user_prompt'])

    problems = split_text(data)

    parsed_problems = [parse_problem(problem) for problem in problems if parse_problem(problem).get('question') != "질문 없음"]

    return parsed_problems

async def get_model_response(user_prompt, system_prompt):
    template = """
        <|begin_of_text|>
        <|start_header_id|>system<|end_header_id|>
        {system_prompt}
        <|eot_id|>
        <|start_header_id|>user<|end_header_id|>
        {user_prompt}
        <|eot_id|>
        <|start_header_id|>assistant<|end_header_id|>
        # 단계별로 생각해봅시다.
    """
    prompt = PromptTemplate(
        input_variables=["system_prompt", "user_prompt"],
        template=template
    )

    # response = llm(prompt.format(system_prompt=system_prompt, user_prompt=user_prompt))
    response = llm.invoke(prompt.format(system_prompt=system_prompt, user_prompt=user_prompt))
    return response

async def load_prompts(filename):
    with open(filename, 'r') as file:
        return json.load(file)

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

    llama_questions = await Ollama()

    # Llama 모델의 응답을 파싱하여 생성된 문제를 데이터베이스에 저장
    for question_data in llama_questions:
        db_question = TestQuestion(
            content=question_data['question'],
            exam_id=db_exam.exam_id,
            description=question_data['explanation']  # 설명 추가
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        correct_choice = None

        # 각 문제의 선택지를 저장
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

                # 정답 선택지일 경우 correct_choice_id 업데이트
                if db_choice.is_correct:
                    correct_choice = db_choice
            
        # correct_choice_id를 업데이트
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


def submit_attempt(db: Session, attempt_data: AttemptCreate, user_id: int) -> Attempt:
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

        db_choice = db.query(Choice).filter(Choice.choice_id == answer_data.selected_choice_id).first()
        if db_choice and db_choice.is_correct:
            score += 1

    db_attempt.score = score
    db.commit()

    return db_attempt

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