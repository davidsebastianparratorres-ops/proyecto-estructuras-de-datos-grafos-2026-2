from dataclasses import dataclass

@dataclass
class Parameters:
    max_towers_k:int # section 4
    d0_time_reference:float # section 4
    beta_height: float # section 5
    alpha_danger:float # section 6
    bridge_rebuild_time:float # section 3 and 8