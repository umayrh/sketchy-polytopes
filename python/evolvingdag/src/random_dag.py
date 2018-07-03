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

    def __str__(self):
        """String representation of this object"""
        return "dag_model" + str(self.dag_model)


class RandomDagModel:
    """Utilities for creating random directed acyclic graphs.

    This class represents a simple DAG with properties
    that might be random models e.g. a 'runtime' property for each node
    with value from the uniform distribution, U(30, 50).
    """
    def __init__(self):
        # TODO: support layers, and random edges between layers
        self.base_dag = nx.DiGraph()

    def add_node(self, node):
        self.base_dag.add_node(node.name, **node.properties)

    def add_edge(self, from_node,
                 to_node,
                 properties=None,
                 check_acyclicity=True):
        """Adds a directed edge to this DAG

        Args:
            from_node (Node): source node
            to_node (Node): target node
            properties (dict): a map of string keys to any values
            check_acyclicity (bool): check and throw if this edge adds a
               cycle to the DAG (default: True)
        """
        if check_acyclicity and \
                from_node.name in nx.descendents(self.base_dag, to_node.name):
            raise Exception("This edge adds a cycle to the graph")
        if properties is None:
            self.base_dag.add_edge(from_node, to_node)
        else:
            self.base_dag.add_edge(from_node, to_node, **properties)

    def __str__(self):
        """String representation of this model as a map of adjacency lists"""
        str(nx.to_dict_of_lists(self.base_dag))


class Node:
    """Represent a node (vertex) in a DAG.

    Associated with a map of properties, and a set of labels.
    """

    NODE_LABEL_KEY = "__node_labels"

    def __init__(self, name, properties, labels=None):
        """
        Creates a node object.

        Args:
            name (str): an identifier for this node, assumed to be
               unique across all nodes in the graph that this node belongs to
            properties (dict): a map of string keys to any values
            labels (set): a set of string labels
        """
        self.name = name
        self.properties = properties
        self.properties[self.__class__.NODE_LABEL_KEY] = labels

    def __str__(self):
        ' '.join("name", self.name, "properties", str(self.properties))
