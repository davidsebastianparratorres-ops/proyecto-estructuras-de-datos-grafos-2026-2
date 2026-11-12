from dataclasses import dataclass
from src.models.Vehicle import Vehicle


@dataclass
class Helicopter(Vehicle):
    speed: float
    uses: int 
