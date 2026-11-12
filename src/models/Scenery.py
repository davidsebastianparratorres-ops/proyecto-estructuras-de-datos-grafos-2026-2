from dataclasses import dataclass
from src.models.GraphE import GraphE
from src.models.GraphM import GraphM
from src.models.Parameters import Parameters



@dataclass
class Scenery:
    graph_e:GraphE
    graph_m:GraphM    
    parameters:Parameters
    
