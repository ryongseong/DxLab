import re
import json

from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

from datetime import datetime
from sqlalchemy.orm import Session, joinedload

from models import Exam, TestQuestion, Choice, Attempt, Answer, User
from domain.exam.exam_schema import ExamCreate, TestQuestionCreate, ChoiceCreate, AttemptCreate, AnswerCreate

llm = OllamaLLM(model="llama3.1", stop=["<|eot_id|>"])

async def Ollama():
    prompts = await load_prompts(filename="data/prompts.json")
    data = await get_model_response(prompts['system_prompt'], prompts['user_prompt'])

    problems = split_text(data)

    parsed_problems = [parse_problem(problem) for problem in problems]

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

    # Step 3: Llama 모델의 응답을 파싱하여 생성된 문제를 데이터베이스에 저장
    for question_data in llama_questions:
        db_question = TestQuestion(
            content=question_data['question'],
            exam_id=db_exam.exam_id,
            correct_choice_id=int(question_data['correct_answer']),  # 정답 인덱스
            description=question_data['explanation']  # 설명 추가
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        # 각 문제의 선택지를 저장
        for i, option in enumerate(question_data['options']):
            db_choice = Choice(
                content=option,
                is_correct=(i + 1 == int(question_data['correct_answer'])),  # 선택지 번호와 정답 비교
                question_id=db_question.question_id
            )
            db.add(db_choice)
            db.commit()

    return db_exam

def get_exam(db: Session, exam_id: int):
    exam = db.query(Exam).filter(Exam.exam_id == exam_id).all()
    if not exam:
        return None
    return exam

def get_exam_questions(db: Session, exam_id: int):
    # 시험에 속한 모든 질문을 가져오기
    questions = db.query(TestQuestion).options(joinedload(TestQuestion.choices)).filter(TestQuestion.exam_id == exam_id).all()
    
    # 질문이 없으면 None 반환
    if not questions:
        return None
    return questions

def get_exam_question_id(db: Session, question: TestQuestion):
    return question.question_id

def get_exam_choices(db: Session, question_id: int):
    choices = db.query(Choice).filter(Choice.question_id == question_id).all()
    
    # 선택지가 없을 경우 None 또는 빈 리스트 반환
    if not choices:
        return []
    return choices

def submit_attempt(db: Session, attempt_data: AttemptCreate, user_id: int) -> Attempt:
    db_attempt = Attempt(
        exam_id=attempt_data.exam_id,
        user_id=user_id,
        score=0,  # 초기 점수 설정
        attempt_date=datetime.now()
    )
    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)

    score = 0
    for answer_data in attempt_data.answers:
        db_answer = Answer(
            attempt_id=db_attempt.id,
            question_id=answer_data.question_id,
            selected_choice_id=answer_data.selected_choice_id
        )
        db.add(db_answer)
        db.commit()

        db_choice = db.query(Choice).filter(Choice.id == answer_data.selected_choice_id).first()
        if db_choice.is_correct:
            score += 1

    db_attempt.score = score
    db.commit()
    return db_attempt

# 텍스트를 문제별로 나누기 위해 패턴을 사용하여 분리
def split_text(text):
    problems = re.split(r"\n\*\*", text)
    return problems

# 각 문제를 파싱하여 문제, 보기, 정답, 설명으로 나누는 함수
def parse_problem(problem_text):
    # 문제 제목 추출
    title = re.search(r"\*\*(.*?)\*\*", problem_text)
    title = title.group(1) if title else "제목 없음"
    
    # 문제 번호 및 질문 추출
    question_match = re.search(r"(\d+)\.\s(.*?)(\n\d\))", problem_text)
    question = question_match.group(2) if question_match else "질문 없음"
    
    # 보기 추출
    options = re.findall(r"\d\)\s(.*?)\n", problem_text)
    
    # 설명 추출
    explanation_match = re.search(r"# 설명 : (.*)", problem_text)
    explanation = explanation_match.group(1) if explanation_match else "설명 없음"
    
    # 정답 추출
    answer_match = re.search(r"\* 정답 : (\d)", problem_text)
    answer = answer_match.group(1) if answer_match else None

    return {
        "title": title,
        "question": question,
        "options": options,
        "correct_answer": answer,
        "explanation": explanation  # 설명 따로 저장
    }