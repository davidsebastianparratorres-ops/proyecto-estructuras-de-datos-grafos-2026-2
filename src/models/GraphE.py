from dataclasses import dataclass,field
from typing import List
from src.models.VertexE import VertexE

@dataclass
class GraphE:
    
    vertex:List[VertexE]=field(default_factory=list)
    
