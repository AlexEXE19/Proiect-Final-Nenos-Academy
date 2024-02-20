from pydantic import BaseModel


class Situation(BaseModel):
    date: str
    observer: str
    source: str
    cause: str
    solver: str
    problem_gravity: int # 1-3
    solved: bool
        
    def __str__(self):
        return f"{self.date}, {self.observer}, {self.source}, {self.cause}, {self.solver}, {self.problem_gravity}, {self.solved}\n"
    
        
