from dataclasses import dataclass, field
from typing import List
from src.models.Vertex import Vertex
from src.models.Machine import Machine
from src.models.EdgeM import EdgeM

@dataclass
class VertexM(Vertex):
    is_entry: bool = False
    is_exit: bool = False
    
    edges: List[EdgeM] = field(default_factory=list) 
    machines: List[Machine] = field(default_factory=list)
    
