import datetime

from pydantic import BaseModel, field_validator

from domain.answer.answer_schema import Answer

class Question(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []


class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject', 'content')
    def not_empry(cls, v):
        if not v or not v.strip():
            raise ValueError('빈값 금지')
        return v