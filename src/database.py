from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.basemodel import Situation  
import json

def save():
    DATABASE_URL = "mysql+mysqlconnector://root:190703@localhost:3306/MyDatabase"
    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()

    with open('proj.data.recorded_situations.json', 'r') as file:
        json_data = json.load(file)

    for data in json_data:
        situation = Situation(
            date=data['date'],
            observer=data['observer'],
            source=data['source'],
            cause=data['cause'],
            solver=data['solver'],
            problem_gravity=data['problem_gravity'],
            solved=data['solved']
        )
        session.add(situation)

    session.commit()
    session.close()
