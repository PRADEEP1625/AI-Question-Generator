from fastapi import FastAPI

from app.database.db import Base, engine
from app.models.question import Question
from app.api.ai_routes import router as ai_router
from app.api.questions_routes import router as questions_router

app = FastAPI(title="AI Question Generator API", version="1.0.0")

Base.metadata.create_all(bind=engine)

app.include_router(ai_router)
app.include_router(questions_router)


@app.get("/")
def root():
    return {"message": "AI Question Generator API Running"}
