from pydantic import BaseModel, Field


class Situation(BaseModel):
    date: str
    observer: str
    source: str
    cause: str
    solver: str
    problem_gravity: int # 1-3
    solved: bool
 

class DepartureDate(BaseModel):
    day: int = Field(..., ge=1, le=30, description="The day has to be a number between 1 and 30!")
    month: int = Field(..., ge=1, le=12, description="The month has to be a number between 1 and 12!")
    year: int


class NrOfCycles(BaseModel):
    nr_cycles: int = Field(..., gt=0, description="The number of cycles has to be greater than 0!")

