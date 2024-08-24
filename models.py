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

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    thread_id = Column(String, nullable=True)

    questions = relationship("Question", back_populates="user")
    exams = relationship("Exam", back_populates="user")
    attempts = relationship("Attempt", back_populates="user")

class Exam(Base):
    __tablename__ = "exam"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    create_date = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="exams")
    questions = relationship("TestQuestion", back_populates="exam")

class TestQuestion(Base):
    __tablename__ = "test_question"

    id = Column(Integer, primary_key=True)
    exam_id = Column(Integer, ForeignKey("exam.id"))
    content = Column(Text, nullable=False)

    exam = relationship("Exam", back_populates="questions")
    choices = relationship("Choice", back_populates="question")

class Choice(Base):
    __tablename__ = "choice"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("test_question.id"))
    content = Column(Text, nullable=False)
    is_correct = Column(Boolean, nullable=False)

    question = relationship("TestQuestion", back_populates="choices")

class Attempt(Base):
    __tablename__ = "attempt"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    exam_id = Column(Integer, ForeignKey("exam.id"))
    score = Column(Integer, nullable=False)
    attempt_date = Column(DateTime, default=datetime.now())

    user = relationship("User", back_populates="attempts")
    exam = relationship("Exam")