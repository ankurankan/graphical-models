"""!
Path in a given graph
"""

from typing import Set, Optional, Callable, List, Tuple, Dict, Union
from gmodels.gtypes.edge import Edge, EdgeType
from gmodels.gtypes.node import Node
from gmodels.gtypes.graph import Graph
from gmodels.gtypes.queue import PriorityQueue
from uuid import uuid4
import math


class Tree(Graph):
    """!
    Tree object
    """

    def __init__(self, gid: str, data={}, edges: Set[Edge] = None):
        ""
        nodes = None
        if edges is not None:
            nodes = set()
            for e in edges:
                estart = e.start()
                eend = e.end()
                nodes.add(estart)
                nodes.add(eend)
        super().__init__(gid=gid, data=data, nodes=nodes, edges=edges)
        self.root = self._root()

    @classmethod
    def from_node_tuples(cls, ntpls: Set[Tuple[Node, Node, EdgeType]]):
        ""
        edges: Set[Edge] = set()
        root = None

        for e in ntpls:
            child = e[0]
            parent = e[1]
            edge = Edge(
                edge_id=str(uuid4()), start_node=parent, end_node=child, edge_type=e[2]
            )
            edges.add(edge)
        return Tree(gid=str(uuid4()), edges=edges)

    @classmethod
    def from_edgeset(cls, eset: Set[Edge]):
        ""
        return Tree(gid=str(uuid4()), edges=eset)

    def node_table(self):
        ""
        node_table = {v: {"child": False, "parent": False} for v in self.V}
        for e in self.edges():
            estart_id = e.start().id()
            eend_id = e.end().id()
            node_table[estart_id]["parent"] = True
            node_table[eend_id]["child"] = True
        #
        return node_table

    def _root(self):
        ""
        node_table = self.node_table()
        root_ids = [
            k
            for k, v in node_table.items()
            if v["child"] is False and v["parent"] is True
        ]
        return self.V[root_ids[0]]

    def leaves(self) -> Set[Node]:
        ""
        node_table = self.node_table()
        #
        leave_ids = [
            k
            for k, v in node_table.items()
            if v["child"] is True and v["parent"] is False
        ]
        return set([self.V[v] for v in leave_ids])

    def root_node(self) -> Node:
        ""
        return self.root

    def upset_of(self, n: Node) -> Set[Node]:
        ""
        raise NotImplementedError

    def downset_of(self, n: Node) -> Set[Node]:
        ""
        raise NotImplementedError

    def less_than_or_equal(self, first: Node, second: Node) -> bool:
        ""
        raise NotImplementedError

    def greater_than_or_equal(self, first: Node, second: Node) -> bool:
        ""
        raise NotImplementedError

    @classmethod
    def find_mst_prim(
        cls, g: Graph, edge_generator: Callable[[Node], Set[Node]]
    ) -> Graph:
        """!
        Find minimum spanning tree as per Prim's algorithm
        Even and Guy Even 2012, p. 32
        """
        l_e = 1  # length of an edge
        l_vs = {}
        vs = []
        eps = {}

        for v in g.V:
            l_vs[v] = math.inf
            vs.append(v)
        #
        s = vs[0]
        l_vs[s] = 0
        eps[s] = set()
        TEMP = vs.copy()
        T: Set[Edge] = set()
        while TEMP:
            minv = None
            minl = math.inf
            for v in TEMP:
                if l_vs[v] < minl:
                    minl = l_vs[v]
                    minv = v
            TEMP = [v for v in TEMP if v != minv]
            if minv is None:
                raise ValueError(
                    "Min vertex is not found. Graph is probably not connected"
                )
            T = T.union(eps[minv])
            for edge in edge_generator(g.V[minv]):
                unode = edge.get_other(g.V[minv])
                u = unode.id()
                if u in TEMP and l_vs[u] > l_e:
                    l_vs[u] = l_e
                    eps[u] = set([edge])
        return cls.from_edgeset(eset=T)

    @classmethod
    def find_mnmx_st(
        cls,
        g: Graph,
        edge_generator: Callable[[Node], Set[Edge]],
        weight_function: Callable[[Edge], float] = lambda x: 1,
        is_min: bool = True,
    ):
        """!
        a modified version of kruskal minimum spanning tree adapted for
        finding minimum and maximum weighted spanning tree of a graph

        from Even and Guy Even 2012, p. 42
        """
        queue = PriorityQueue(is_min=is_min)
        T: Set[Edge] = set()
        clusters = {v: set([v]) for v in g.V}
        L: List[Edge] = []
        for e, edge in g.E.items():
            queue.insert(weight_function(edge), edge)
        #
        while len(queue) > 0:
            edge = None
            if is_min is True:
                k, edge = queue.min()
            else:
                k, edge = queue.max()
            #
            u = edge.start().id()
            v = edge.end().id()
            vset = clusters[v]
            uset = clusters[u]
            if vset != uset:
                T.add(edge)
                L.append(edge)
                clusters[v] = vset.union(uset)
                clusters[u] = vset.union(uset)
        return cls.from_edgeset(eset=T), L

    #
    def assign_num(
        self,
        v: str,
        num: Dict[str, int],
        visited: Dict[str, bool],
        parent: Dict[str, str],
        counter: int,
        generative_fn: Callable[[Node], Set[Node]],
    ):
        ""
        counter += 1
        num[v] = counter
        visited[v] = True
        vnode = self.V[v]
        for unode in generative_fn(vnode):
            u = unode.id()
            cond = visited.get(u)
            if cond is None or cond is False:
                parent[u] = v
                self.assign_num(
                    u,
                    num=num,
                    generative_fn=generative_fn,
                    visited=visited,
                    parent=parent,
                    counter=counter,
                )

    #
    def check_ap(
        self,
        v: str,
        num: Dict[str, int],
        visited: Dict[str, bool],
        parent: Dict[str, str],
        low: Dict[str, int],
        counter: int,
        aset: Set[str],
        generative_fn: Callable[[Node], Set[Node]],
    ):
        ""
        low[v] = num[v]
        vnode = self.V[v]
        for unode in generative_fn(vnode):
            u = unode.id()
            if num[u] >= num[v]:
                self.check_ap(
                    v=u,
                    num=num,
                    visited=visited,
                    parent=parent,
                    low=low,
                    counter=counter,
                    generative_fn=generative_fn,
                    aset=aset,
                )
                if low[u] >= num[v]:
                    aset.add(v)
                #
                low[v] = min(low[v], low[u])
            elif parent[v] != u:
                low[v] = min(low[v], num[u])

    def find_separating_vertices(
        self, generative_fn: Callable[[Node], Set[Node]]
    ) -> Set[Node]:
        """!
        find separating vertices of graph
        as in Erciyes 2018, p. 230, algorithm 8.3
        """
        num: Dict[str, float] = {n: math.inf for n in self.V}
        low: Dict[str, float] = {n: math.inf for n in self.V}
        visited: Dict[str, bool] = {}
        parent: Dict[str, str] = {n: "" for n in self.V}
        aset: Set[str] = set()

        counter = 1
        v = [node for node in self.V][0]
        self.assign_num(
            v=v,
            num=num,
            visited=visited,
            parent=parent,
            counter=counter,
            generative_fn=generative_fn,
        )
        self.check_ap(
            v=v,
            num=num,
            visited=visited,
            generative_fn=generative_fn,
            parent=parent,
            low=low,
            counter=counter,
            aset=aset,
        )
        return set([self.V[a] for a in aset])