# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore
import sys
class MaNode(QtGui.QGraphicsItem):
    Type = QtGui.QGraphicsItem.UserType+1
    def __init__(self,drawWidget,name):
        QtGui.QGraphicsItem.__init__(self)
        self.drawWidget = drawWidget
        self.newPos = QtCore.QPointF()
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable)
        self.name = name
    def type(self):
        return MaItem.Type
    def setName(self,name):
        self.name = name
    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(-10,-10,40,20) #match with Ellipse draw x y w h
        return path
    def paint(self,painter,option,widget):
        painter.setBrush(QtCore.Qt.yellow)
        painter.setPen(QtGui.QPen(QtCore.Qt.black,0))
        painter.drawEllipse(-10,-10,40,20)
        #paint name
        painter.drawText(QtCore.QPointF(7,4),self.name)
    def boundingRect(self):
        adjust = 2.0
        return QtCore.QRectF(-10-adjust,-10-adjust,
                             40 + adjust, 20 + adjust)
class DrawWidget(QtGui.QGraphicsView):
    def __init__(self):
        QtGui.QGraphicsView.__init__(self)
        self.scene = QtGui.QGraphicsScene(self)
        self.scene.setSceneRect(-20,-20,520,520)#scene size 0-500
        self.setScene(self.scene)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.items = []
        self.kownt = 0
    def addNode(self,node):
        print str(type(node))
        if type(node) == str:
            newitem = MaNode(self,node)
            self.items.append(newitem)
            newitem.setPos((self.kownt*5)+100,250)
            newitem.setPos(0,0)
            self.scene.addItem(newitem)
            self.kownt += 1
        elif type(node) == 'MaNode':
            pass
        else:
            pass
        
        

'''Main'''
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))

    widget = DrawWidget()
    widget.addNode("G")
    widget.show()
    sys.exit(app.exec_())
