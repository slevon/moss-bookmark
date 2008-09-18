from JeremyQueue import JeremyQueue
from PyQt4 import QtGui
class BreadthFirstTree:
    def __init__(self):
        pass
    def getName(self):
        return "Breadth-First Traversal of a Tree"
    def getResult(self,graph,rootNode):
        resultGraph   = {}
        traversal = set()
        waitQueue = []
        if rootNode in graph:
            print "root node in graph"
            #set frind of root node
            waitQueue.append(rootNode)
            while len(waitQueue):#zero is false
                traverseNode = waitQueue.pop(0)
                traversal.add(traverseNode)
                for neightbor in graph[traverseNode]:
                    if (not neightbor in traversal) and \
                       (not neightbor in waitQueue):

                        waitQueue.append(neightbor)
                        if traverseNode in resultGraph:
                            resultGraph[traverseNode].append(neightbor)
                        else:
                            resultGraph[traverseNode] = [neightbor]
                        if neightbor in resultGraph:
                            resultGraph[neightbor].append(traverseNode)
                        else:
                            resultGraph[neightbor] = [traverseNode]
        print resultGraph
        return resultGraph
if __name__ == "__main__":
    graph = {}
    graph['a'] = ['b','c']
    graph['b'] = ['a','c','d','e']
    graph['c'] = ['a','b','f','g']
    graph['d'] = ['b','g']
    graph['e'] = ['b','f']
    graph['f'] = ['c','e']
    graph['g'] = ['c','d']
    bst = BreadthFirstTree()
    bst.getResult(graph,['a'])

