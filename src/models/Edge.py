from abc import ABC
from dataclasses import dataclass

@dataclass

class Edge(ABC):
    id:str
    destiny:str