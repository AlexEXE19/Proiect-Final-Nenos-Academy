from pydantic import BaseModel


class Situation(BaseModel):
    date: str
    observer: str
    source: str
    cause: str
    solver: str
    problem_gravity: int # 1-3
    solved: bool
 