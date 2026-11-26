from dataclasses import dataclass,field
from src.models.VertexM import VertexM
from typing import List



@dataclass
class GraphM:
    vertex:List[VertexM]=field(default_factory=list)
    
    
