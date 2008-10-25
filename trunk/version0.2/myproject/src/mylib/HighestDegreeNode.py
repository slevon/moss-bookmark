class HighestDegreeNode:
    def __init__(self):
        pass
    def getName(self):
        return "Highest degree node"
    def getResult(self,graph): #return dics type
        highestDics = {}
        highestList = []
        highest = 0
        for node in graph:
            if len(graph[node]) > highest:
                highest = len(graph[node])
                highestList = [node]
            elif len(graph[node]) == highest:
                highestList.append(node)
        for node in highestList:
            highestDics[node] = []
        return highestDics

