from src.models.GraphM import GraphM

class GraphMController:
    
    def __init__(self, graph_m=GraphM):
        
        self.graph_m = graph_m
        
    def dfs_has_path(self,start_id: str, end_id: str)->bool:
        
        start=self.graph_m.get_vertex_by_id(start_id)
        end=self.graph_m.get_vertex_by_id(end_id)
        visited=[start.id]
        stack=[start]
        
        while(stack):
            
            currenly=stack.pop() #objeto vertice M
            for neighbor in currenly.edges: #neighbor objeto arista con destiny:str
                if neighbor.destiny not in visited:
                    visited.append(neighbor.destiny) 
                    if neighbor.destiny==end.id:
                        return True
                
        return False
        
            
