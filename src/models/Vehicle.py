from dataclasses import dataclass


@dataclass
class Vehicle:
    id:str
    capacity:int
    availability:bool
