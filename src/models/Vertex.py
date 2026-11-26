from dataclasses import dataclass
from abc import ABC, abstractmethod

@dataclass
class Vertex(ABC):
    id:str
    x_coord:float
    y_coord:float
