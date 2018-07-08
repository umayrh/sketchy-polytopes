import unittest
import pytest
from random_dag import Node, RandomDagModel, RandomDag
from numpy.random import uniform


class Test(unittest.TestCase):
    def test_node(self):
        """Tests if a node with name and properties can be created correctly"""
        a = Node("a")
        self.assertEqual("a", a.name)
        self.assertEqual({}, a.properties)

        b = Node("b", {"type": 1})
        self.assertEqual("b", b.name)
        self.assertEqual({"type": 1}, b.properties)

        c = Node("c", {"time": 1, "class": "xyz"}, set("ctx"))
        self.assertEqual("c", c.name)
        c_expected = {"time": 1, "class": "xyz", c.NODE_LABEL_KEY: set("ctx")}
        self.assertEqual(c_expected, c.properties)

    def test_random_dag_model(self):
        """Tests if a RandomDagModel can be created correctly"""
        a = Node("a")
        b = Node("b")
        dag = RandomDagModel()
        dag.add_node(a)
        dag.add_node(b)
        dag.add_edge(a, b, {"w": 2})

        self.assertTrue(a.name in dag.dag)
        self.assertTrue(b.name in dag.dag)
        self.assertFalse("c" in dag.dag)
        self.assertFalse(dag.dag.succ[b.name])
        self.assertFalse(dag.dag.pred[a.name])

        self.assertTrue(dag.dag.has_edge("a", "b"))
        self.assertTrue(2, dag.dag["a"]["b"]["w"])
        self.assertFalse("d" in dag.dag["a"]["b"])

        pytest.raises(Exception, dag.add_edge, b, a)
        dag.add_edge(b, a, {"w": 2}, False)
        self.assertTrue(dag.dag.has_edge("b", "a"))

    def test_random_dag(self):
        """Tests if a RandomDag can be created correctly"""
        a = Node("a", {"x": [uniform, 10, 20]})
        b = Node("b", {"y": [uniform, 20, 30]})
        c = Node("c", {"z": [uniform, 30, 40]})
        model = RandomDagModel()
        model.add_node(a)
        model.add_node(b)
        model.add_node(c)
        model.add_edge(a, b, {"w": 2})
        model.add_edge(b, c, {"r": [uniform, 30, 40]})
        dag = RandomDag(model)

        dag.sample_edge_property("q")
        self.assertTrue(dag.model.dag.has_edge("a", "b"))
        self.assertTrue(dag.model.dag.has_edge("b", "c"))
        self.assertEqual(0, dag.model.dag["a"]["b"]["w"])
        self.assertEqual(0, dag.model.dag["b"]["c"]["w"])

        dag.sample_edge_property("r")
        self.assertTrue(dag.model.dag.has_edge("a", "b"))
        self.assertTrue(dag.model.dag.has_edge("b", "c"))
        self.assertEqual(0, dag.model.dag["a"]["b"]["w"])
        self.assertTrue(30 <= dag.model.dag["b"]["c"]["w"] < 40)

        dag.sample_node_property("x")
        self.assertTrue(10 <= dag.model.dag.nodes["a"]["w"] < 20)
        self.assertTrue(dag.model.dag.nodes["b"]["w"] == 0)
        self.assertTrue(dag.model.dag.nodes["c"]["w"] == 0)

        dag.sample_node_property("y")
        self.assertTrue(dag.model.dag.nodes["a"]["w"] == 0)
        self.assertTrue(20 <= dag.model.dag.nodes["b"]["w"] < 30)
        self.assertTrue(dag.model.dag.nodes["c"]["w"] == 0)

        dag.sample_node_property("z")
        self.assertTrue(dag.model.dag.nodes["a"]["w"] == 0)
        self.assertTrue(dag.model.dag.nodes["b"]["w"] == 0)
        self.assertTrue(30 <= dag.model.dag.nodes["c"]["w"] < 40)

if __name__ == "__main__":
    unittest.main()
