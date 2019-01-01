import unittest
import pytest
from evolvingdag.random_dag import Node, RandomDag
from numpy.random import uniform


class Test(unittest.TestCase):
    @staticmethod
    def make_model():
        a = Node("a", {"x": [uniform, 10, 20]})
        b = Node("b", {"y": [uniform, 20, 30]})
        c = Node("c", {"z": [uniform, 30, 40]})
        model = RandomDag()
        model.add_node(a)
        model.add_node(b)
        model.add_node(c)
        model.add_edge(a, b, {"w": 2})
        model.add_edge(b, c, {"r": [uniform, 30, 40]})
        return model

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

    def test_random_dag_add(self):
        """Tests if a RandomDagModel can be created correctly"""
        model = Test.make_model()

        self.assertTrue("a" in model.dag)
        self.assertTrue("b" in model.dag)
        self.assertFalse("e" in model.dag)

        self.assertTrue(model.dag.has_edge("a", "b"))
        self.assertTrue(2, model.dag["a"]["b"]["w"])
        self.assertFalse("d" in model.dag["a"]["b"])

        pytest.raises(Exception, model.add_edge, "b", "a")
        model.add_edge(Node("b"), Node("a"), {"w": 2}, False)
        self.assertTrue(model.dag.has_edge("b", "a"))

    def test_random_dag_sample(self):
        """Tests if a RandomDag can be created correctly"""
        model = Test.make_model()

        model.sample_edge_property("q")
        self.assertTrue(model.dag.has_edge("a", "b"))
        self.assertTrue(model.dag.has_edge("b", "c"))
        self.assertEqual(0, model.dag["a"]["b"]["w"])
        self.assertEqual(0, model.dag["b"]["c"]["w"])

        model.sample_edge_property("r")
        self.assertTrue(model.dag.has_edge("a", "b"))
        self.assertTrue(model.dag.has_edge("b", "c"))
        self.assertEqual(0, model.dag["a"]["b"]["w"])
        self.assertTrue(30 <= model.dag["b"]["c"]["w"] < 40)

        model.sample_node_property("x")
        self.assertTrue(10 <= model.dag.nodes["a"]["w"] < 20)
        self.assertTrue(model.dag.nodes["b"]["w"] == 0)
        self.assertTrue(model.dag.nodes["c"]["w"] == 0)

        model.sample_node_property("y")
        self.assertTrue(model.dag.nodes["a"]["w"] == 0)
        self.assertTrue(20 <= model.dag.nodes["b"]["w"] < 30)
        self.assertTrue(model.dag.nodes["c"]["w"] == 0)

        model.sample_node_property("z")
        self.assertTrue(model.dag.nodes["a"]["w"] == 0)
        self.assertTrue(model.dag.nodes["b"]["w"] == 0)
        self.assertTrue(30 <= model.dag.nodes["c"]["w"] < 40)

    def test_random_dag_property(self):
        """Tests if a RandomDag can be created correctly"""
        model = Test.make_model()
        model.sample_node_property("x")
        model.node_property_to_edge(start_node_name="s")
        self.assertTrue("s" in model.dag)
        self.assertTrue(10 <= model.dag["s"]["a"]["w"] < 20)
        self.assertTrue(model.dag["a"]["b"]["w"] == 0)
        self.assertTrue(model.dag["b"]["c"]["w"] == 0)


if __name__ == "__main__":
    unittest.main()
