from dataclasses import dataclass,field
from typing import List
from src.models.Soldier import Soldier

@dataclass
class Tower:
    surveillance_radius: float = 0.0  
    height: float = 0.0               
    is_built: bool = False
    reserved_soldiers: List[Soldier] = field(default_factory=list)
