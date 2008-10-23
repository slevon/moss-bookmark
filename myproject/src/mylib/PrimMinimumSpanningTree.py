class PrimMinimumSpanningTree:
    def __init__(self):
        pass
    def getName(self):
        return "Prim Minimum Spanning Tree"
    def getResult(self,weigthedGraph):
        resultGraph   = {}
        INFINITY = ()
        graph = weigthedGraph.getGraph()
        root  = "" #init for nothing
        #init root node get first node in graph
        for node in graph:
            root = node
            break
        if root == "": #if no node init
            return resultGraph

        min = INFINITY
        minedge = ()
        for neb in graph[root]:
            nweight = weigthedGraph.getWeight(root,neb)
            if nweight < min:
                min = nweight
                minedge = (root,neb)

        self.addEdge(minedge, resultGraph)
        #print root,minedge
        return resultGraph

    def addEdge(self,edge,graph):
        if edge[0] in graph:
            graph[source].append(edge[1])
        else:#create new node
            graph[edge[0]] =[edge[1]]

        if edge[1] in graph:
            graph[edge[1]].append(edge[0])
        else:#create new node
            graph[edge[1]] = [edge[0]]
        return graph
    def minimal_spanning_tree(graph, root=None):
        visited = []                    # List for marking visited and non-visited nodes
        spanning_tree = {}              # Minimal Spanning tree

        # Initialization
        if (root is not None):
                visited.append(root)
                nroot = root
                spanning_tree[root] = None
        else:
                nroot = 1

        # Algorithm loop
        while (nroot is not None): #if new root is None mean it no node to go
                ledge = lightest_edge(graph, visited)
                if (ledge == (-1, -1)):
                        if (root is not None):
                                break
                        nroot = first_unvisited(graph, visited)
                        if (nroot is not None):
                                spanning_tree[nroot] = None
                        visited.append(nroot)
                else:
                        spanning_tree[ledge[1]] = ledge[0]
                        visited.append(ledge[1])

        return spanning_tree


    def first_unvisited(graph, visited):
        """
        Return first unvisited node.

        @type  graph: graph
        @param graph: Graph.

        @type  visited: list
        @param visited: List of nodes.

        @rtype:  node
        @return: First unvisited node.
        """
        for each in graph:
                if (each not in visited):
                        return each
        return None
    def lightest_edge(graph, visited):
        """
        Return the lightest edge in graph going from a visited node to an unvisited one.

        @type  graph: graph
        @param graph: Graph.

        @type  visited: list
        @param visited: List of nodes.

        @rtype:  tuple
        @return: Lightest edge in graph going from a visited node to an unvisited one.
        """
        lightest_edge = (-1, -1)
        weight = -1
        for each in visited:
                for other in graph[each]:
                        if (other not in visited):
                                w = graph.get_edge_weight(each, other)
                                if (w < weight or weight < 0):
                                        lightest_edge = (each, other)
                                        weight = w
        return lightest_edge
