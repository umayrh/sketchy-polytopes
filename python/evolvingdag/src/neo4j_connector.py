from neo4j.v1 import GraphDatabase


class Neo4jConnector:
    def __init__(self, url, auth):
        self.driver = GraphDatabase.driver(url, auth=auth)

    @staticmethod
    def add_node(tx, labels=set("Node"), data={}):
        """Adds a node to the database.
        https://neo4j.com/docs/developer-manual/current/cypher/clauses/merge/

        Args:
            tx (transaction): a transaction object
            labels (set): node label
            name (str): node name
            data (dict): node properties (must have string keys)
        """
        if labels is None or len(labels) is 0 or data is None:
            raise Exception("Arguments must be non-null")

        create_query = "MERGE (a:{})".format(":".join(labels))
        subqueries = [create_query]
        for k in data.iterkeys():
            subqueries.append("SET a.{} = ${}".format(k, k))
        query = " ".join(subqueries)
        tx.run(query, **data)
