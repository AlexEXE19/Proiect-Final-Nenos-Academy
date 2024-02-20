import random


class Crew():
    def __init__(self)->None:
        self.engineers: list
        self.researchers: list
        self.medics: list
        self.soldiers: list
        self.init_crew()

    def init_crew(self)->None:
        self.engineers=[{"profession": "IT","nr_of":random.randint(1,3)},{"profession":"Mechanics","nr_of":random.randint(1,3)},{"profession":"Aeronautics","nr_of":random.randint(1,3)}]
        self.researchers=[{"profession":"Psychologists","nr_of":random.randint(1,3)},{"profession":"Biologists","nr_of":random.randint(1,3)},{"profession":"Astronomeers","nr_of":random.randint(1,3)}]
        self.medics=[{"profession":'Assistants',"nr_of":random.randint(1,3)},{"profession":'General Practitioners',"nr_of":random.randint(1,3)},{"profession":'Neurologists',"nr_of":random.randint(1,3)}]
        self.soldiers=[{"profession":'Level 1',"nr_of":random.randint(1,3)},{"profession":'Level 2',"nr_of":random.randint(1,3)},{"profession":'Level 3',"nr_of":random.randint(1,3)}]

    def __str__(self) -> str:
        pass
  

