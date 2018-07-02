import networkx as nx


class RandomDag:
    """Represents an instance of a RandomGraphModel.

    The model uses a random sample from each property with a random model.
    """
    def __init__(self, dag_model):
        self.dag_model = dag_model

    def make(self):
        """ Instantiates a DAG model.
        """
        print("unimplemented")

    def to_string(self):
        """String representation of this object"""
        return "dag_model" + self.dag_model.to_string()


class RandomDagModel:
    """Utilities for creating random directed acyclic graphs.

    This class represents a structurally well-defined DAG with properties
    that might be random models e.g. a 'runtime' property for each node
    with value from the uniform distribution, U(30, 50).
    """
    def __init__(self):
        # TODO: figure out the object and the interface for
        # this graph model. List of nodes, and associated meta-properties
        # (including random model), properties, and labels.
        self.base_dag = nx.DiGraph()

    def add_node(self, node):
        self.base_dag.add_node(node)

    def add_edge(self, fromNode, toNode):
        self.base_dag.add_edge(fromNode, toNode)


class Node:
    """Represent a node (vertex) in a DAG.

    Associated with a map of properties, and a set of labels.
    """
    def __init__(self, name, properties, labels):
        """
        Creates a node object.

        :param name: a string identifier for this node
        :param properties: a map (dictionary) of string keys to any values
        :param labels: a set of string labels
        """
        self.name = name
        self.properties = properties
        self.labels = labels


class Edge:
    """Represent an edge in a DAG.

    Associated with a map of properties.
    """
    def __init__(self, name, properties):
        """
        Creates a node object.

        :param name: a string identifier for this edge
        :param properties: a map (dictionary) of string keys to any values
        """
        self.name = name
        self.properties = properties
