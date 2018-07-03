import unittest
import random_dag as rd


class Test(unittest.TestCase):
    def test_node_creation(self):
        """Tests if a node can be created correctly"""
        a = rd.Node("name", {}, None)
        self.assertEqual("name", a.name)
        self.assertEqual({a.NODE_LABEL_KEY: None}, a.properties)

if __name__ == "__main__":
    unittest.main()
