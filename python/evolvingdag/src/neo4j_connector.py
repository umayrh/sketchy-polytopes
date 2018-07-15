from neo4j.v1 import GraphDatabase


class Neo4jConnector:
    def __init__(self, url, auth):
        self._driver = GraphDatabase.driver(url, auth=auth)

    @staticmethod
    def __make_property_list(data):
        properties = []
        for k in data.iterkeys():
            properties.append("{}: ${}".format(k, k))
        return properties

    @staticmethod
    def __check_args(label, data):
        if label is None or not label or data is None:
            raise Exception("Arguments must be non-null; label, non-empty")

    @staticmethod
    def add_node(tx, label="Node", data={}):
        """Adds a node to the database.
        https://neo4j.com/docs/developer-manual/current/cypher/clauses/merge/

        TODO: support multiple labels

        Args:
            tx (transaction): a transaction object
            label (str): node label
            data (dict): node properties (must have string keys)
        """
        Neo4jConnector.__check_args(label, data)
        properties = Neo4jConnector.__make_property_list(data)
        query = "MERGE (a:{} {{ {} }})".format(label, ",".join(properties))
        tx.run(query, **data)

    @staticmethod
    def add_edge(tx, from_node, to_node, edge_type="SUCCEEDS", data={}):
        """Adds an edge to the database.
        https://neo4j.com/docs/developer-manual/current/cypher/clauses/create

        Args:
            tx (transaction): a transaction object
            from_node (str): source node label
            to_node (str): target node label
            edge_type (str): relationship type
            data (dict): edge properties (must have string keys)
        """
        Neo4jConnector.__check_args(edge_type, data)
        # TODO allow adding edges by the node property (e.g. 'name')
        properties = Neo4jConnector.__make_property_list(data)
        query = "MATCH (a:{}), (b:{}) " \
                "CREATE (a)-[r:{} {{ {} }}]->(b)" \
            .format(from_node, to_node, edge_type, ",".join(properties))
        tx.run(query, **data)

    def close(self):
        self._driver.close()
