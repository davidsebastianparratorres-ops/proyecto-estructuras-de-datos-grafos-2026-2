from dataclasses import dataclass, field
from typing import List
from src.models.VertexE import VertexE
from src.models.Base import Base


@dataclass
class GraphE:
    vertex: List[VertexE] = field(default_factory=list)

    def get_base(self) -> Base:
        for v in self.vertex:
            if isinstance(v, Base):
                return v
        raise ValueError("No Base vertex found in GraphE.")

    def get_vertex_by_id(self, id: str) -> VertexE:
        for v in self.vertex:
            if v.id == id:
                return v
        raise ValueError(f"No vertex found in GraphE with id '{id}'.")