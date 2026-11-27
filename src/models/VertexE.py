from dataclasses import dataclass,field
from src.models.Vertex import Vertex
from typing import List,Tuple
from src.models.Vertex import Vertex
from src.models.Soldier import Soldier
from src.models.Road import Road



@dataclass
class VertexE(Vertex):
    soldiers: List[Soldier] = field(default_factory=list)
    edges: List[Road] = field(default_factory=list)
    
    
    def lower_cost_destiny(self,visited)->Tuple[str,str,float]:
        
        cost=float('inf')
        destiny=None
        for e in self.edges:
            if e.destiny not in visited:
                if (e.get_walk_time()<cost 
                    or (e.get_walk_time()==cost and destiny is not None and e.destiny<destiny)):#desempate lexicografico
                    cost=e.get_walk_time()
                    destiny=e.destiny
        
        if destiny is None:
            return None
                
        return (self.id,destiny,cost)