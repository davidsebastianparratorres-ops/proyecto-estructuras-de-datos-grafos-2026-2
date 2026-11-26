from dataclasses import dataclass
from src.models.Edge import Edge


@dataclass
class Road(Edge):
    walk_time:float
    moto_time:float