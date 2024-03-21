import random
import threading
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .basemodel import Situation
from .crew import Crew

from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import json
import os


DATABASE_URL = "mysql+mysqlconnector://root:190703@localhost:3306/MyDatabase"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class SituationDB(Base):
    __tablename__ = 'situations'

    id = Column(Integer, primary_key = True, autoincrement = True)
    date = Column(String)
    observer = Column(String)
    source = Column(String)
    cause = Column(String)
    solver = Column(String)
    problem_gravity = Column(Integer)
    solved = Column(Boolean)


def count_executions(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        print(f"Function {func.__name__} has been executed {wrapper.count} times.")
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper

    
def init_status(squad: list, day: str, month: str, year: str) -> list: 
    source_options = ["System A", "System B", "System C", "System D", "External Module", "Backup System", "Communication Module"]
    cause_options = ["Malfunction", "Technical Glitch", "Human Error", "Software Bug", "Power Surge", "Sensor Failure", "Data Corruption"]
    situations = []
    
    for _ in range(random.randint(1, 5)):
        situations.append(Situation(
            date = init_date(day, month, year),
            observer = random.choice(squad)["profession"],
            source = random.choice(source_options),
            cause = random.choice(cause_options),
            solver = random.choice(squad)["profession"],
            problem_gravity = random.randint(1, 3),
            solved = True if random.random() <= 0.8 else False))
    
    return situations
        

def init_date(day: str, month: str, year: str) -> str: 
    month = random.randint(1, 12)
    year = int(year) if month >= int(month) else int(year) + 1
    
    if month in [4, 6, 9, 11]:
        if month == int(month) and year == int(year):
            day = random.randint(int(day), 30)
        elif month == int(month) and year == int(year) + 1:
            day = random.randint(1, int(day))
        else:
            day = random.randint(1, 30)
    elif month in [1, 3, 5, 7, 8, 10, 12]:
        if month == int(month) and year == int(year):
            day = random.randint(int(day), 31)
        elif month == int(month) and year == int(year) + 1:
            day = random.randint(1, int(day))
        else:
            day = random.randint(1, 31)
    else:
        leap_days =  29 if is_leap(int(year)) else 28

        if month == int(month) and year == int(year):
            day = random.randint(int(day), leap_days)
        elif month == int(month) and year == int(year) + 1:
            day = random.randint(1, int(day))
        else:
            day = random.randint(1, leap_days)
    
    return f"{day}.{month}.{year}"


def is_leap(year: int) -> bool: 
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        return True
    else:
        return False


def record(squad: dict, situations: list, date: list) -> None:
    session = SessionLocal()

    for sit in situations:
        situation_entry = SituationDB(
            date=sit.date,
            observer=sit.observer,
            source=sit.source,
            cause=sit.cause,
            solver=sit.solver,
            problem_gravity=sit.problem_gravity,
            solved=sit.solved
        )
        session.add(situation_entry)

    session.commit()
    session.close()  

    data = []
    loaded_data = []
    file_name = "record.json"
    data_dir = "data"
    file_path = os.path.join(data_dir, file_name)

    try:
        with open(file_path, "r") as json_file:
            loaded_data = json.load(json_file)
            print("File exists and has been loaded successfully.\n")
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except json.JSONDecodeError:
        print(f"The file '{file_path}' is not valid JSON.")

    if loaded_data:
        data.extend(loaded_data)

    sit_dict_list = []
    for sit in situations:

        sit_dict_list.append({
            "date": sit.date,
            "observer": sit.observer,
            "source": sit.source,
            "cause": sit.cause,
            "solver": sit.solver,
            "problem_gravity": sit.problem_gravity,
            "solved": sit.solved
        })

    data.append({
        "Cycle that started on": f"{date[0]}.{date[1]}.{date[2]}",
        "Has awaken following personnel": squad,
        "Situations encountered": sit_dict_list
    })
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    

def start(start_day: str, start_month: str, start_year: str, cycles: int) -> None: 
    small_cycle_record = []
    big_cycle_record = []
    combo_record = []
    
    year = start_year  
    
    for i in range(1, cycles + 1):
        if (i - 1) % 3 == 0:
            small_cycle_record=[] 
        if (i - 1) % 10 == 0:
            big_cycle_record=[] 
    
        squad = wake_up()
        
        thread1 = threading.Thread(target=check_small_record, args=(small_cycle_record, squad))
        thread2 = threading.Thread(target=check_big_record, args=(big_cycle_record, squad))

        thread1.start()
        thread2.start()

        for j in range(4):
            small_cycle_record.append(squad[j]["profession"])
            combo_record.append(squad[j]["profession"])

        big_cycle_record.append(combo_record)
        combo_record = []
        
        year = str(int(year) + 1)

        record(report_squad(squad), init_status(squad, start_day, start_month, year), [start_day, start_month, year])


def wake_up() -> list: 
    crew = Crew()
    squad = []
    squad.append(random.choice(crew.engineers))
    squad.append(random.choice(crew.researchers))
    squad.append(random.choice(crew.medics))
    squad.append(random.choice(crew.soldiers))
    return squad


def report_solving_rate()->dict: 
        session = SessionLocal()
        situations = session.query(SituationDB).all()

        if len(situations) == 0:
            return {"I got some good news": "there is nothing to report!"}
        else:
            solved_sits = 0
            for sit in situations:
                if sit.solved:
                    solved_sits += 1

            solved_rate = 100 * solved_sits / len(situations)

            rate = f"{round(solved_rate)} % |"

            for i in range(20):
                if i <= (solved_rate / 100) * 20:
                    rate += '*'
                else:
                    rate += ' '
            rate += ' '

            return {"We are doing good, we got a solving rate of": f"{rate}|"}


def report_squad(squad: list) -> dict:
    return {
        "Engineers": f"{squad[0]["nr_of"]} {squad[0]["profession"]}",
        "Researchers": f"{squad[1]["nr_of"]} {squad[1]["profession"]}",
        "Medics": f"{squad[2]["nr_of"]} {squad[2]["profession"]}",
        "Soldiers": f"{squad[3]["nr_of"]} {squad[3]["profession"]}"
        
    }


@count_executions   
def check_small_record(small_cycle_record: list, squad: list) -> None: 
    crew = Crew()
    while squad[0]["profession"] in small_cycle_record:
        squad[0] = random.choice(crew.engineers)

    while squad[1]["profession"] in small_cycle_record:
        squad[1] = random.choice(crew.researchers)

    while squad[2]["profession"] in small_cycle_record:
        squad[2] = random.choice(crew.medics)

    while squad[3]["profession"] in small_cycle_record:
        squad[3] = random.choice(crew.soldiers)


@count_executions   
def check_big_record(big_cycle_record: list, squad: list) -> None: 
    temp_squad = []
    for sq in squad:
        temp_squad.append(sq["profession"])

    for record in big_cycle_record:
        if set(temp_squad) == set(record):
            squad = wake_up()

            