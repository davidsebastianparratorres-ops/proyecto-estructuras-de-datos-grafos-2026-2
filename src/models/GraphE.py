from dataclasses import dataclass,field
from typing import List
from src.models.VertexE import VertexE
from src.models.Road import Road


@dataclass
class GraphE:
    
    vertex:List[VertexE]=field(default_factory=list)
    edges: List[Road] = field(default_factory=list)
    
    
