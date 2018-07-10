import unittest
from neo4j.v1 import basic_auth
from neo4j_connector import Neo4jConnector


class Test(unittest.TestCase):
    """Tests Neo4jConnector

    TODO: basic auth is consistent with Travis' setup; use
    https://docs.travis-ci.com/user/environment-variables/#Defining-encrypted-variables-in-.travis.yml
    """

    @classmethod
    def setUpClass(cls):
        cls.conn = Neo4jConnector(
            "bolt://localhost",
            basic_auth("neo4j", "neo4j"))

    @classmethod
    def tearDownClass(cls):
        cls.conn._driver.close()

    def test_add_node(self):
        """Tests if Neo4j nodes can be created"""
        properties = {"name": "a", "time": 4}
        with Test.conn._driver.session() as session:
            tx = session.begin_transaction()
            Neo4jConnector.add_node(tx, set("Node"), properties)
            tx.commit()
            tx = session.begin_transaction()
            result = tx.run("MATCH (a:Node) WHERE a.time = $val "
                            "RETURN a.name",
                            val=properties["time"]).single().value()
            self.assertEqual(properties["name"], result)
