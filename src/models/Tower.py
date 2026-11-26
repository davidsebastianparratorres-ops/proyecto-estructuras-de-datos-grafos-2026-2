from dataclasses import dataclass,field
from typing import List
from src.models.Soldier import Soldier
from src.models.VertexE import VertexE

@dataclass
class Tower(VertexE):
    surveillance_radius: float = 0.0  
    height: float = 0.0               
    is_built: bool = False
    reserved_soldiers: List[Soldier] = field(default_factory=list)
