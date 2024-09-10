from sqlalchemy import Boolean, Integer, String, Column, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=True)
    subject = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now())
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="questions")
    modify_date = Column(DateTime, nullable=True)

class Gemini(Base):
    __tablename__ = "gemini"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=True)
    subject = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False, default=datetime.now())
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="gemini")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    thread_id = Column(String, nullable=True)

    questions = relationship("Question", back_populates="user")
    gemini = relationship("Gemini", back_populates="user")
    exams = relationship("Exam", back_populates="user")
    attempts = relationship("Attempt", back_populates="user")

class Exam(Base):
    __tablename__ = "exams"

    exam_id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    create_date = Column(DateTime, default=datetime.now)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", back_populates="exams")
    questions = relationship("TestQuestion", back_populates="exam")
    results = relationship("Attempt", back_populates="exam")


class TestQuestion(Base):
    __tablename__ = "test_questions"

    question_id = Column(Integer, primary_key=True, index=True)
    exam_id = Column(Integer, ForeignKey("exams.exam_id", ondelete="CASCADE"))
    content = Column(Text, nullable=False)
    correct_choice_id = Column(Integer, ForeignKey("choices.choice_id", ondelete="SET NULL"),  nullable=True)
    description = Column(Text, nullable=False)

    exam = relationship("Exam", back_populates="questions")
    correct_choice = relationship(
        "Choice",
        foreign_keys=[correct_choice_id],
        back_populates="question",  # 여기를 'question'으로 수정
        uselist=False  # 이 관계가 하나의 객체만 반환하도록 설정
    )
    choices = relationship(
        "Choice",
        foreign_keys="[Choice.question_id]",
        back_populates="question"  # 'question'이라는 역방향 관계가 Choice 모델에 정의되어 있어야 합니다.
    )
class Choice(Base):
    __tablename__ = "choices"

    choice_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("test_questions.question_id"), onupdate="CASCADE")
    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)

    question = relationship(
        "TestQuestion",
        back_populates="choices",  # 'choices'가 TestQuestion 모델에 정의된 관계 이름입니다.
        foreign_keys=[question_id]
    )


class Attempt(Base):
    __tablename__ = "attempts"

    attempt_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    exam_id = Column(Integer, ForeignKey("exams.exam_id", ondelete="CASCADE"))
    score = Column(Integer, nullable=False)
    attempt_date = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="attempts")
    exam = relationship("Exam", back_populates="results")
    answers = relationship("Answer", back_populates="attempt")

class Answer(Base):
    __tablename__ = "answers"

    answer_id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("attempts.attempt_id", ondelete="CASCADE"))
    question_id = Column(Integer, ForeignKey("test_questions.question_id", ondelete="CASCADE"))
    selected_choice_id = Column(Integer, ForeignKey("choices.choice_id", ondelete="SET NULL"), nullable=True)

    attempt = relationship("Attempt", back_populates="answers")
    question = relationship("TestQuestion")
    selected_choice = relationship("Choice")
