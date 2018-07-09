import unittest
from neo4j.v1 import basic_auth
from neo4j_connector import Neo4jConnector


class Test(unittest.TestCase):
    @staticmethod
    def make_model():
        print("")

    def test_add_node(self):
        """Tests if Neo4j nodes can be created"""
        properties = {"name": "a", "time": 4}
        # TODO: basic auth is consistent with Travis' setup; use
        # https://docs.travis-ci.com/user/environment-variables/#Defining-encrypted-variables-in-.travis.yml
        conn = Neo4jConnector("bolt://localhost", basic_auth("neo4j", "neo4j"))
        with conn.driver.session() as session:
            tx = session.begin_transaction()
            Neo4jConnector.add_node(tx, "Node", properties)
            tx.commit()
            tx = session.begin_transaction()
            result = tx.run("MATCH (a:Node) WHERE a.time = $val "
                            "RETURN a.name",
                            val=properties["time"]).single().value()
            self.assertEqual(properties["name"], result)
