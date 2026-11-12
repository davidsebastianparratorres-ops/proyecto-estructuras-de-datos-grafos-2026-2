from dataclasses import dataclass
from src.models.Vertex import Vertex

@dataclass
class VertexE(Vertex):
    position_type:str
    soldiers=[]
    bridges=[]
    roads=[]
    
