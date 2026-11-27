from src.controllers.GraphEController import GraphEController
from src.controllers.ScenarioLoader import ScenarioLoader

class ScenarioController:
    
    def __init__(self):
        self.scenario = None
        self.graph_e_controller:GraphEController| None = None 
        self.mst_edges = []
        
    def initialize_scenario(self, json_path: str) -> None:
        # 1. Solo parsea e instancia los modelos
        self.scenario = ScenarioLoader.load_from_file(json_path)

        # 2. Inicializa los controladores de cada grafo
        self.graph_e_controller = GraphEController(
            graph_e=self.scenario.graph_e,
            graph_m=self.scenario.graph_m
        )

        # 3. Ejecuta la preparación inicial del mapa
        self.mst_edges = self.graph_e_controller.build_mst_prim()