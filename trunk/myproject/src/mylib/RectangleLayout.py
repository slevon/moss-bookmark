class RectangleLayout:
    def __init__(self):
        pass
    def getInfo(self,gNode):
        for node in gNode:
            print "info node ",node,gNode[node].x(),gNode[node].y()
        pass