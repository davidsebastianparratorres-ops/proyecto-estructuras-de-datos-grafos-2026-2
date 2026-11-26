from dataclasses import dataclass
from src.models.Edge import Edge

@dataclass
class EdgeM(Edge):
    speed:float
    long: float
