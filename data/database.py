from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import os


DATABASE_URL = "mysql+mysqlconnector://root:190703@localhost:3306/MyDatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)
Base = declarative_base()

class Situation(Base):
    __tablename__ = 'situations'

    id = Column(Integer, primary_key = True, autoincrement = True)
    date = Column(String)
    observer = Column(String)
    source = Column(String)
    cause = Column(String)
    solver = Column(String)
    problem_gravity = Column(Integer)
    solved = Column(Boolean)

def save():
    session = SessionLocal()
    file_name = "recorded_situations.json"
    data_dir = "data"

    file_path = os.path.join(data_dir, file_name)

    try:
        with open(file_path, 'r') as file:
            json_data = json.load(file)

        for data in json_data:
            situation = Situation(
                date = data['date'],
                observer = data['observer'],
                source = data['source'],
                cause = data['cause'],
                solver = data['solver'],
                problem_gravity = data['problem_gravity'],
                solved = data['solved']
            )
            session.add(situation)

        session.commit()
        session.close()
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON in file '{file_path}': {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


