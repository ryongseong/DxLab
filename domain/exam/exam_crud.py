from datetime import datetime
from sqlalchemy.orm import Session

from models import Exam, TestQuestion, Choice, Attempt, Answer, User
from domain.exam.exam_schema import ExamCreate, TestQuestionCreate, ChoiceCreate, AttemptCreate, AnswerCreate

def create_exam(db: Session, exam_data: ExamCreate, user_id: int) -> Exam:
    db_exam = Exam(
        title=exam_data.title,
        description=exam_data.description,
        user_id=user_id,
        create_date=datetime.now()
    )
    db.add(db_exam)
    db.commit()
    db.refresh(db_exam)

    for question_data in exam_data.questions:
        db_question = TestQuestion(
            content=question_data.content,
            exam_id=db_exam.exam_id
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)

        for choice_data in question_data.choices:
            db_choice = Choice(
                content=choice_data.content,
                is_correct=choice_data.is_correct,
                question_id=db_question.question_id
            )
            db.add(db_choice)
            db.commit()
            db.refresh(db_choice)

    return db_exam

def get_exam(db: Session, exam_id: int) -> Exam:
    exam = db.query(Exam).filter(Exam.exam_id == exam_id).first()
    if not exam:
        return None
    return exam

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
