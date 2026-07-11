from dataclasses import dataclass, field
@dataclass
class Constructor:
    constructorId : int
    constructorRef : str
    name : str
    nationality : str
    url : str

    results: dict = field(default_factory=dict)
    resultsNull: dict = field(default_factory=dict)# <-- attributo-dizionario (MAI = {} in una dataclass)

    def __hash__(self):
        return self.constructorId  # hash sulla SOLA chiave identificativa

    def __eq__(self, other):
        return self.constructorId == other.constructorId

    def __str__(self):
        return f"{self.constructorId}, {self.name}, [{self.nationality}]"