import unittest
from src.models.Base import Base
from src.models.Tower import Tower
from src.models.Road import Road
from src.models.GraphE import GraphE
from src.models.GraphM import GraphM
from src.controllers.GraphEController import GraphEController


class TestGraphEController(unittest.TestCase):

    def _connect(self, v1, v2, road_id: str, walk_time: float, moto_time: float):
        """Helper to simulate ScenarioLoader adding undirected roads as two directed edges."""
        v1.edges.append(Road(id=road_id, destiny=v2.id, walk_time=walk_time, moto_time=moto_time))
        v2.edges.append(Road(id=road_id, destiny=v1.id, walk_time=walk_time, moto_time=moto_time))

    def test_mst_connected_graph_with_cycles(self):
        """Verifies Prim builds the minimum cost tree and avoids cycles."""
        base = Base(id="B", x_coord=0.0, y_coord=0.0)
        t1 = Tower(id="T1", x_coord=10.0, y_coord=0.0)
        t2 = Tower(id="T2", x_coord=0.0, y_coord=10.0)
        t3 = Tower(id="T3", x_coord=10.0, y_coord=10.0)

        # Edges: B-T1 (4), B-T2 (2), T2-T1 (1), T1-T3 (5), T2-T3 (8)
        # Expected MST: (B, T2, 2), (T2, T1, 1), (T1, T3, 5) -> Total cost = 8
        self._connect(base, t1, "R1", walk_time=4.0, moto_time=2.0)
        self._connect(base, t2, "R2", walk_time=2.0, moto_time=1.0)
        self._connect(t2, t1, "R3", walk_time=1.0, moto_time=0.5)
        self._connect(t1, t3, "R4", walk_time=5.0, moto_time=2.5)
        self._connect(t2, t3, "R5", walk_time=8.0, moto_time=4.0)

        graph_e = GraphE(vertex=[base, t1, t2, t3])
        graph_m = GraphM(vertex=[])
        controller = GraphEController(graph_e, graph_m)

        mst = controller.build_mst_prim()
        total_cost = sum(edge[2] for edge in mst)

        self.assertEqual(len(mst), 3)
        self.assertEqual(total_cost, 8.0)
        self.assertEqual(mst, [("B", "T2", 2.0), ("T2", "T1", 1.0), ("T1", "T3", 5.0)])

    def test_mst_ignores_disconnected_components(self):
        """Verifies Prim only includes the connected component containing the Base."""
        base = Base(id="B", x_coord=0.0, y_coord=0.0)
        t1 = Tower(id="T1", x_coord=5.0, y_coord=0.0)
        isolated_t2 = Tower(id="T2", x_coord=50.0, y_coord=50.0)
        isolated_t3 = Tower(id="T3", x_coord=60.0, y_coord=50.0)

        self._connect(base, t1, "R1", walk_time=3.0, moto_time=1.5)
        self._connect(isolated_t2, isolated_t3, "R2", walk_time=1.0, moto_time=0.5)

        graph_e = GraphE(vertex=[base, t1, isolated_t2, isolated_t3])
        controller = GraphEController(graph_e, GraphM(vertex=[]))

        mst = controller.build_mst_prim()

        self.assertEqual(mst, [("B", "T1", 3.0)])

    def test_mst_tie_breaking_deterministic(self):
        """Verifies lexicographical tie-breaking when two edges have equal walk_time."""
        base = Base(id="B", x_coord=0.0, y_coord=0.0)
        t1 = Tower(id="T1", x_coord=5.0, y_coord=0.0)
        t2 = Tower(id="T2", x_coord=0.0, y_coord=5.0)

        self._connect(base, t2, "R2", walk_time=4.0, moto_time=2.0)
        self._connect(base, t1, "R1", walk_time=4.0, moto_time=2.0)

        graph_e = GraphE(vertex=[base, t2, t1])
        controller = GraphEController(graph_e, GraphM(vertex=[]))

        mst = controller.build_mst_prim()

        self.assertEqual(mst, [("B", "T1", 4.0), ("B", "T2", 4.0)])

    def test_mst_isolated_base(self):
        """Verifies an isolated Base returns an empty list without crashing."""
        base = Base(id="B", x_coord=0.0, y_coord=0.0)
        t1 = Tower(id="T1", x_coord=10.0, y_coord=10.0)

        graph_e = GraphE(vertex=[base, t1])
        controller = GraphEController(graph_e, GraphM(vertex=[]))

        mst = controller.build_mst_prim()

        self.assertEqual(mst, [])


if __name__ == "__main__":
    unittest.main()