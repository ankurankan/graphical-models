"""!
\file edge.py
\ingroup graphgroup edgegroup

\see \link graphgroup Graph Object \endlink edgegroup nodegroup

"""
from typing import Set, Union
from gmodels.gtypes.abstractobj import AbstractEdge, EdgeType
from gmodels.gtypes.node import Node
from gmodels.gtypes.graphobj import GraphObject


class Edge(AbstractEdge, GraphObject):
    """!
    \brief A simple edge in a graph.

    Description
    ===========
    An edge in a graph object.
    """

    def __init__(
        self,
        edge_id: str,
        start_node: Node,
        end_node: Node,
        edge_type: EdgeType = EdgeType.UNDIRECTED,
        data={},
    ):
        """!
        \brief Constructor for an edge.

        Description
        ===========

        This method initializes the attributes of a class when an object is
        created from said class. This blueprint spares space for the id of the
        attribute, in this case, the Edge, which Node it starts with, which
        Node it ends with, its type and other data it holds.
        """
        super().__init__(oid=edge_id, odata=data)
        self.etype = edge_type
        self.start_node = start_node
        self.end_node = end_node

    def __eq__(self, n):
        """!
        \brief Check for equality of a given object with this one.

        Description
        ===========

        First, we control the instance of the given argument. If the given
        argument is of the same instance, we check further. If not, we return
        False. In the case of having the same instance, we check their ids. If
        they have the same id, we return True. If not, False.

        \param n argument object of which we test for equality.
        \return True/False
        """
        if isinstance(n, Edge):
            return self.id() == n.id()
        return False

    def __str__(self):
        """!
        \brief Obtain string representation of Edge object.

        Description
        ===========

        We call the id value with data value, the Node where the Edge starts
        and the Node where the Edge ends. We transform them into strings. Then,
        we concatanate them using '--'.

        \return str
        """
        return (
            self.id()
            + "--"
            + str(self.type())
            + "--"
            + "::".join([str(k) + "-" + str(v) for k, v in self.data().items()])
            + "--"
            + str(self.start_node)
            + "--"
            + str(self.end_node)
        )

    def __hash__(self):
        """!
        \brief Obtain hash value from string representation of Edge.

        Description
        ===========

        First, we obtain the string representation of Edge. Then, we call hash
        on it.

        \return int
        """
        return hash(self.__str__())

    def start(self) -> Node:
        """!
        \brief Returns the Node from which the attribute starts.

        Description
        ===========
        Returns the Node from which the attribute starts.

        \return Node.
        """
        return self.start_node

    def is_start(self, n: Node) -> bool:
        """!
        """
        if self.type() == EdgeType.UNDIRECTED:
            return self.is_endvertice(n)
        if n.id() == self.start().id():
            return True
        return False

    def is_end(self, n: Node) -> bool:
        """!
        """

        if self.type() == EdgeType.UNDIRECTED:
            return self.is_endvertice(n)
        if n.id() == self.end().id():
            return True
        return False

    def end(self) -> Node:
        """!
        \brief Returns the Node at which the attribute ends.

        Description
        ===========
        Returns the Node at which the attribute ends.

        \return Node.
        """
        return self.end_node

    def type(self) -> EdgeType:
        """!
        """
        return self.etype

    def set_type(self, etype: EdgeType):
        """!
        """
        self.etype = etype

    def node_ids(self) -> Set[str]:
        """!
        \brief Spit out ids of nodes that belong to this edge
        """
        ids = set()
        ids.add(self.start().id())
        ids.add(self.end().id())
        return ids

    def is_endvertice(self, n: Union[Node, str]) -> bool:
        """!
        \brief Check if Node is contained by this edge
        """
        ids = self.node_ids()
        if isinstance(n, str):
            return n in ids
        else:
            return n.id() in ids

    def get_other(self, n: Union[Node, str]) -> Node:
        """!
        """
        if not self.is_endvertice(n):
            raise ValueError("node is not an end vertex")
        cmpv: str = n if isinstance(n, str) else n.id()
        if self.start().id() == cmpv:
            return self.end()
        else:
            return self.start()


"""!
\defgroup edgegroup Edge documentation
\ingroup graphgroup

\section desc_sect Description

Edge is a set of nodes with two members generally designated as E.
...
"""
