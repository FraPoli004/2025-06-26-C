from dataclasses import dataclass, field


@dataclass
class Piazzamento:
    raceId: int
    driverId: int
    position: int



    def __hash__(self):
        return hash(self.raceId+self.driverId)                       # hash sulla SOLA chiave identificativa

    def __eq__(self, other):
        return self.raceId == other.raceId and self.driverId == other.driverId

    def __str__(self):
        return f"gara:{self.raceId}, driver:{self.driverId}, posizionamento: {self.position}"                       # come appare in stampe e dropdown
