import json
from pathlib import Path
from typing import Dict, Any

from src.models.Scenery import Scenery
from src.models.Parameters import Parameters
from src.models.GraphE import GraphE
from src.models.GraphM import GraphM
from src.models.VertexE import VertexE
from src.models.Base import Base
from src.models.Tower import Tower
from src.models.Heliport import Heliport
from src.models.VertexM import VertexM
from src.models.Road import Road
from src.models.Bridge import Bridge
from src.models.EdgeM import EdgeM
from src.models.Machine import Machine
from src.models.TypeMachine import TypeMachine

class ScenarioLoader:
    
    @staticmethod
    def load_from_file(file_path:str)->Scenery:
        path=Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Scenario file not found: {file_path}")
        
        with open(path, "r", encoding="utf-8") as file:
            data: Dict[str,Any] = json.load(file)# pasar scenario.json a estructura diccionario
            
        required_keys = {"parameters", "graph_e", "graph_m", "convoy"}
        
        #para verificar keys del diccionario faltantes
        if not required_keys.issubset(data.keys()):
            missing = required_keys = set(data.keys())
            raise ValueError(f"Missing required JSON sections: {missing}")
        
        parameters = ScenarioLoader._parse_parameters(data["parameters"])
        graph_e = ScenarioLoader._parse_graph_e(data["graph_e"])
        graph_m = ScenarioLoader._parse_graph_m(data["graph_m"])
        convoy = ScenarioLoader._parse_convoy(data["convoy"])
        
        entry_vertex = graph_m.get_entry_vertex()
        entry_vertex.machines.extend(convoy)
        
        return Scenery(graph_e=graph_e, graph_m=graph_m, parameters=parameters)

    @staticmethod
    
    def _parse_parameters(raw: Dict[str,Any])->Parameters:
        
        if raw["inicial_budget"]<0 or raw["max_towers_k"]<=0 or raw["d0_time_reference"] <=0 or raw["alpha_danger"]<=0 or raw["beta_height"<=0]:
            raise ValueError("Invalid numeric parameters: budget, K', and D0 must be positive.")
        
        return Parameters(
            max_towers_k=int(raw["max_towers_k"]),
            d0_time_reference=float(raw["d0_time_reference"]),
            beta_height=float(raw["beta_height"]),
            alpha_danger=float(raw["alpha_danger"]),
            bridge_rebuild_time=float(raw["bridge_rebuild_time"])            
        )
    
    @staticmethod
    
    def _parse_graph_e(raw: Dict[str,Any])->GraphE:
        vertices: Dict[str,VertexE]={}
        base_count=0 #contador para asegurar que solo haya una base
        
        #parsear vertices
        for vertice in raw["vertices"]:
            vertice_id=str(vertice["id"])
            if vertice_id in vertices:
                raise ValueError(f"Duplicate vertex ID in G_E: {vertice_id}")
            
            x, y=float(vertice["x"]) , float(vertice["y"])
            
            if x < 0 or y < 0:
                raise ValueError(f"Coordinates in G_E must be positive: {vertice_id}")
            
            vertice_type = vertice["type"]
            if vertice_type == "base":
                base_count+=1
                vertices[vertice_id]=Base(id=vertice_id, x_coord=x, y_coord=y)
            
            elif vertice_type == "tower_candidate":
                vertices[vertice_id]=Tower(
                    id=vertice_id,
                    x_coord=x,
                    y_coord=y,
                    surveillance_radius=float(vertice["surveillance_radius"]),
                    height=float(vertice["height"])
                    )
            elif vertice_type == "heliport":
                vertices[vertice_id] = Heliport(id=vertice_id, x_coord=x, y_coord=y)
            elif vertice_type == "transit":
                vertices[vertice_id] = VertexE(id=vertice_id, x_coord=x, y_coord=y)
            else:
                raise ValueError(f"Unknown VertexE type '{vertice_type}' for vertex {vertice_id}")
            
            if base_count != 1:
                raise ValueError(f"G_E must contain exactly one base, found {base_count}.")
            
        #parsear aristas
        
        for e in raw["edges"]:
            orig, dest = str(e["origin"]), str(e["destiny"])
            if orig not in vertices or dest not in vertices:
                raise ValueError(f"Edge {e['id']} connects non-existent vertices ({orig} -> {dest}).")
            
            e_type=e["type"]
            
            if e_type == "road":
                edge_obj= Road(
                    id=str(e["id"]),
                    origin=orig,
                    destiny=dest,
                    walk_time=float(e["walk_time"]),
                    moto_time=float(e["moto_time"])
                )
            elif e_type == "bridge":
                max_res =int(e["max_resistence"])    
                if max_res<=0:
                    raise ValueError(f"Bridge {e['id']} must have positive resistence.")
                edge_obj = Bridge(
                    id=str(e["id"]),
                    origin=orig,
                    destiny=dest,
                    walk_time=float(e["walk_time"]),
                    moto_time=float(e["moto_time"]),
                    max_resistence=max_res,
                    currenly_resistence=max_res,
                    aviable=True
                )
            else:
                raise ValueError(f"Unknown Edge type '{e_type}' in G_E.")
            
            
            vertices[orig].edges.append(edge_obj)
            vertices[dest].edges.append(edge_obj)
            
        return GraphE(vertexE=vertices)
        
    @staticmethod
    def _parse_graph_m(raw: Dict[str, Any]) -> GraphM:
        vertices: Dict[str, VertexM] = {}
        entries = 0
        exits = 0

        for v in raw["vertices"]:
            v_id = str(v["id"])
            if v_id in vertices:
                raise ValueError(f"Duplicate vertex ID in G_M: {v_id}")

            is_entry = bool(v.get("is_entry", False))
            is_exit = bool(v.get("is_exit", False))
            if is_entry and is_exit:
                raise ValueError(f"Vertex {v_id} cannot be both entry and exit.")
            if is_entry:
                entries += 1
            if is_exit:
                exits += 1

            vertices[v_id] = VertexM(
                id=v_id,
                x_coord=float(v["x"]),
                y_coord=float(v["y"]),
                is_entry=is_entry,
                is_exit=is_exit
            )

        if entries != 1 or exits != 1:
            raise ValueError("G_M must have exactly one entry and one exit vertex.")

        for e in raw["edges"]:
            orig, dest = str(e["origin"]), str(e["destiny"])
            if orig not in vertices or dest not in vertices:
                raise ValueError(f"Corridor {e['id']} connects non-existent vertices.")

            length, speed = float(e["length"]), float(e["speed"])
            if length <= 0 or speed <= 0:
                raise ValueError(f"Corridor {e['id']} must have positive length and speed.")

            corridor = EdgeM(
                id=str(e["id"]),
                origin=orig,
                destiny=dest,
                long=length,
                speed=speed
            )
            # Add to both endpoints since G_M is undirected
            vertices[orig].edges.append(corridor)
            vertices[dest].edges.append(corridor)

        return GraphM(vertexM=vertices)
    
    @staticmethod
    
    def _parse_convoy(raw:Dict[str,int])->list[Machine]:
        
        machine_specs = {
            TypeMachine.TANK: (200, 150),
            TypeMachine.TRUCK: (100, 100),
            TypeMachine.ROBOT_SOLDIER: (50, 50),
        }
        
        machines: list[Machine] = []
        counter = 1
        
        for raw_type, count in raw.items():
            
            m_type = TypeMachine(raw_type)
            hp, reward = machine_specs[m_type]
            
            for i in range(int(count)):
                machines.append(
                    Machine(
                        id=f"M_UNIT_{counter:03d}",
                        type=m_type,
                        resistence=hp,
                        reward=reward
                        )
                )
                counter+=1
                
        if not machines:
            raise ValueError("Convoy must contain at least one enemy machine.")
        
        return machines