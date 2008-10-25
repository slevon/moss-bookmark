class LeafNode:
    def __init__(self):
        pass
    def getName(self):
        return "Leaf node"
    def getResult(self,graph):
        leafList = []
        leafDics = {}
        for node in graph:
            if len(graph[node]) == 0:
                leafList.append(node)
        for node in leafList:
            leafDics[node] = []
        return leafDics