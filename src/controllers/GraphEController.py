from src.models.GraphE import GraphE
from src.models.GraphM import GraphM
from typing import List,Tuple

class GraphEController:
    
    def __init__(self, graph_e:GraphE, graph_m:GraphM):
        
        self.graph_e = graph_e
        self.graph_m = graph_m
    
    
    def build_mst_prim(self)->List[Tuple[str,str,float]]:
        """Builds the Minimum Spanning Tree (T_E) returning a list of (origin, destiny, cost)."""
        mst_edges: List[Tuple[str, str, float]] = []
        base=self.graph_e.get_base()
        visited=[base.id]
        start=base.lower_cost_destiny(visited)
        
        if start is None: return mst_edges
        
        mst_edges.append(start)
        visited.append(start[1])
        
        while(len(visited)<len(self.graph_e.vertex)):
            
            lower=None
            
            for v_id in visited:
                candidate=self.graph_e.get_vertex_by_id(v_id).lower_cost_destiny(visited)
                if candidate is not None:
                    if (
                        lower is None 
                        or candidate[2]<lower[2] 
                        or (candidate[2] == lower[2] and candidate[1] < lower[1])):#desempate lexicografico
                        
                        lower=candidate
            
            if lower is None: break #no nay mas componentes conexas desde la base
            visited.append(lower[1])
            mst_edges.append(lower)        
        
        return mst_edges
    