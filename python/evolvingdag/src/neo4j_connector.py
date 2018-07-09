from neo4j.v1 import GraphDatabase


class Neo4jConnector:
    def __init__(self, url, auth):
        self.driver = GraphDatabase.driver(url, auth=auth)

    @staticmethod
    def add_node(tx, label="Node", data={}):
        """

        Args:
            tx (transaction): a transaction object
            label: node label
            name: node name
            data: node properties (must have string keys)
        """
        if label is None or data is None:
            raise Exception("Arguments must be non-null")

        create_query = "MERGE (a:{})".format(label)
        subqueries = [create_query]
        for k in data.iterkeys():
            subqueries.append("SET a.{} = ${}".format(k, k))
        query = " ".join(subqueries)
        tx.run(query, **data)
