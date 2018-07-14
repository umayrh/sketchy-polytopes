import unittest
from neo4j.v1 import basic_auth
from neo4j_connector import Neo4jConnector


class Test(unittest.TestCase):
    """Tests Neo4jConnector

    TODO: basic auth is consistent with Travis' setup; use
    https://docs.travis-ci.com/user/environment-variables/#Defining-encrypted-variables-in-.travis.yml

    TODO: use IntegrationTestCase for better isolation
    https://github.com/neo4j/neo4j-python-driver/blob/1.6/test/integration/tools.py
    """

    @classmethod
    def setUpClass(cls):
        """Initializes the Neo4j driver"""
        cls.conn = Neo4jConnector(
            "bolt://localhost",
            basic_auth("neo4j", "neo4j"))

    @classmethod
    def tearDownClass(cls):
        """Shuts down the Neo4j driver"""
        cls.conn._driver.close()

    def tearDown(self):
        """Deletes all nodes in the current graph"""
        with Test.conn._driver.session() as session:
            session.run("MATCH (n) WITH n LIMIT 1000 DETACH DELETE n")

    def test_add_node(self):
        """Tests if Neo4j nodes can be created"""
        properties = {"name": "a", "time": 4}
        with Test.conn._driver.session() as session:
            tx = session.begin_transaction()
            Neo4jConnector.add_node(tx, "Node", properties)
            tx.commit()
        with Test.conn._driver.session() as session:
            result = session.run("MATCH (a:Node) WHERE a.time = $val "
                                 "RETURN a.name",
                                 val=properties["time"])
            record = next(iter(result))
            self.assertEqual(properties["name"], record[0])
