from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Annotated
import models
from database import engine, session_local
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ChoiceBase(BaseModel):
    choice_text: str 
    is_correct: bool


class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]


def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]



@app.get("/question")
async def get_question(db: db_dependency):
    result = db.query(models.Questions).all()
    if result:
        return result
    raise HTTPException(status_code=404, detail="Questão não encontrada")


@app.get("/question/{id}")
async def get_question(id: int, db: db_dependency):
    result = db.query(models.Questions).filter(models.Questions.id == id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Questão não encontrada")
    return  result


@app.post("/questions")
async def create_questions(question: QuestionBase, db: db_dependency):
    db_question = models.Questions(question_text=question.question_text)
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    for choice in question.choices:
        db_choice = models.Choices(choice_text=choice.choice_text, is_correct=choice.is_correct, question_id=db_question.id)