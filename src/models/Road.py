from dataclasses import dataclass
from src.models.Edge import Edge


@dataclass
class Road(Edge):
    time:float