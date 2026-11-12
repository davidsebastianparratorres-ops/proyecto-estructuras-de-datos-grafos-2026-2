from dataclasses import dataclass
from src.models.Road import Road


@dataclass
class Bridge(Road):
    
    max_resistence:int
    currenly_resistence:int
    aviable:bool
    
    
