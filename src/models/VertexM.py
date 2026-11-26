from dataclasses import dataclass, field
from typing import List
from src.models.Vertex import Vertex
from src.models.EdgeM import EdgeM
from src.models.Machine import Machine

@dataclass
class VertexM(Vertex):
    is_entry: bool = False
    is_exit: bool = False
    # Adjacency list of corridors (EdgeM) connected to this intersection
    edges: List[EdgeM] = field(default_factory=list)
    
    # Enemy convoy units currently located at this intersection
    machines: List[Machine] = field(default_factory=list)
    
