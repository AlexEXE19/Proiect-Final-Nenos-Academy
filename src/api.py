from fastapi import FastAPI, HTTPException, Query
from sqlalchemy import Column, Integer, String, Boolean, func, create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models.crew import Crew
from models.basemodel import Situation
from pydantic import BaseModel


Base = declarative_base()

class SituationDB(Base):
    __tablename__ = 'situations'

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String)
    observer = Column(String)
    source = Column(String)
    cause = Column(String)
    solver = Column(String)
    problem_gravity = Column(Integer)
    solved = Column(Boolean)

class SituationUpdate(BaseModel):
    solved: bool

app = FastAPI()

DATABASE_URL = "mysql+mysqlconnector://root:190703@localhost:3306/MyDatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.get("/")
async def read_root():
    return {"Welcome": "aboard!"}

@app.get("/personnel/")
async def read_personnel():
    crew = Crew()
    return {"Engineers": crew.engineers, "Researchers": crew.researchers, "Medics": crew.medics, "Soldiers": crew.soldiers}

@app.get("/situations/")
async def read_situations(solved: bool = Query(None)):
    session = SessionLocal()

    if solved is not None:
        situations = session.query(SituationDB).filter(SituationDB.solved == solved).all()
    else:
        situations = session.query(SituationDB).all()

    session.close()

    return [{"date": situation.date, "observer": situation.observer, "source": situation.source, "cause": situation.cause, "solver": situation.solver, "problem_gravity": situation.problem_gravity, "solved": situation.solved} for situation in situations]

@app.delete("/situations/clean/")
async def delete_solved_situations(delete_all: bool = Query(False)):
    session = SessionLocal()

    if delete_all:
        session.query(SituationDB).delete()
    else:
        session.query(SituationDB).filter(SituationDB.solved == True).delete(synchronize_session=False)
    
    session.commit()

    count = session.query(func.count()).select_from(SituationDB).scalar()

    if count > 0:
        query = text("ALTER TABLE sitations AUTO_INCREMENT = 1")
        session.execute(query)
        session.commit()
    
    session.close()

    return {"message": "Solved situations have been deleted succesfully"}

@app.post("/situations/add/")
async def add_situation(situation: Situation):
    session = SessionLocal()

    new_situation = SituationDB(
        date=situation.date,
        observer=situation.observer,
        source=situation.source,
        cause=situation.cause,
        solver=situation.solver,
        problem_gravity=situation.problem_gravity,
        solved=situation.solved
    )

    session.add(new_situation)
    session.commit()

    session.close()

    return {"message":"Situation has been added successfully"}
    
@app.put("/situations/update/{situation_id}/")
async def update_situation(situation_id: int, situation_update: SituationUpdate):
    session = SessionLocal()

    db_situation = session.query(SituationDB).filter(SituationDB.id == situation_id).first()
   
    if db_situation is None:
        raise HTTPException(status_code=404, detail="Situation not found")

    db_situation.solved = situation_update.solved

    session.commit()
    session.close()

    return {"message": "Situation has been updated successfully"}

