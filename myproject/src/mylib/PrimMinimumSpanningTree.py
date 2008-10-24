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
        print "Root",root
        print "First edge",minedge
        self.addEdge(minedge, resultGraph)

        while len(resultGraph) < len(graph):
            minedge = self.featherEdge(resultGraph, graph, weigthedGraph)
            print "New edge",minedge
            if minedge != ():
                self.addEdge(minedge, resultGraph)

        '''
        for visited in resultGraph:
            for neb in graph[visited]:
                print "Friend of root",neb
                if not neb in resultGraph:
                    nweight = weigthedGraph.getWeight(visited,neb)
                    if nweight < min:
                        min = nweight
                        minedge = (visited,neb)
        '''
        print "New edge is",minedge
        self.addEdge(minedge, resultGraph)
        #print root,minedge
        return resultGraph
    def featherEdge(self,visitedGraph,graph,weigthedGraph):
        INFINITY = ()
        min = nweight = INFINITY
        minedge = ()
        for visited in visitedGraph:
            for neb in graph[visited]:
                print "Friend of root",neb
                if not neb in visitedGraph:
                    nweight = weigthedGraph.getWeight(visited,neb)
                    if nweight < min:
                        min = nweight
                        minedge = (visited,neb)
        return minedge
    def addEdge(self,edge,graph):
        if edge[0] in graph:
            graph[edge[0]].append(edge[1])
        else:#create new node
            graph[edge[0]] =[edge[1]]

        if edge[1] in graph:
            graph[edge[1]].append(edge[0])
        else:#create new node
            graph[edge[1]] = [edge[0]]
        return graph