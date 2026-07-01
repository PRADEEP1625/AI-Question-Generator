from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.question_schema import DifficultyEnum, ModelEnum
from app.services.ai_service import generate_questions
from app.services.question_service import save_questions
from app.database.session import get_db

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/generate")
def generate(
    topic: str,
    difficulty: DifficultyEnum = DifficultyEnum.medium,
    count: int = 10,
    model: Optional[ModelEnum] = None,
    db: Session = Depends(get_db),
):
    selected_model = model.value if model else ModelEnum.llama3.value

    questions = generate_questions(
        topic=topic,
        difficulty=difficulty.value,
        count=count,
        model=selected_model,
    )

    save_questions(
        db=db,
        questions=questions,
        topic=topic,
        difficulty=difficulty.value,
        model=selected_model,
    )

    return questions
