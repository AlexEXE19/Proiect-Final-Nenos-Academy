from fastapi import FastAPI, HTTPException, Query, Path
from sqlalchemy import func, create_engine, text
from sqlalchemy.orm import sessionmaker
from models.basemodel import Situation, DepartureDate, NrOfCycles 
from models.module import SituationDB, start, report_solving_rate
import json
import os


app = FastAPI()

DATABASE_URL = "mysql+mysqlconnector://root:190703@localhost:3306/mydatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@app.get("/")
async def read_root():
    return {"Greetings! This is ISS Legacy super-smart Artificial Intelligence terminal!": "Please, tell me, what' the number of cycles of decriogenization and the departuring date!"}


@app.put("/start/")
async def put_departure_date(date: DepartureDate, cycles: NrOfCycles):
    start(date.day, date.month, date.year, cycles.nr_cycles)
    return {
        "I can't wait to power up my reactors on": {
            "day": date.day,
            "month": date.month,
            "year": date.year
        }, 
        "I will wake up proper personnel within these number of cycles": cycles.nr_cycles
    }


@app.get("/report/{report_type}")
async def get_report_from_cycles(report_type: str=Path(...)):
    if report_type == "full_report":
        file_name = "record.json"
        data_dir = "data"
        file_path = os.path.join(data_dir, file_name)

        try:
            with open(file_path, 'r') as file:
                json_data = json.load(file)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file '{file_path}': {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

        return json_data
    
    elif report_type == "summed_report":
        return report_solving_rate()
    
    else:
        return {"Warning!": f"Invalid report type: {report_type}, try full_report / summed_report"}


@app.get("/situations/{date}")
async def read_situation_by_date(date: str=Path(...)):
        with SessionLocal() as session:
            situation = session.query(SituationDB).filter(SituationDB.date==date).first()
            
            if situation is None:
                return {"Warning!": "Situation not found"}
            
            return {
                "date": situation.date,
                "observer": situation.observer,
                "source": situation.source,
                "cause": situation.cause,
                "solver": situation.solver,
                "problem_gravity": situation.problem_gravity,
                "solved": situation.solved
            }
        

@app.get("/situations/")
async def read_situations(
    solved: bool=Query(None),
    problem_gravity: int=Query(None),
    by_date: str=Query(None)
):
    with SessionLocal() as session:
        query = session.query(SituationDB)

        if solved is not None:
            query = query.filter(SituationDB.solved == solved)

        if problem_gravity is not None:
            query = query.filter(SituationDB.problem_gravity == problem_gravity)

        situations = query.all()

        if by_date == "ascending":
            situations = sorted(
                situations,
                key=lambda situation: tuple(map(int, situation.date.split('.')[::-1]))
            )
        elif by_date == "descending":
                situations = sorted(
                situations,
                key=lambda situation: tuple(map(int, situation.date.split('.')[::-1]))
            )
                situations.reverse()

        return [
            {
                "date": situation.date,
                "observer": situation.observer,
                "source": situation.source,
                "cause": situation.cause,
                "solver": situation.solver,
                "problem_gravity": situation.problem_gravity,
                "solved": situation.solved
            } for situation in situations
        ]
    

@app.delete("/situations/clean/")
async def delete_situations(delete_all: bool=Query(False)):
    session = SessionLocal()

    if delete_all:
        session.query(SituationDB).delete()
    else:
        session.query(SituationDB).filter(SituationDB.solved==True).delete(synchronize_session=False)
    
    session.commit()

    count = session.query(func.count()).select_from(SituationDB).scalar()

    if count > 0:
        query = text("ALTER TABLE situations AUTO_INCREMENT = 1")
        session.execute(query)
        session.commit()
    
    session.close()

    if delete_all:
        return {"Message": "All situations have been deleted succesfully"}
    else:
        return {"Message": "Solved situations have been deleted succesfully"}


@app.post("/situations/add/")
async def add_situation(situation: Situation):
    session = SessionLocal()

    new_situation = SituationDB(
        date = situation.date,
        observer = situation.observer,
        source = situation.source,
        cause = situation.cause,
        solver = situation.solver,
        problem_gravity = situation.problem_gravity,
        solved = situation.solved
    )

    session.add(new_situation)
    session.commit()

    session.close()

    return {"Message":"Situation has been added successfully"}

 
@app.put("/situations/update/{date}/")
async def update_situation(situation_update: Situation, date: str=Path(...)):
    session = SessionLocal()

    db_situation = session.query(SituationDB).filter(SituationDB.date==date).first()
   
    if db_situation is None:
        raise HTTPException(status_code=404, detail="Situation not found")

    db_situation.date = situation_update.date
    db_situation.observer = situation_update.observer
    db_situation.source = situation_update.source
    db_situation.cause = situation_update.cause
    db_situation.solver = situation_update.solver
    db_situation.problem_gravity = situation_update.problem_gravity
    db_situation.solved = situation_update.solved

    session.commit()
    session.close()

    return {"Message": "Situation has been updated successfully"}

