from dataclasses import dataclass
from src.models.Vertex import Vertex


@dataclass
class VertexM(Vertex):
    machines=[]
    edgeM=[]
