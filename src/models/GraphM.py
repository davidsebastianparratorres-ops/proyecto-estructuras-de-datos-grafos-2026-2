from dataclasses import dataclass,field
from src.models.VertexM import VertexM
from typing import List



@dataclass
class GraphM:
    vertex:List[VertexM]=field(default_factory=list)
    
    def get_vertex_by_id(self, id: str) -> VertexM:
            for v in self.vertex:
                if v.id == id:
                    return v
            raise ValueError(f"No vertex found in GraphM with id '{id}'.")
        
    def get_entry(self) -> VertexM:
        
        for v in self.vertex:
            if v.is_entry:
                return v
        raise ValueError("No entry vertex found in GraphM.")
        
    def get_exit(self) ->VertexM:
        
        for v in self.vertex:
            if v.is_exit:
                return v
        raise ValueError("No exit vertex found in GraphM.")

            
            
