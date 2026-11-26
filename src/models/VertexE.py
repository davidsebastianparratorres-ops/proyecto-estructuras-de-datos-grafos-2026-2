from dataclasses import dataclass,field
from src.models.Vertex import Vertex
from typing import List
from src.models.Vertex import Vertex
from src.models.Soldier import Soldier

@dataclass
class VertexE(Vertex):
    soldiers: List[Soldier] = field(default_factory=list)
    
