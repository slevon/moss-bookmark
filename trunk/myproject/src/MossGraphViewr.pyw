import sys
import imp

from mylib.HighestDegreeNode import HighestDegreeNode
from mylib.LeafNode          import LeafNode
from mylib.BreadthFirstTree  import BreadthFirstTree
from mylib.GraphMLHelpr      import GraphMLHelpr
from mylib.LayoutInfo        import LayoutInfo
from mylib.PrimMinimumSpanningTree import PrimMinimumSpanningTree
from mylib.ShortestPath      import ShortestPath

from DrawWidget              import DrawWidget,MaNode,MaEdge

from PyQt4                   import QtCore, QtGui
from xml.dom                 import minidom



class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.createActions()
        self.createMenus()
        self.resize(1000,650)
        #test addWidget area
        self.mygraph = DrawWidget()

        #set icon of the application
        self.setWindowIcon(QtGui.QIcon('../images/app_icon.png'))
        self.file_dir_hist = "."
        #set title of the application
        self.setCentralWidget(self.mygraph)
        self.welcome()
        self.setWindowTitle('Moss Graph Viewr Qt')
        self.setCenterScreen()

    def createActions(self):
        #file{
        self.newMenu = QtGui.QAction(self.tr("&New graph"),self)
        self.newMenu.setShortcut('Alt+Shift+N')
        self.connect(self.newMenu,QtCore.SIGNAL('triggered()'),self.newGraph)

        self.openFileMenu = QtGui.QAction(self.tr("&Open file"),self)
        self.openFileMenu.setShortcut('Ctrl+O')
        self.connect(self.openFileMenu,QtCore.SIGNAL('triggered()'),self.openFile)

        self.saveFileMenu = QtGui.QAction(self.tr("&Save as"),self)
        self.saveFileMenu.setShortcut('Ctrl+S')
        self.connect(self.saveFileMenu,QtCore.SIGNAL('triggered()'),self.saveFile)

        self.exitMenu = QtGui.QAction(QtGui.QIcon('../images/close.png'),self.tr("&Exit"), self)
        self.exitMenu.setShortcut('Ctrl+Q')
        self.connect(self.exitMenu,QtCore.SIGNAL('triggered()'),
                     QtGui.qApp,QtCore.SLOT('quit()'))
        #}file
        #graph{
        self.addNodeMenu = QtGui.QAction(self.tr("&Add New Node"),self)
        self.addNodeMenu.setShortcut('Ctrl+N')
        self.connect(self.addNodeMenu,QtCore.SIGNAL("triggered()"),self.addNode)

        self.addEdgeMenu = QtGui.QAction(self.tr("&Add New Edge"),self)
        self.addEdgeMenu.setShortcut('Ctrl+E')
        self.connect(self.addEdgeMenu,QtCore.SIGNAL("triggered()"),self.addEdge)

        self.delNodeMenu = QtGui.QAction(self.tr("&Remove Node"),self)
        self.delNodeMenu.setShortcut('Ctrl+Shift+N')
        self.connect(self.delNodeMenu,QtCore.SIGNAL("triggered()"),self.delNode)

        self.delEdgeMenu = QtGui.QAction(self.tr("&Remove Edge"),self)
        self.delEdgeMenu.setShortcut('Ctrl+Shift+E')
        self.connect(self.delEdgeMenu,QtCore.SIGNAL("triggered()"),self.delEdge)

        self.setWeightMenu = QtGui.QAction(self.tr("&Set weight"),self)
        self.setWeightMenu.setShortcut('Ctrl+W')
        self.connect(self.setWeightMenu,QtCore.SIGNAL("triggered()"),self.setWeight)

        self.graphInfoMenu = QtGui.QAction(self.tr("&Graph info"),self)
        self.graphInfoMenu.setShortcut('Ctrl+G')
        self.connect(self.graphInfoMenu,QtCore.SIGNAL("triggered()"),self.infoGraph)

        self.animateMenu = QtGui.QAction(self.tr("&Stop animate"),self)
        self.connect(self.animateMenu,QtCore.SIGNAL("triggered()"),self.animateStatus)
        #}graph
        #algorithm{
        self.highestDegreeMenu = QtGui.QAction(self.tr("&Highest Degree Node"),self)
        self.connect(self.highestDegreeMenu,QtCore.SIGNAL("triggered()")
                 ,self.highestDegree)
        self.bstMenu = QtGui.QAction(self.tr("&Breadth first traversal tree"),self)
        self.connect(self.bstMenu,QtCore.SIGNAL("triggered()"),self.bstTree)

        self.mstMenu = QtGui.QAction(self.tr("&Prim Minimum Spanning Tree"),self)
        self.connect(self.mstMenu,QtCore.SIGNAL("triggered()"),self.mstTree)

        self.shtMenu = QtGui.QAction(self.tr("&Dijkstra shortest path"),self)
        self.connect(self.shtMenu,QtCore.SIGNAL("triggered()"),self.shtPath)
        #}algorithm
        #layout{
        #self.layoutInfoMenu = QtGui.QAction(self.tr("&Layout info"),self)
        #self.connect(self.layoutInfoMenu,QtCore.SIGNAL("triggered()")
        #             ,self.layoutInfo)
        #}layout
        #help{
        self.aboutActMenu = QtGui.QAction(self.tr("&About"), self)
        self.connect(self.aboutActMenu, QtCore.SIGNAL("triggered()"), self.about)

        self.aboutQtActMenu = QtGui.QAction(self.tr("About &Qt"), self)
        self.connect(self.aboutQtActMenu, QtCore.SIGNAL("triggered()"), QtGui.qApp, QtCore.SLOT("aboutQt()"))
        #}help

    def createMenus(self):
        self.filemenu = self.menuBar().addMenu(self.tr("&File"))
        self.filemenu.addAction(self.newMenu)
        self.filemenu.addAction(self.openFileMenu)
        self.filemenu.addAction(self.saveFileMenu)
        self.filemenu.addAction(self.exitMenu)

        self.graphmenu = self.menuBar().addMenu(self.tr("&Graph"))
        self.graphmenu.addAction(self.addNodeMenu)
        self.graphmenu.addAction(self.addEdgeMenu)
        self.graphmenu.addAction(self.delNodeMenu)
        self.graphmenu.addAction(self.delEdgeMenu)
        self.graphmenu.addAction(self.setWeightMenu)
        self.graphmenu.addAction(self.graphInfoMenu)
        self.graphmenu.addAction(self.animateMenu)

        self.algoMenu = self.menuBar().addMenu(self.tr("&Algorithm"))
        self.algoMenu.addAction(self.highestDegreeMenu)
        self.algoMenu.addAction(self.bstMenu)
        self.algoMenu.addAction(self.mstMenu)
        self.algoMenu.addAction(self.shtMenu)
        #self.layoutMenu = self.menuBar().addMenu(self.tr("&Layout"))
        #self.layoutMenu.addAction(self.layoutInfoMenu)

        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.aboutActMenu)
        self.helpMenu.addAction(self.aboutQtActMenu)

    def setCenterScreen(self):
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,
                  (screen.height()-size.height())/2
                  )
    #reimplement the closeEvent() event handler.
    #QWidget method i think
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
    def welcome(self):
        self.mygraph.addEdge("W", "e")
        self.mygraph.setWeight(4.0, "W", "e")
        self.mygraph.addEdge("e", "l")
        self.mygraph.setWeight(7.0, "e", "l")
        self.mygraph.addEdge("l", "c")
        self.mygraph.setWeight(2.0, "l", "c")
        self.mygraph.addEdge("c", "o")
        self.mygraph.setWeight(3.0, "c", "o")
        self.mygraph.addEdge("o", "m")
        self.mygraph.setWeight(1.0, "o", "m")
        self.mygraph.addEdge("m", "e")
        self.mygraph.setWeight(5.0, "m", "e")
        '''
        self.mygraph.addEdge("m", "O")
        self.mygraph.setWeight(0.0, "m", "O")
        self.mygraph.addEdge("O", "s")
        self.mygraph.setWeight(2.0, "O", "s")
        self.mygraph.addEdge("s", "S")
        self.mygraph.setWeight(2.0, "s", "S")
        '''

        bst = BreadthFirstTree().getResult(self.mygraph.getGraph(), "c")
        self.setResult(bst)
    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About Moss graph viewr"),
            self.tr("The <b>Application</b> provide Reader/Editor of graph data structure in GUI mode.<br/>"
                    "This is version 0.2.3 Beta.<br/>"
                    "First version that support Open/Save weighted graph file."))

    #Graph Method
    def addNode(self):
        nodeName, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter node name:')
        if ok:
            self.mygraph.addNode(str(nodeName))
    def addEdge(self):
        source, ok1 = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter source node name:')
        dest, ok2 = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter destination node name:')
        if ok1 and ok2:
            self.mygraph.addEdge(str(source), str(dest))
    def delNode(self):
        nodeName, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter node name:')
        if ok:
            self.mygraph.delNode(str(nodeName)) #case to str because output of Qt is Qt String
    def delEdge(self):
        source, ok1 = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter source node name:')
        dest, ok2 = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter destination node name:')
        if ok1 and ok2:
            self.mygraph.delEdge(str(source), str(dest))
    def setWeight(self):
        source, ok1 = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter source node name:')
        dest, ok2 = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter destination node name:')
        weight, ok3 = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter weight:')
        if ok1 and ok2 and ok3:
            try:
                self.mygraph.setWeight(float(weight),str(source), str(dest))
            except ValueError:
                pass
    def infoGraph(self):
        info  = "<table border=1><tr><th>  Edge  </th>\
                <th>  Weight  </th></tr>"
        allEdge = self.mygraph.getEdges()
        totalEdge = len(allEdge)
        totalNode = len(self.mygraph.getGraph())
        for edge in allEdge:
            info += "<tr>"
            info += "<td align='center'>%s--%s</td>"%(edge[0],edge[1])
            info += "<td align='center'>%d</td>"%(self.mygraph.getGEdge(edge[0],edge[1]).getWeight())
            info += "</tr>"
        info += "<tr><th> Total node:</th><th>%d</th></tr>"%(totalNode)
        info += "<tr><th> Total edge:</th><th>%d</th></tr>"%(totalEdge)
        info += "</table>"
        QtGui.QMessageBox.about(self, self.tr("Graph Info"),
            self.tr(info))
    def animateStatus(self):
        if self.mygraph.getAnimateStatus():
            self.animateMenu.setText(self.tr("&Start animate"))
            self.mygraph.animateChange()
        else:
            self.animateMenu.setText(self.tr("&Stop animate"))
            self.mygraph.animateChange()
    #File Method
    def newGraph(self):
        self.mygraph.clean()
        del self.mygraph
        self.mygraph = DrawWidget()
        self.setCentralWidget(self.mygraph)
    def openFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                    self.file_dir_hist,"XML File (*.xml *.graphML)")
        filenamebuff = str(filename)
        if filename != "":
            self.file_dir_hist = filenamebuff[0:filenamebuff.rfind("/")+1]
            del filenamebuff
            file=open(filename)
            data = file.read()
            file.close()
            self.graphMLAddGraph(data)
    def saveFile(self):
        filename = QtGui.QFileDialog.getSaveFileName(self,
                                                     'Save file',
                                                     self.file_dir_hist,
                                                     'GraphML File(*.graphml *.xml)')
        filenamebuff = str(filename)
        if filename != "":
            self.file_dir_hist = filenamebuff[0:filenamebuff.rfind("/")+1]
            del filenamebuff
            graphML = GraphMLHelpr()
            graphML.saveXML(filename,self.mygraph)
    def graphMLAddGraph(self,inputText):
        inputXML = minidom.parseString(inputText)
        self.mygraph.clean()
        del self.mygraph
        self.mygraph = DrawWidget()
        self.setCentralWidget(self.mygraph)
        nodes = inputXML.getElementsByTagName('node')
        edges = inputXML.getElementsByTagName('edge')
        for node in nodes:
            self.mygraph.addNode(str(node.attributes['id'].value))
        for edge in edges:
            self.mygraph.addEdge(str(edge.attributes['source'].value),str(edge.attributes['target'].value))
            try:
                self.mygraph.setWeight(float(edge.attributes['weight'].value),str(edge.attributes['source'].value),str(edge.attributes['target'].value))
            except KeyError:
                self.mygraph.setWeight(1.0,str(edge.attributes['source'].value),str(edge.attributes['target'].value))
            except ValueError:
                self.mygraph.setWeight(1.0,str(edge.attributes['source'].value),str(edge.attributes['target'].value))
        print self.mygraph.toString()
        self.animateMenu.setText(self.tr("&Stop animate"))
    def highestDegree(self):
        highestList = HighestDegreeNode().getResult(self.mygraph.getGraph())
        self.setResult(highestList)
    def bstTree(self):
        rootNode, ok = QtGui.QInputDialog.getText(self, 'Root node', 'Enter root node name:')
        if ok and rootNode != "":
            bst = BreadthFirstTree().getResult(self.mygraph.getGraph(), str(rootNode))
            self.setResult(bst)
        else:
            QtGui.QMessageBox.information(self,"Invalid input","root node empty")

    def mstTree(self):
        mst,weightDict = PrimMinimumSpanningTree().getResult(self.mygraph)#weighted graph
        self.setResult(mst)
        #display record
        weightResult  = "<table border=1><tr><th>  Node  </th>\
        <th>  Total weight  </th></tr>"
        totalWeight = 0
        resultOrdered = []
        for node in mst:
            resultOrdered.append((weightDict[node],node))
        resultOrdered.sort()
        N = 1 #index of node
        W = 0 #index of weight


        for result in resultOrdered:
            weightResult += "<tr>"
            weightResult += "<td align='center'>%s</td>"%(result[N])
            weightResult += "<td align='center'>%d</td>"%(result[W])
            weightResult += "</tr>"
            totalWeight += result[W]
        weightResult += "<tr><th> Total Weights:</th><th>%d</th></tr>"%(totalWeight)
        weightResult += "</table>"
        QtGui.QMessageBox.about(self, self.tr("Result Info"),
            self.tr(weightResult))
        #print "Weight record", weightDict

    def shtPath(self):
        source, ok = QtGui.QInputDialog.getText(self, 'Source node for shortest path', 'Enter source node name:')
        if ok and source != "":
            #bst = BreadthFirstTree().getResult(self.mygraph.getGraph(), str(rootNode))
            dest, ok = QtGui.QInputDialog.getText(self, 'Destination node for shortest path', 'Enter destination node name:')
            if ok and dest != "":
                sht,weightDict = ShortestPath().getResult(self.mygraph, str(source), str(dest))
                self.setResult(sht)
                #display record
                weightResult  = "<table border=1><tr><th>  Node  </th>\
                <th>  Total weight  </th></tr>"
                totalWeight = 0
                resultOrdered = []
                for node in sht:
                    resultOrdered.append((weightDict[node],node))
                resultOrdered.sort()
                N = 1 #index of node
                W = 0 #index of weight


                for result in resultOrdered:
                    weightResult += "<tr>"
                    weightResult += "<td align='center'>%s</td>"%(result[N])
                    weightResult += "<td align='center'>%d</td>"%(result[W])
                    weightResult += "</tr>"
                    totalWeight += result[W]
                weightResult += "<tr><th> Total Weights:</th><th>%d</th></tr>"%(totalWeight)
                weightResult += "</table>"
                QtGui.QMessageBox.about(self, self.tr("Result Info"),
                    self.tr(weightResult))
            else:
                QtGui.QMessageBox.information(self,"Invalid input","Destination node empty")
        else:
            QtGui.QMessageBox.information(self,"Invalid input","Source node empty")
    def setResult(self,resultGraph):
        #clear old status
        for node in self.mygraph.gNode:
            self.mygraph.gNode[node].paintStatus = MaNode.Unhighlight
        for edge in self.mygraph.gEdge:
            self.mygraph.gEdge[edge].paintStatus = MaEdge.Unhighlight
        #set new status
        for node in resultGraph:
            self.mygraph.gNode[node].paintStatus = MaNode.Highlight
            #paint highlight edge
            for neightbor in resultGraph[node]:
                edge = self.mygraph.getGEdge(node, neightbor)
                edge.paintStatus = MaEdge.Highlight
        #repaint new status
        self.mygraph.hide()
        self.mygraph.show()
    def layoutInfo(self):
        info = LayoutInfo()
        info.getInfo(self.mygraph.gNode)
        pass

#if this is main module do this
if __name__ == "__main__":
    try:
        import psyco
        print "using psyco"
        psyco.full()
    except:
        pass

    #Create Object application need for Qt apps
    app = QtGui.QApplication(sys.argv)
    #Create main window
    mainWin = MainWindow()
    #call method show to show main window
    mainWin.show()
    #clear all when exit
    sys.exit(app.exec_())
