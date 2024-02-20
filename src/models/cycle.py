from .basemodel import Situation
from .crew import Crew
import random

def count_executions(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        print(f"Function {func.__name__} has been executed {wrapper.count} times.")
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper

class Cycle():

    def __init__(self, date: list)->None:
        
        self.source_options = ["System A", "System B", "System C", "System D", "External Module", "Backup System", "Communication Module"]
        self.cause_options = ["Malfunction", "Technical Glitch", "Human Error", "Software Bug", "Power Surge", "Sensor Failure", "Data Corruption"]
        self.deCrio()
        self.initStatus(date)
    
    def deCrio(self)->None:
        self.crew=Crew()
        self.squad=[]
        self.squad.append(random.choice(self.crew.engineers))
        self.squad.append(random.choice(self.crew.researchers))
        self.squad.append(random.choice(self.crew.medics))
        self.squad.append(random.choice(self.crew.soldiers))
        

    def initStatus(self, date_p: list)->None:
        self.situations=[]
        
        for _ in range(random.randint(0,5)):
            self.situations.append(Situation(date=self.initDate(date_p),
                                         observer=random.choice(self.squad)["profession"],
                                         source=random.choice(self.source_options),
                                         cause=random.choice(self.cause_options),
                                         solver=random.choice(self.squad)["profession"],
                                         problem_gravity=random.randint(1,3),
                                         solved=True if random.random()<=0.8 else False))
            
    @count_executions   
    def check_small_record(self, small_cycle_record: list)->None:
        
        while self.squad[0]["profession"] in small_cycle_record:
            self.squad[0]=random.choice(self.crew.engineers)

        while self.squad[1]["profession"] in small_cycle_record:
            self.squad[1]=random.choice(self.crew.researchers)

        while self.squad[2]["profession"] in small_cycle_record:
            self.squad[2]=random.choice(self.crew.medics)

        while self.squad[3]["profession"] in small_cycle_record:
            self.squad[3]=random.choice(self.crew.soldiers)

    @count_executions   
    def check_big_record(self, big_cycle_record: list)->None:
        temp_squad=[]
        for sq in self.squad:
            temp_squad.append(sq["profession"])

        for record in big_cycle_record:
            if set(temp_squad)==set(record):
                self.deCrio()
            
    
    
    def isLeap(self, year: int)->bool:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return True
        else:
            return False

    def initDate(self, date: list)->str:
        
        month=random.randint(1,12)
        year=int(date[2]) if month>=int(date[1]) else int(date[2])+1
        
        if month in [4,6,9,11]:
            if month==int(date[1]) and year==int(date[2]):
                day=random.randint(int(date[0]), 30)
            elif month==int(date[1]) and year==int(date[2])+1:
                day=random.randint(1, int(date[0]))
            else:
                day=random.randint(1,30)
        elif month in [1,3,5,7,8,10,12]:
            if month==int(date[1]) and year==int(date[2]):
                day=random.randint(int(date[0]), 31)
            elif month==int(date[1]) and year==int(date[2])+1:
                day=random.randint(1, int(date[0]))
            else:
                day=random.randint(1,31)
        else:
            leap_days=29 if self.isLeap(int(date[2])) else 28

            if month==int(date[1]) and year==int(date[2]):
                day=random.randint(int(date[0]), leap_days)
            elif month==int(date[1]) and year==int(date[2])+1:
                day=random.randint(1, int(date[0]))
            else:
                day=random.randint(1,leap_days)
        
        return f"{day}.{month}.{year}"
       
        

    
    def __str__(self) -> str:
        info = "Current cycle has awoken the following personnel:\n"
        info+=f"Engineers: {self.squad[0]["nr_of"]} {self.squad[0]["profession"]}\n"
        info+=f"Researchers: {self.squad[1]["nr_of"]} {self.squad[1]["profession"]}\n"
        info+=f"Medics: {self.squad[2]["nr_of"]} {self.squad[2]["profession"]}\n"
        info+=f"Soldiers: {self.squad[3]["nr_of"]} {self.squad[3]["profession"]}\n"

        return info + "\n"


        


        
    