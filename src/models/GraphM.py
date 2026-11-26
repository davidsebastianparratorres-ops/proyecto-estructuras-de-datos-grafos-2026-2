from dataclasses import dataclass,field
from src.models.VertexM import VertexM
from src.models.EdgeM import EdgeM
from typing import List



@dataclass
class GraphM:
    vertex:List[VertexM]=field(default_factory=list)
    edges: List[EdgeM] = field(default_factory=list)
    
    
