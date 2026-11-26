from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Vertex(ABC):
    id:str
    x_coord:int
    y_coord:int
