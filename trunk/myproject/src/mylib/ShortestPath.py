'''
Dijkstra's algorithm for shortest path
'''
class ShortestPath:
    def __init__(self):
        pass
    def getName(self):
        return "Dijkstra shortest path"
    def getResult(self,weigthedGraph,source,dest):
        '''
        return list off new graph,weight for every node

        '''
        #none sence case{
        if source == dest:
            return {source:[]}
        graph = weigthedGraph.getGraph()
        if not source in graph or not dest in graph:
            print "Does not has source or dest in this graph"
            return {},{source:0}
        #}none sence case
        #define
        INFINITY = ()

        #variable
        resultGraph   = {} # node : neightbors list
        weightRecord  = {} # node : weight record

        #preprocess

        minedge = ()
        for node in graph:
            weightRecord[node] = INFINITY
        weightRecord[source] = 0

        #starting weight of min weight for find the real min weight
        min = INFINITY
        for neb in graph[source]:
            # new weight for node
            nweight = weigthedGraph.getWeight(source,neb)+weightRecord[source]
            if nweight < weightRecord[neb]:
                weightRecord[neb] = nweight
            if nweight < min:
                min = nweight
                minedge = (source,neb)

        self.addEdge(minedge, resultGraph)

        if dest in minedge:
            return resultGraph,weightRecord

        #while len(resultGraph) < len(graph): #wrost case
        min = INFINITY
        while len(resultGraph) < len(graph): #wrost case
            minedge = self.featherEdge(resultGraph, weightRecord, graph, weigthedGraph)
            if minedge != ():
                self.addEdge(minedge, resultGraph)
            if dest in minedge:
                break
        #print root,minedge

        tree = self.backtrack(resultGraph, source, dest)
        resultGraph = {}
        for i in range(len(tree)):
            if i == 0:
                resultGraph[tree[i]] = [tree[i+1]]
            elif i < len(tree)-1 and i != 0:
                resultGraph[tree[i]] = [tree[i+1]]
                resultGraph[tree[i]].append(tree[i-1])
            elif i == len(tree)-1:
                resultGraph[tree[i]] = [tree[i-1]]
        print resultGraph
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
    def backtrack(self,tree,source,dest):
        print "Tree",tree
        print "Source",source
        print "Dest",dest
        resultStack = []
        resultStack.append(source)
        if source == dest:#none sence case
            return [source]
        resultStack.append(source)
        self.found = False
        print "Begin stack",resultStack
        for neb in tree[source]:
            print "Current neb",neb
            resultStack.pop()
            if neb == dest:#found
                resultStack.append(neb)
                return resultStack
            else:
                resultStack.append(neb)
                print "Current stack",resultStack
                self.goDeep(dest,source,tree,neb,resultStack)

            if self.found:
                break
            resultStack.append(source)
            print "Before end loop stack",resultStack
        return resultStack
    def goDeep(self,dest,parentNode,tree,current,resultStack):
        #if len(tree[current]) == 1:#leaf node
        #    if tree[current] != dest:
        #        return
        print "Deep stack",resultStack
        for neb in tree[current]:
            if neb != parentNode:
                if neb == dest:
                    resultStack.append(neb)
                    print "Founddddd"
                    print "Stack list",resultStack
                    self.found = True
                    return
                else:
                    print "Found status",self.found
                    resultStack.append(neb)
                    print "Before go Deep",resultStack
                    self.goDeep(dest, current, tree, neb, resultStack)
                if self.found:
                    return
            else:
                pass
        resultStack.pop()

