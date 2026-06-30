from sqlalchemy import Column, Integer, String, Text
from app.database.db import Base


class Question(Base):
    __tablename__ = "question"

    id = Column(Integer, primary_key=True, index=True)

    topic = Column(String(255), nullable=False)

    question_text = Column(Text, nullable=False)

    option_a = Column(Text, nullable=False)

    option_b = Column(Text, nullable=False)

    option_c = Column(Text, nullable=False)

    option_d = Column(Text, nullable=False)

    correct_answer = Column(String(5), nullable=False)

    explanation = Column(Text)

    difficulty = Column(String(50), default="Medium")

    ai_model = Column(String(100), default="Ollama")
