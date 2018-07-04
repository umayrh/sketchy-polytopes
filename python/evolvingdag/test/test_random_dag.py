import unittest
from random_dag import Node, RandomDagModel


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
        dag = RandomDagModel()
        a = Node("a")
        b = Node("b")
        dag.add_node(a)
        dag.add_node(b)
        dag.add_edge(a, b)

        self.assertTrue(a.name in dag.base_dag)
        self.assertTrue(b.name in dag.base_dag)
        self.assertFalse("c" in dag.base_dag)
        self.assertTrue(dag.base_dag.has_edge("a", "b"))

if __name__ == "__main__":
    unittest.main()
