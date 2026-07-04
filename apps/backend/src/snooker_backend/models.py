from pydantic import BaseModel


class Result(BaseModel):
    id: int
    created_at: str
    date: str
    opponent_name: str
    score: int
    opponent_score: int
    high_break: int
