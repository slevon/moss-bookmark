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
        queue = []
        for node in graph:
            queue.append(node)
        if len(queue)==0: #if no node init #double check
            return resultGraph,{}


        minedge = ()
        weightRecord = {}
        totalWeight = INFINITY
        for root in queue:
            weightRecordBuff = {}
            result = {}
            min = INFINITY
            for node in graph:
                weightRecordBuff[node] = INFINITY
            weightRecordBuff[root] = 0

            for neb in graph[root]:
                nweight = weigthedGraph.getWeight(root,neb)+weightRecordBuff[root]
                if nweight < weightRecordBuff[neb]:
                    weightRecordBuff[neb] = nweight
                if nweight < min:
                    min = nweight
                    minedge = (root,neb)
            self.addEdge(minedge, result)

            while len(result) < len(graph):
                minedge = self.featherEdge(result,weightRecordBuff, graph, weigthedGraph)
                if minedge != ():
                    self.addEdge(minedge, result)

            total = 0
            for element in weightRecordBuff:
                total += weightRecordBuff[element]
            if total < totalWeight:
                totalWeight = total
                resultGraph = result
                weightRecord = weightRecordBuff

        return resultGraph,weightRecord

    def featherEdge(self,visitedGraph,weightRecord,graph,weigthedGraph):
        INFINITY = ()
        min = nweight = INFINITY
        minedge = ()
        for visited in visitedGraph:
            for neb in graph[visited]:
                if not neb in visitedGraph:
                    nweight = weigthedGraph.getWeight(visited,neb)+weightRecord[visited]
                    if nweight < weightRecord[neb]:
                        weightRecord[neb] = nweight
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