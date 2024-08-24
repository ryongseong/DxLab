import time

from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session
from models import Exam, TestQuestion, Choice, Attempt, User
from domain.exam.exam_schema import ExamCreate, TestQuestionCreate, ChoiceCreate, AttemptCreate

def create_exam(db: Session, exam: ExamCreate, user: User) -> Exam:
    db_exam = Exam(
        title=exam.title,
        description=exam.description,
        create_date=datetime.now(),
        user_id=user.id
    )
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)

    for question_data in exam.questions:
        create_question(db, question_data, db_exam.id)
    
    return db_exam

def get_exam(db: Session, exam_id: int) -> Exam:
    return db.query(Exam).filter(Exam.id == exam_id).first()

def get_exam_list(db: Session) -> list[Exam]:
    return db.query(Exam).all()

def update_exam(db: Session, exam_id: int, exam_update: ExamCreate) -> Exam:
    db_exam = get_exam(db, exam_id)
    if not db_exam:
        return None

    db_exam.title = exam_update.title
    db_exam.description = exam_update.description
    db.commit()
    db.refresh(db_exam)
    
    return db_exam

def delete_exam(db: Session, exam_id: int):
    db_exam = get_exam(db, exam_id)
    if db_exam:
        db.delete(db_exam)
        db.commit()

def create_question(db: Session, question_data: TestQuestionCreate, exam_id: int) -> TestQuestion:
    db_question = TestQuestion(
        content=question_data.content,
        exam_id=exam_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)

    for choice_data in question_data.choices:
        create_choice(db, choice_data, db_question.id)

    return db_question

def create_choice(db: Session, choice_data: ChoiceCreate, question_id: int) -> Choice:
    db_choice = Choice(
        question_id,
        content=choice_data.content,
        is_correct=choice_data.is_correct
    )

    db.add(db_choice)
    db.commit()
    db.refresh(db_choice)

    return db_choice

def update_choice(db: Session, choice_id: int, choice_data: ChoiceCreate) -> ChoiceCreate:
    db_choice = db.query(Choice).filter(Choice.id == choice_id).first()
    if not db_choice:
        return None
    
    db_choice.content = choice_data.content
    db_choice.is_correct = choice_data.is_correct
    db.commit()
    db.refresh(db_choice)

    return db_choice

def delete_choice(db: Session, choice_id: int):
    db_choice = db.query(Choice).filter(Choice.id == choice_id).first()
    if db_choice:
        db.delete(db_choice)
        db.commit()

def create_attempt(db: Session, attempt: AttemptCreate, user: User) -> Attempt:
    db_attempt = Attempt(
        user_id = user.id,
        exam_id = attempt.exam_id,
        score = attempt.score,
        attempt_date = datetime.now()
    )

    db.add(db_attempt)
    db.commit()
    db.refresh(db_attempt)

    return db_attempt

def get_attempt_list(db: Session, user_id: int) -> list[Attempt]:
    return db.query(Attempt).filter(Attempt.user_id == user_id).all()