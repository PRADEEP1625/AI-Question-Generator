from sqlalchemy.orm import Session
from app.models.question import Question


def save_questions(
    db: Session, questions: list, topic: str, difficulty: str, model: str
) -> list:
    saved_questions = []

    for q in questions:
        question = Question(
            topic=topic,
            question_text=q["question"],
            option_a=q["option_a"],
            option_b=q["option_b"],
            option_c=q["option_c"],
            option_d=q["option_d"],
            correct_answer=q["correct_answer"],
            explanation=q.get("explanation"),
            difficulty=difficulty,
            ai_model=model,  # stores "llama3" or "gpt-4o-mini" here
        )
        db.add(question)
        saved_questions.append(question)

    db.commit()

    for question in saved_questions:
        db.refresh(question)

    return saved_questions
