import random
import threading
import time
import os
import sys
import json

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data.database import save
from .basemodel import Situation
from .crew import Crew

def count_executions(func):
    def wrapper(*args, **kwargs):
        wrapper.count += 1
        print(f"Function {func.__name__} has been executed {wrapper.count} times.")
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper


class Departure():
    def __init__(self)->None:
        self.config()
        thread = threading.Thread(target = self.departure)
        thread.start()
        thread.join()
        
        save() # saves every situation into the database
    

    def config(self)->None: # initialize the date and number of cycles atributes with inputs from the user
        print("Greetings! This is ISS Legacy super-smart Artificial Intelligence terminal, please, tell me, what's the planned date of departuring Earth!")
        
        self.departure_day = input("Day: ")
        self.departure_month = input("Month: ")
        self.departure_year = input("Year: ")

        while (
            self.departure_day is None or 
            self.departure_month is None or 
            self.departure_year is None or 
            int(self.departure_day) < 1 or 
            int(self.departure_day) > 31 or 
            int(self.departure_month) < 1 or 
            int(self.departure_month) > 12 or 
            int(self.departure_year) < 1
        ):
            print("No need to rush! Make sure you cover all fields and assign proper inputs for them!")
            
            self.departure_day = input("Day: ")
            self.departure_month = input("Month: ")
            self.departure_year = input("Year: ")

        print(f"Your chosen date of departure shall be: {self.departure_day}.{self.departure_month}.{self.departure_year}\nSee y'all on the desk!")

        self.cycles = input("Now I need one more thing from you. How many cycles of de-cryogenization may I conduct?\n"
                        "PS: If you let the field clear then I will perform unlimited ones until someone will shut me up, they can do that every 3rd cycle.\n"
                        "Cycles: ")
        
        self.cycles = 999 if self.cycles == "" else int(self.cycles)
        
        if self.cycles == 0:
            print("Off, make sure to wake me up when you're ready!\nGoodbye!")
        elif self.cycles < 0:
            self.cycles *= -1
        else:
            print(f"I will carry out {self.cycles} cycles.\nBuckle up!")

        
    def init_status(self)->None: # initliaze situations that could occur on the ship for each cycle
        self.source_options = ["System A", "System B", "System C", "System D", "External Module", "Backup System", "Communication Module"]
        self.cause_options = ["Malfunction", "Technical Glitch", "Human Error", "Software Bug", "Power Surge", "Sensor Failure", "Data Corruption"]
        
        self.situations = []
        
        for _ in range(random.randint(0, 5)):
            self.situations.append(Situation(date = self.init_date(),
                                         observer = random.choice(self.squad)["profession"],
                                         source = random.choice(self.source_options),
                                         cause = random.choice(self.cause_options),
                                         solver = random.choice(self.squad)["profession"],
                                         problem_gravity = random.randint(1, 3),
                                         solved = True if random.random() <= 0.8 else False))
            

    def init_date(self)->str: # initialize a random date for the situation encountered
        month = random.randint(1, 12)
        year = int(self.departure_year) if month >= int(self.departure_month) else int(self.departure_year) + 1
        
        if month in [4, 6, 9, 11]:
            if month == int(self.departure_month) and year == int(self.departure_year):
                day = random.randint(int(self.departure_day), 30)
            elif month == int(self.departure_month) and year == int(self.departure_year) + 1:
                day = random.randint(1, int(self.departure_day))
            else:
                day = random.randint(1, 30)

        elif month in [1, 3, 5, 7, 8, 10, 12]:
            if month == int(self.departure_month) and year == int(self.departure_year):
                day = random.randint(int(self.departure_day), 31)
            elif month == int(self.departure_month) and year == int(self.departure_year) + 1:
                day = random.randint(1, int(self.departure_day))
            else:
                day = random.randint(1, 31)

        else:
            leap_days =  29 if self.is_leap(int(self.departure_year)) else 28

            if month == int(self.departure_month) and year == int(self.departure_year):
                day = random.randint(int(self.departure_day), leap_days)
            elif month == int(self.departure_month) and year == int(self.departure_year) + 1:
                day = random.randint(1, int(self.departure_day))
            else:
                day = random.randint(1, leap_days)
        
        return f"{day}.{month}.{year}"


    def is_leap(self, year: int)->bool: # checks if a specific year is leap or not
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return True
        else:
            return False


    def record(self)->None: # records the situations occured into the json file
        data = []
        file_name = "recorded_situations.json"
        data_dir = "data"

        file_path = os.path.join(data_dir, file_name)
        
        try:
            with open(file_path, "r") as json_file:
                data = json.load(json_file)
                print("File exists and has been loaded successfully.\n")
        except FileNotFoundError:
            print(f"The file '{file_path}' does not exist.")
        except json.JSONDecodeError:
            print(f"The file '{file_path}' is not valid JSON.")

        for sit in self.situations:
            dict = {"date": sit.date, "observer": sit.observer, "source": sit.source, "cause": sit.cause, "solver": sit.solver, "problem_gravity": sit.problem_gravity, "solved": sit.solved}
            data.append(dict)
        
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent = 4)


    def departure(self)->None: # executes the loop to initialize all cycles
        small_cycle_record = []
        big_cycle_record = []
        combo_record = []
        situations = []

        for i in range(1, self.cycles + 1):
            print(f"Initializing cycle number {i} at {self.departure_day}.{self.departure_month}.{self.departure_year}\nDe-cryogenization process is starting.")
            time.sleep(1)

            if (i - 1) % 3 == 0:
                small_cycle_record=[] # recording every profession awoken for every 3 cycles
                

            if (i - 1) % 10 == 0:
                big_cycle_record=[] # recording every squad combo awoken for every 10 cycles
        
            self.de_crio()
            self.init_status()
            
            self.check_small_record(small_cycle_record)
            self.check_big_record(big_cycle_record)

            for j in range(4):
                small_cycle_record.append(self.squad[j]["profession"])
                combo_record.append(self.squad[j]["profession"])

            big_cycle_record.append(combo_record)
            combo_record = []
            
            
            print("Current cycle has awoken the following personnel:\n")
            print(f"Engineers: {self.squad[0]["nr_of"]} {self.squad[0]["profession"]}\n")
            print(f"Researchers: {self.squad[1]["nr_of"]} {self.squad[1]["profession"]}\n")
            print(f"Medics: {self.squad[2]["nr_of"]} {self.squad[2]["profession"]}\n")
            print(f"Soldiers: {self.squad[3]["nr_of"]} {self.squad[3]["profession"]}\n")

            self.departure_year = str(int(self.departure_year) + 1)
            self.record()
            situations.extend(self.situations)

            if i >= 3 and i % 3 == 0:
                print("It's been a while since we've seen each other.\n"
                        "Now, tell me what to do next: (R) for report, (C) for continue or (Q) to stop.\nPS: I'm not case sensitive")
                option = input()
                option = option.upper()

                while option not in ['R', 'C', 'Q']:
                    print("C'mon, I know you can do it!\nLet's try again.\nPS: Remember magic letters RCQ")
                    option=input()
                    option=option.upper()

                if option == 'Q':
                    print("Bye bye!")
                    break
                elif option == 'C':
                    print("See ya in 3 years!")
                elif option == 'R':
                    if self.report(situations) == 'C':
                        print("See ya in 3 years!")
                    else:
                        print("Bye bye!")
                        break
    

    def de_crio(self)->None: # initialize the squad
        self.crew = Crew()
        self.squad = []
        self.squad.append(random.choice(self.crew.engineers))
        self.squad.append(random.choice(self.crew.researchers))
        self.squad.append(random.choice(self.crew.medics))
        self.squad.append(random.choice(self.crew.soldiers))


    def report(self, situations: list)->str: # prints the percentage of solved situations unless the situations list is empty
            if len(situations) == 0:
                print("I got some good news, there is nothing to report!\nI am nonetheless all ears to every situation that might occur.")
            else:
                solved_sits = 0
                for sit in situations:
                    if sit.solved:
                        solved_sits += 1

                solved_rate = 100 * solved_sits / len(situations)

                print("We are doing good, we got a solving rate of:")
                print(f'{round(solved_rate)} % |', end = '')

                for i in range(20):
                    if i <= (solved_rate / 100) * 20:
                        print('*', end = '')
                    else:
                        print(' ', end = '')
                print('|')
            
            print("What's next?\nPS: (C) for continue or (Q) to stop.")

            option = input()
            option = option.upper()

            while option not in ['C', 'Q']:
                print("C'mon, I know you can do it!\nLet's try again.\nPS: Remember magic letters CQ")
                option = input()
                option = option.upper()

            return option


    @count_executions   
    def check_small_record(self, small_cycle_record: list)->None: # checks if the awoken personnel has already been awoken on its series of 3 cycles if so, it initializes a new squad that would satisfy the condition
        while self.squad[0]["profession"] in small_cycle_record:
            self.squad[0] = random.choice(self.crew.engineers)

        while self.squad[1]["profession"] in small_cycle_record:
            self.squad[1] = random.choice(self.crew.researchers)

        while self.squad[2]["profession"] in small_cycle_record:
            self.squad[2] = random.choice(self.crew.medics)

        while self.squad[3]["profession"] in small_cycle_record:
            self.squad[3] = random.choice(self.crew.soldiers)


    @count_executions   
    def check_big_record(self, big_cycle_record: list)->None: # checks if the awoken squad combination has already been awoken in the same format on its series of 10 cycles if so, it initializes a new squad that would satisfy the condition
        temp_squad = []
        for sq in self.squad:
            temp_squad.append(sq["profession"])

        for record in big_cycle_record:
            if set(temp_squad) == set(record):
                self.de_crio()
            