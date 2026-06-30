from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.question import Question
from app.database.session import get_db

router = APIRouter(prefix="/questions", tags=["Questions"])


@router.get("/")
def get_all_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()


@router.get("/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):
    return db.query(Question).filter(Question.id == question_id).first()
