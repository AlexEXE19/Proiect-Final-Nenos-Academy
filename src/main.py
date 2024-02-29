
from models.cycle import Cycle
import threading
import time
import json



def config()->list:
    print("Greetings! This is ISS Legacy super-smart Artificial Intelligence terminal, please, tell me, what's the planned date of departuring Earth!")
    day=input("Day: ")
    month=input("Month: ")
    year=input("Year: ")

    while day is None or month is None or year is None or int(day)<1 or int(day) >31 or int(month)<1 or int(month) >12 or int(year)<1:
        print("No need to rush! Make sure you cover all fields and assign proper inputs for them!")
        day=input("Day: ")
        month=input("Month: ")
        year=input("Year: ")
    print(f"Your chosen date of departure shall be: {day}.{month}.{year}\nSee y'all on the desk!")
    cycles=input("Now I need one more thing from you. How many cycles of de-cryogenization may I conduct?\n"
                     "PS: If you let the field clear then I will perform unlimited ones until someone will shut me up, they can do that every 3rd cycle.\n"
                     "Cycles: ")
    cycles=999 if cycles=="" else int(cycles)
    
    if cycles==0:
        print("Off, make sure to wake me up when you're ready!\nGoodbye!")
    elif cycles<0:
        cycles*=-1
    else:
        print(f"I will carry out at least {cycles} cycles.\nBuckle up!")

    return [day,month,year, str(cycles)]


def report(situations: list)->str:

    if len(situations) == 0:
        print("I got some good news, there is nothing to report!\nI am nonetheless all ears to every situation that might ocurr.")
    else:
        solved_sits=0
        for sit in situations:
            if sit.solved:
                solved_sits+=1

        solved_rate=100*solved_sits/len(situations)

        print("We are doing good, we got a solving rate of:")
        print(f'{round(solved_rate)} % |', end='')
        for i in range(20):
            if i<=(solved_rate/100)*20:
                print('*',end='')
            else:
                print(' ',end='')
        print('|')
    
    print("What's next?\nPS: (C) for continue or (Q) to stop.")
    option=input()
    option=option.upper()

    while option not in ['C','Q']:
        print("C'mon, I know you can do it!\nLet's try again.\nPS: Remember magic letters CQ")
        option=input()
        option=option.upper()

    return option
        

def departure(cycles: int, date: list)->None:

    small_cycle_record=[]
    big_cycle_record=[]
    combo_record=[]
    situations=[]

    for i in range(1, cycles+1):
        print(f"Initializing cycle number {i} at {date[0]}.{date[1]}.{date[2]}\nDe-cryogenization process is starting.")
        time.sleep(2)

        if (i-1)%3==0:
            
            small_cycle_record=[] # recording every profession awaken for every 3 cycles
            if i>=3:
                
                print("It's been a while since we've seen each other.\n"
                      "Now, tell me what to do next: (R) for report, (C) for continue or (Q) to stop.\nPS: I'm not case sensitive")
                option=input()
                option=option.upper()

                while option not in ['R','C','Q']:
                    print("C'mon, I know you can do it!\nLet's try again.\nPS: Remember magic letters RCQ")
                    option=input()
                    option=option.upper()

                if option == 'Q':
                    print("Bye bye!")
                    i=cycles+1
                    continue
                elif option == 'R':
                    if report(situations)=='C':
                        print("See ya in 3 years!")
                    else:
                        print("Bye bye!")
                        i=cycles+1
                        continue
                    
                elif option == 'C':
                    print("See ya in 3 years!")


        if (i-1)%10==0:
            big_cycle_record=[] # recording every squad combo awaken for every 10 cycles
    
        
        cycle=Cycle(date)
        
        cycle.check_small_record(small_cycle_record)
        cycle.check_big_record(big_cycle_record)

        for j in range(4):
            small_cycle_record.append(cycle.squad[j]["profession"])
            combo_record.append(cycle.squad[j]["profession"])

        big_cycle_record.append(combo_record)
        combo_record=[]
        
        
        print("Current cycle has awoken the following personnel:\n")
        print(f"Engineers: {cycle.squad[0]["nr_of"]} {cycle.squad[0]["profession"]}\n")
        print(f"Researchers: {cycle.squad[1]["nr_of"]} {cycle.squad[1]["profession"]}\n")
        print(f"Medics: {cycle.squad[2]["nr_of"]} {cycle.squad[2]["profession"]}\n")
        print(f"Soldiers: {cycle.squad[3]["nr_of"]} {cycle.squad[3]["profession"]}\n")

        date[2]=str(int(date[2])+1)
        record(cycle)
        situations.extend(cycle.situations)
        

def record(cycle: Cycle)->None:
    
    data=[]
    file_path = "proj.data.recorded_situations.json"
    
    try:
        with open(file_path, "r") as json_file:
            data = json.load(json_file)
            print("File exists and has been loaded successfully.")
    except FileNotFoundError:
        print(f"The file '{file_path}' does not exist.")
    except json.JSONDecodeError:
        print(f"The file '{file_path}' is not valid JSON.")

    for sit in cycle.situations:
        dict={"date":sit.date,"observer":sit.observer,"source":sit.source,"cause":sit.cause,"solver":sit.solver,"problem_gravity":sit.problem_gravity,"solved":sit.solved}
        data.append(dict)
    

    with open(file_path,'w') as json_file:
        json.dump(data,json_file,indent=4)

    



def main():
    input_data = config()
    cycles = int(input_data[-1])
    thread=threading.Thread(target=departure, args=(cycles, input_data[:-1]))
    thread.start()
    thread.join()
     
    

if __name__=="__main__":
    main()
