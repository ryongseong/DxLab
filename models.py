from sqlalchemy import Integer, String, Column, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base

class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=True)
    subject = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    create_date = Column(DateTime, nullable=False)
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