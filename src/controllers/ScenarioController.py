from src.controllers.GraphEController import GraphEController
from src.controllers.GraphMController import GraphMController
from src.controllers.ScenarioLoader import ScenarioLoader

class ScenarioController:
    
    def __init__(self):
        self.scenario = None
        self.graph_e_controller:GraphEController| None = None 
        self.graph_m_controller:GraphMController| None = None
        self.mst_edges = []
        
    def initialize_scenario(self, json_path: str) -> None:
        # 1. Solo parsea e instancia los modelos
        self.scenario = ScenarioLoader.load_from_file(json_path)

        # 2. Inicializa los controladores de cada grafo
        self.graph_e_controller = GraphEController(
            graph_e=self.scenario.graph_e,
            graph_m=self.scenario.graph_m
        )
        
        self.graph_m_controller = GraphMController(
            graph_m=self.scenario.graph_m
        )

        # 3. Ejecuta la preparación inicial del mapa
        entry_id=self.scenario.graph_m.get_entry().id
        exit_id=self.scenario.graph_m.get_exit().id
        
        if not self.graph_m_controller.dfs_has_path(entry_id,exit_id):
            raise ValueError(f"Invalid scenario: no path exists between '{entry_id}' and '{exit_id}")
            
        self.mst_edges = self.graph_e_controller.build_mst_prim()
        
        