from networkx import DiGraph
from networkx.algorithms.dag import descendants


class RandomDag:
    """This class represents a simple DAG with properties
    that might be random variable e.g. a 'runtime' property for each node
    with value from the uniform distribution, U(30, 50).

    Each node may be associated with key-value pairs of properties. The key
    specifies the name of the property whereas the value is a list. The first
    element in the list is the name of a SciPy random distribution function
    (https://docs.scipy.org/doc/numpy-1.14.0/reference/routines.random.html),
    and the rest are the arguments to that function.

    TODO: support layers, and random edges between layers
    """
    def __init__(self):
        self.dag = DiGraph()

    def add_node(self, node):
        """Adds a node to this DAG

        Args:
            node (Node): a node to add to this DAG
        """
        self.dag.add_node(node.name, **node.properties)

    def add_edge(self, from_node,
                 to_node,
                 properties={},
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
                from_node.name in descendants(self.dag, to_node.name):
            raise Exception("This edge adds a cycle to the graph")

        if properties is None or properties is {}:
            self.dag.add_edge(from_node.name, to_node.name)
        else:
            self.dag.add_edge(from_node.name, to_node.name, **properties)

    @staticmethod
    def __update_property(data, property_name, default_weight):
        """ Updates a node or edge property with given name.

        Args:
            data (dict): map of node/edge properties
            property_name: name of a property (i.e. a key for 'data')
            default_weight (float): default value of the property
        """
        if property_name in data:
            property_val = data[property_name]
            if property_val is not None and len(property_val) > 1:
                func_args = property_val[1:]
                return property_val[0](*func_args)
        return default_weight

    def sample_node_property(self, node_property,
                             weight_key='w',
                             default_weight=0):
        """ Samples nodes with given property, and sets weight_key with the
        sampled, or default, value.

        Args:
            node_property (str): name of node property to sample
            weight_key (str): name of property that holds sampled value
            default_weight (float): default value of the weight_key property
        """
        if node_property is None or node_property is "":
            raise Exception("Invalid property")

        for (node, data) in list(self.dag.nodes(data=True)):
            property_weight = RandomDag.__update_property(
                data, node_property, default_weight)
            self.dag.nodes[node][weight_key] = property_weight

    def sample_edge_property(self, edge_property,
                             weight_key='w',
                             default_weight=0):
        """ Samples edges with given property, and sets weight_key with the
        sampled, or default, value.

        Args:
            edge_property (str): name of edge property to sample
            weight_key (str): name of property that holds sampled value
            default_weight (float): default value of the weight_key property
        """
        if edge_property is None or edge_property is "":
            raise Exception("Invalid property")

        for (s, t, data) in list(self.dag.edges(data=True, default={})):
            property_weight = RandomDag.__update_property(
                data, edge_property, default_weight)
            self.dag[s][t][weight_key] = property_weight

    def node_property_to_edge(self, start_node_name="start",
                              node_property='w',
                              edge_property='w'):
        """ Translates a node property to an edge property by modifying the
        underlying DAG to (1) add a "start" node, and to (2) add an
        edge weight, which is the weight of its successor node.

        Args:
            start_node_name (str): name of the node to add that will be
               topologically precedent to all others
            node_property (str): name of node property to get
            edge_property (str): name of edge property to set
        """
        if len(self.dag) == 0:
            return
        # add an edge to existing start nodes
        start = Node(start_node_name)
        zero_indegree = [v for v, d in self.dag.in_degree() if d == 0]
        for node in zero_indegree:
            self.dag.add_edge(start.name, node)
        for (s, t) in list(self.dag.edges(data=False)):
            self.dag[s][t][edge_property] = self.dag.nodes[t][node_property]

    def second_longest_path(self, weight='w', default_weight=0):
        """

        Args:
            weight (str): edge data key to use for weight
            default_weight (int): weight of edges that do
               not have a weight attribute
        """
        # TODO
        print(["not implemented", weight, default_weight])


class Node:
    """Represent a node (vertex) in a DAG.

    Associated with a map of properties, and a set of labels.
    """

    NODE_LABEL_KEY = "__node_labels"

    def __init__(self, name, properties={}, labels=None):
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
        if labels is not None:
            self.properties[self.__class__.NODE_LABEL_KEY] = labels

    def __str__(self):
        ' '.join("name", self.name, "properties", str(self.properties))
