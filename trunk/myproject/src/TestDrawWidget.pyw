# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import sys
import random
import math
class MaNode(QtGui.QGraphicsItem):
    Type     = QtGui.QGraphicsItem.UserType+1
    NHigh    = 30
    NWigth   = 30
    def __init__(self,graphWidget,name):
        QtGui.QGraphicsItem.__init__(self)
        #self.drawWidget = drawWidget
        self.graph = graphWidget
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.setZValue(1)#node is alway on top over the edge
        self.name = name
    def type(self):
        return MaNode.Type
    def setName(self,name):
        self.name = name
    def getName(self):
        return self.name
    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-(MaNode.NWigth/2),
                            -(MaNode.NHigh/2),
                            MaNode.NWigth,
                            MaNode.NHigh) #match with Ellipse draw x y w h
        return path
    def paint(self,painter,option,widget):
        grandient = QtGui.QRadialGradient(-(MaNode.NWigth/5),
                                          -(MaNode.NHigh/5),
                                          MaNode.NWigth)
        #if select highlight node
        if option.state & QtGui.QStyle.State_Sunken:
            grandient.setCenter((MaNode.NWigth/3),
                                (MaNode.NHigh/3))
            grandient.setFocalPoint((MaNode.NWigth/3),
                                (MaNode.NHigh/3))
            grandient.setColorAt(1,QtGui.QColor(QtCore.Qt.yellow).light(120))
            grandient.setColorAt(0,QtGui.QColor(QtCore.Qt.darkYellow).light(120))

        else:
            grandient.setColorAt(1,QtGui.QColor(QtCore.Qt.yellow).light(120))
            grandient.setColorAt(0,QtGui.QColor(QtCore.Qt.darkYellow).light(120))

        #painter.setBrush(QtCore.Qt.yellow)
        painter.setBrush(QtGui.QBrush(grandient))
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
    def itemChange(self,change,value):
        if change == QtGui.QGraphicsItem.ItemPositionChange:
            print self.graph.getEdge(self.name)
        return QtGui.QGraphicsItem.itemChange(self,change,value)
    def mousePressEvent(self, event):
        self.update()
        QtGui.QGraphicsItem.mousePressEvent(self, event)
    def mouseReleaseEvent(self,event):
        self.update()
        QtGui.QGraphicsItem.mouseReleaseEvent(self, event)
class MaEdge(QtGui.QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QtGui.QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        QtGui.QGraphicsItem.__init__(self)

        self.sourcePoint = QtCore.QPointF()
        self.destPoint = QtCore.QPointF()
        self.setAcceptedMouseButtons(QtCore.Qt.NoButton)
        self.setZValue(0)#edge is alway on below the node
        self.source = sourceNode
        self.dest = destNode

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
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setSceneRect(-20,-20,520,520)#scene size 0-500
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.graph = {}
        self.gNode = {}
        self.gEdge = {}
        self.kownt = 0
    def addNode(self,node):
        if type(node) == str:
            newitem = MaNode(self,node)
            self.graph[node] = []
            self.gNode[node] = newitem
            newitem.setPos(random.randint(0,500),random.randint(0,500))
            self.scene.addItem(newitem)
            self.kownt += 1
        elif type(node) == 'MaNode':
            pass
        else:
            pass
    def addEdge(self,source,dest):
        if (type(source) == str) and (type(dest) == str):
            #create Edge by name

            #add to graph skeleton
            if source in self.graph:
                self.graph[source].append(dest)
            else:#create new node
                self.addNode(source)
                self.graph[source] =[dest]
                print self.graph[source]


            if dest in self.graph:
                self.graph[dest].append(source)
            else:#create new node
                self.addNode(dest)
                self.graph[dest] = [source]

            #add to graphic widget
            newGEdge = MaEdge(self.gNode[source],self.gNode[dest])
            if source in self.gEdge:
                self.gEdge[source].append(newGEdge)
            else:
                self.gEdge[source] = [newGEdge]
            if dest in self.gEdge:
                self.gEdge[dest].append(newGEdge)
            else:
                self.gEdge[dest] = [newGEdge]
            self.scene.addItem(MaEdge(self.gNode[source],self.gNode[dest]))
        else:
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
    def getEdge(self,nodeName):
        return self.graph[nodeName]
    def getGEdge(self,nodeName):
        return self.gEdge[nodeName]



'''Main'''
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))

    widget = DrawWidget()
    widget.addNode("G")
    widget.addNode("B")
    #widget.addNode("A")
    widget.addEdge("G", "B")
    widget.addEdge("A","B")
    print "Graph toString",widget.toString()
    print "Get edge of A is",widget.getEdge("A")
    print "Get edge of B is",widget.getEdge("B")
    print "Nodes name",widget.getNodesName()
    widget.show()
    sys.exit(app.exec_())
