from neo4j.v1 import GraphDatabase


class Neo4jConnector:
    def __init__(self, url, auth):
        self._driver = GraphDatabase.driver(url, auth=auth)

    @staticmethod
    def add_node(tx, label="Node", data={}):
        """Adds a node to the database.
        https://neo4j.com/docs/developer-manual/current/cypher/clauses/merge/

        Args:
            tx (transaction): a transaction object
            label (str): node label
            data (dict): node properties (must have string keys)
        """
        if label is None or not label or data is None:
            raise Exception("Arguments must be non-null; label, non-empty")

        create_query = "MERGE (a:{})".format(label)
        subqueries = [create_query]
        for k in data.iterkeys():
            subqueries.append("SET a.{} = ${}".format(k, k))
        query = " ".join(subqueries)
        tx.run(query, **data)

    def close(self):
        self._driver.close()
