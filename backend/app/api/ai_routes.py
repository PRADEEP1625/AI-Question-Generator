from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.question_schema import TopicEnum, DifficultyEnum
from app.services.ollama_service import generate_questions
from app.services.question_service import save_questions
from app.database.session import get_db

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/generate")
def generate(
    topic: TopicEnum,
    difficulty: DifficultyEnum = DifficultyEnum.medium,
    count: int = 10,
    model: str = "openai/gpt-4o-mini",
    db: Session = Depends(get_db),
):

    questions = generate_questions(
        topic=topic.value, difficulty=difficulty.value, count=count, model=model
    )

    save_questions(
        db=db,
        questions=questions,
        topic=topic.value,
        difficulty=difficulty.value,
        model=model,
    )

    return questions
