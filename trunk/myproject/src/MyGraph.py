class MyGraph():
    def __init__(self):
        self.graph = {}
    def addNode(self,node):
        if node in self.graph:
            pass
        else:
            self.graph[node] = []
    def addEdge(self,node1,node2):
        if node1 in self.graph:
            self.graph[node1].append(node2)
        else:
            self.graph[node1] = [node2]
        if node2 in self.graph:
            self.graph[node2].append(node1)
        else:
            self.graph[node2] = [node1]
    def getGraph(self):
        buf = ""
        for node in self.graph:
            buf = buf+str(node)+" -> "+str(self.graph[node])+"\n"
        return buf
    def getNodes(self):
        return self.graph.keys
    def getNodeCount(self):
        return len(self.graph)
    def getEdgeCount(self):
        return len(self.getEdges())
    def getEdges(self):
        edges = set()
        for node in self.graph:
            for neighbor in self.graph[node]:
                edge = set()
                edge.add(node)
                edge.add(neighbor)
                edges.add(tuple(edge))
        return edges
    def getNeighbor(self,nodeName):
        return self.graph[nodeName]

if __name__ == "__main__":
    graph = MyGraph()
    nodes = ['A','B','C','D','E','F','G']
    for node in nodes:
        graph.addNode(node)
    for i in range(len(nodes)):
        if i < len(nodes)-1:
            graph.addEdge(nodes[i],nodes[i+1])
        else:
            graph.addEdge(nodes[0],nodes[6])
    graph.addEdge('A','E')
    graph.addEdge('A','D')
    print type(graph)
    print graph.getGraph()
    print graph.getNodeCount()
    print graph.getEdgeCount()
    print graph.getNeighbor('A')
    for edge in graph.getEdges():
        print edge[0],"->",edge[1]