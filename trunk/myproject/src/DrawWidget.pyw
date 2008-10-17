# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore

import sys
import random
import math
class MaNode(QtGui.QGraphicsItem):
    Type     = QtGui.QGraphicsItem.UserType+1
    NHigh    = 30
    NWigth   = 30
    Unhighlight = 0
    Highlight = 1
    HLC = 0 #HighLight and mouse Click
    HLN = 1 #HighLight and No mouse click
    ULC = 2 #UnhighLight and mouse Click
    ULN = 3 #UnhighLinht and No mouse click

    def __init__(self,graphWidget,name):
        QtGui.QGraphicsItem.__init__(self)
        #self.drawWidget = drawWidget
        self.graph = graphWidget
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setZValue(1)#node is alway on top over the edge
        self.name = name
        self.paintStatus = MaNode.Unhighlight
    def type(self):
        return MaNode.Type
    def setName(self,name):
        self.name = name
    def getName(self):
        return self.name
    def getBGStyle(self,gNodeType):
        penstyle = QtGui.QRadialGradient(-(MaNode.NWigth*(3/10)),
                                          -(MaNode.NHigh*(3/10)),
                                          MaNode.NWigth)

        if gNodeType == MaNode.HLC:#High light click
            penstyle.setCenter((MaNode.NWigth*(3/10)),
                                    (MaNode.NHigh*(3/10)))
            penstyle.setFocalPoint((MaNode.NWigth*(3/10)),
                                    (MaNode.NHigh*(3/10)))
            penstyle.setColorAt(0,QtGui.QColor(QtCore.Qt.blue).light(170))
            penstyle.setColorAt(1,QtGui.QColor(QtCore.Qt.darkBlue).light(220))
        elif gNodeType == MaNode.ULC:
            penstyle.setCenter((MaNode.NWigth*(3/10)),
                                    (MaNode.NHigh*(3/10)))
            penstyle.setFocalPoint((MaNode.NWigth*(3/10)),
                                    (MaNode.NHigh*(3/10)))
            penstyle.setColorAt(0,QtGui.QColor(QtCore.Qt.yellow).light(120))
            penstyle.setColorAt(1,QtGui.QColor(QtCore.Qt.darkYellow).light(120))
        elif gNodeType == MaNode.HLN:#High light No click
            penstyle.setColorAt(0,QtGui.QColor(QtCore.Qt.blue).light(120))#zero is center out
            penstyle.setColorAt(1,QtGui.QColor(QtCore.Qt.blue).light(170))#one is border in
        elif gNodeType == MaNode.ULN:
            penstyle.setColorAt(1,QtGui.QColor(QtCore.Qt.yellow))
            penstyle.setColorAt(0,QtGui.QColor(QtCore.Qt.darkYellow).light(150))
        return penstyle

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-(MaNode.NWigth/2),
                            -(MaNode.NHigh/2),
                            MaNode.NWigth,
                            MaNode.NHigh) #match with Ellipse draw x y w h
        return path
    def paint(self,painter,option,widget):
        #if select highlight node
        if option.state & QtGui.QStyle.State_Sunken:
            if self.paintStatus == MaNode.Highlight:
                painter.setBrush(self.getBGStyle(MaNode.HLC))
            else:
                painter.setBrush(self.getBGStyle(MaNode.ULC))
        else:
            if self.paintStatus == MaNode.Highlight:
                painter.setBrush(self.getBGStyle(MaNode.HLN))
            else:
                painter.setBrush(self.getBGStyle(MaNode.ULN))
        #painter.setBrush(QtCore.Qt.yellow)
        painter.setPen(QtGui.QPen(QtCore.Qt.black,0))
        painter.drawEllipse(-(MaNode.NWigth/2),
                            -(MaNode.NHigh/2),
                            MaNode.NWigth,
                            MaNode.NHigh)
        #paint name -3,2 vary by font size
        painter.drawText(QtCore.QPointF(-3,2),self.name)
    def boundingRect(self): #require
        adjust = 2.0
        return QtCore.QRectF(-(MaNode.NWigth/2)-adjust,
                             -(MaNode.NHigh/2)-adjust,
                             MaNode.NWigth+adjust,MaNode.NHigh+adjust)
    def addGEdge(self,edge):
        edge.adjust()
    #move edge follow node when node move
    def itemChange(self,change,value):
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            gEdges = self.graph.getGEdgesOf(self.name)
            for gEdge in gEdges:
                gEdge.adjust()
        return QtGui.QGraphicsItem.itemChange(self,change,value)
    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)
    def mouseReleaseEvent(self,event):
        self.update()
        #update edge
        gEdges = self.graph.getGEdgesOf(self.name)
        for gEdge in gEdges:
            gEdge.adjust()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
class MaEdge(QtGui.QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi
    Unhighlight = 0
    Highlight = 1
    Type = QtGui.QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)

        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.setZValue(0)#edge is alway on below the node
        self.source = sourceNode
        self.dest = destNode
        self.paintStatus = MaEdge.Unhighlight
        self.source.addGEdge(self)
        self.dest.addGEdge(self)
        self.adjust()

    def type(self):
        return Edge.Type

    def sourceNode(self):
        return self.source

    def setSourceNode(self, node):
        self.source = node
        self.adjust()

    def destNode(self):
        return self.dest

    def setDestNode(self, node):
        self.dest = node
        self.adjust()
    def adjust(self):
        if not self.source or not self.dest:
            return

        line = QtCore.QLineF(self.mapFromItem(self.source, 0, 0), self.mapFromItem(self.dest, 0, 0))
        length = line.length()

        if length == 0.0:
            return

        edgeOffset = QtCore.QPointF((line.dx()) / length, (line.dy()) / length)

        self.prepareGeometryChange()
        self.sourcePoint = line.p1() + edgeOffset
        self.destPoint = line.p2() - edgeOffset

    def boundingRect(self):
        if not self.source or not self.dest:
            return QtCore.QRectF()

        penWidth = 1
        extra = penWidth / 2.0

        return QtCore.QRectF(self.sourcePoint,
                             QtCore.QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                                           self.destPoint.y() - self.sourcePoint.y())
                             ).normalized().adjusted(-extra, -extra, extra, extra)

    def paint(self, painter, option, widget):
        if not self.source or not self.dest:
            return

        # Draw the line itself.
        line = QtCore.QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return
        if self.paintStatus == MaEdge.Highlight:
            painter.setPen(QtGui.QPen(QtCore.Qt.red, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        else:
            painter.setPen(QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawLine(line)

        # Draw the arrows if there's enough room.
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = MaEdge.TwoPi - angle

        #sourceArrowP1 = self.sourcePoint + QtCore.QPointF(math.sin(angle + MaEdge.Pi / 3) * self.arrowSize,
        #                                                  math.cos(angle + MaEdge.Pi / 3) * self.arrowSize)
        #sourceArrowP2 = self.sourcePoint + QtCore.QPointF(math.sin(angle + MaEdge.Pi - MaEdge.Pi / 3) * self.arrowSize,
        #                                                  math.cos(angle + MaEdge.Pi - MaEdge.Pi / 3) * self.arrowSize);
        #destArrowP1 = self.destPoint + QtCore.QPointF(math.sin(angle - MaEdge.Pi / 3) * self.arrowSize,
        #                                              math.cos(angle - MaEdge.Pi / 3) * self.arrowSize)
        #destArrowP2 = self.destPoint + QtCore.QPointF(math.sin(angle - MaEdge.Pi + MaEdge.Pi / 3) * self.arrowSize,
        #                                              math.cos(angle - MaEdge.Pi + MaEdge.Pi / 3) * self.arrowSize)

        painter.setBrush(QtCore.Qt.black)
        #painter.drawPolygon(QtGui.QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
        #painter.drawPolygon(QtGui.QPolygonF([line.p2(), destArrowP1, destArrowP2]))

class DrawWidget(QtGui.QGraphicsView):
    scensSize = 400
    drawSize  = 400
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setSceneRect(-20,-20,DrawWidget.scensSize+20,DrawWidget.scensSize+20)#scene size 0-500
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graph = {} #set of all nodes point to neightbor as edges in str information
        self.gGraph = {} #set of all nodes point to gEdge
        self.gNode = {}
        self.gEdge = {}
        self.kownt = 0
    def addNode(self,node):
        if type(node) == str:
            if self.hasNode(node):
                QtGui.QMessageBox.information(self,"Wrong input","Has node \"%s\" already"%(node))
                #print "Has node %s already"%(node)
                return
            if node == "":
                QtGui.QMessageBox.information(self,"Wrong input","Node name is empty")
                #print "Empty name add node"
                return
            newitem = MaNode(self,node)
            self.graph[node] = []
            self.gGraph[node] = []
            self.gNode[node] = newitem
            newitem.setPos(random.randint(0,DrawWidget.drawSize),random.randint(0,DrawWidget.drawSize))
            self.scene.addItem(newitem)
            self.kownt += 1
        elif type(node) == 'MaNode':
            pass
        else:
            pass
    def addEdge(self,source,dest):
        #create Edge by name
        if self.hasEdge(source, dest):
            print "Has edge",source,'<==>',dest,'already'
            return
        if (type(source) == str) and (type(dest) == str):

            #add to graph skeleton
            if source == "" or dest == "":
                print "Empty name add edge"
                return

            if source in self.graph:
                self.graph[source].append(dest)
            else:#create new node
                self.addNode(source)
                self.graph[source] =[dest]

            if dest in self.graph:
                self.graph[dest].append(source)
            else:#create new node
                self.addNode(dest)
                self.graph[dest] = [source]
            #create graphic object
            newGEdge = MaEdge(self.gNode[source],self.gNode[dest])
            if source in self.graph:
                self.gGraph[source].append(newGEdge)
            else:#create new node
                self.gGraph[source] = [newGEdge]

            if dest in self.graph:
                self.gGraph[dest].append(newGEdge)
            else:
                self.gGraph[dest] = [newGEdge]
            #add to graphic widget

            if not(source,dest) in self.gEdge \
            or not(dest,source) in self.gEdge:
                self.gEdge[(source,dest)] = newGEdge
            self.scene.addItem(newGEdge)
    def delNode(self,node):
        if node in self.graph:
            self.scene.removeItem(self.gNode[node])
            neightbors = self.graph[node]#get all edge point to it and del it of
            print "Edges of",node,self.graph[node]
            for neightbor in neightbors:
                if (node,neightbor) in self.gEdge:
                    self.scene.removeItem(self.gEdge[(node,neightbor)])

                elif  (neightbor,node) in self.gEdge:
                    self.scene.removeItem(self.gEdge[(neightbor,node)])
                print "Del %s to %s"%(node,neightbor)
                self.graph[neightbor].remove(node)
            del self.gNode[node]
            del self.graph[node]

    def delEdge(self,source,dest):
        if (source,dest) in self.gEdge:
            self.scene.removeItem(self.gEdge[(source,dest)])
        elif  (dest,source) in self.gEdge:
            self.scene.removeItem(self.gEdge[(dest,source)])
        if dest in self.graph[source]:
            self.graph[source].remove(dest)
            self.graph[dest].remove(source)
        pass
    def toString(self):
        result = ""
        for node in self.graph:
            result += node+" -> "+str(self.graph[node])+"\n"
        return result
    def getNodesName(self):
        result = []
        for gnode in self.gNode:
            result += gnode
        return result
    #def getGNode(self,name):
    def getGraph(self):
        return self.graph
    def getEdgesOf(self,nodeName):
        if nodeName in self.graph:
            return self.graph[nodeName]

    def getEdges(self):
        result = set()
        for key in self.graph:
            neighbors = self.graph[key]
            for neighbor in neighbors:
                #not have this edge before
                if not (key,neighbor) or not (neighbor,key) in result:
                    result.add((key,neighbor))
        return result

    def getGEdgesOf(self,nodeName):
        return self.gGraph[nodeName]
    def getGEdge(self,source,dest):
        for gEdge in self.gGraph[source]:
            if gEdge in self.gGraph[dest]:
                return gEdge
    def hasEdge(self,source,dest):
        if source in self.graph and dest in self.graph:
            if source in self.graph[dest]:
                return True
            else:
                return False
        else:
            return False
    def hasNode(self,nodeName):
        if nodeName in self.graph:
            return True
        return False

    def getAllGEdges(self):
        result = []
        for node in self.graph:
            result.extend(self.gEdge(node))
        return result

    #zoomable feature
    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.delta() / 240.0))
    def scaleView(self, scaleFactor):
        factor = self.matrix().scale(scaleFactor, scaleFactor).mapRect(QtCore.QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)
'''Main'''
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))

    widget = DrawWidget()
    widget.addNode("G")
    widget.addNode("B")
    #widget.addNode("A")
    widget.addEdge("G", "B")
    widget.addEdge("Z","A")
    widget.addEdge("Z","B")
    widget.addEdge("A","B")
    widget.addEdge("A","G")
    widget.addEdge("C","A")
    widget.addEdge("C","B")
    widget.addEdge("C","G")
    widget.gNode["A"].paintStatus = MaNode.Highlight
    widget.gNode["Z"].paintStatus = MaNode.Highlight
    widget.getGEdge("A","Z").paintStatus = MaEdge.Highlight
    #highestList,highestValue = SimpleAlgorithm.highestDegreeNode(widget.getGraph())
    #print "Highest degree node list",highestList
    #print "Max at",highestValue
    #for resultNode in highestList:
    #    widget.gNode[resultNode].paintStatus = MaNode.Highlight
    #widget.delEdge("A","B")
    print "Graph toString",widget.toString()
    print "Get edge of A is",widget.getEdgesOf("A")
    print "Get edge of B is",widget.getEdgesOf("B")
    print "Nodes name",widget.getNodesName()
    print "Hole graph",widget.getGraph()
    print "All Edges",widget.getEdges()
    widget.show()
    sys.exit(app.exec_())
