import sys
from PyQt4 import QtCore, QtGui
from xml.dom import minidom
#from elasticnodes import GraphWidget
#from MyGraph import MyGraph
from TestDrawWidget import DrawWidget
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.createActions()
        self.createMenus()
        self.resize(500,500)
        #test addWidget area
        QtCore.qsrand(QtCore.QTime(0,0,0).secsTo(QtCore.QTime.currentTime()))
        #self.graph = GraphWidget()
        self.mygraph = DrawWidget()
        self.mygraph.addEdge("A", "B")
        self.mygraph.addEdge("G","B")
        self.mygraph.addEdge("C","D")
        self.mygraph.addEdge("C","B")
        self.mygraph.addEdge("D","A")
        self.mygraph.addEdge("D","G")
        self.mygraph.addEdge("A","C")
        self.mygraph.addEdge("A","G")
        self.mygraph.addEdge("G","A")
        self.mygraph.addEdge("G","A")
        self.mygraph.addEdge("G","A")
        #print type(self.mygraph)
        #print type(self.graph)
        #nodes = ['A','B','C','D','E','F','G']
        #for node in nodes:
        #    self.graph.addNode(node)
        #for i in range(len(nodes)):
        #    if i < len(nodes)-1:
        #        self.graph.addEdge(nodes[i],nodes[i+1])
        #    else:
        #        self.graph.addEdge(nodes[0],nodes[6])
        #self.graph.addEdge('A','E')
        #self.graph.addEdge('A','D')

        #print type(self.graph)

        #self.gwidget = GraphWidget()

        #set icon of the application
        self.setWindowIcon(QtGui.QIcon('../images/app_icon.png'))
        #set title of the application
        self.setCentralWidget(self.mygraph)
        self.setWindowTitle('Moss Graph Viewr Qt')
        self.setCenterScreen()
        self.statusBar().showMessage('Not ready')

    def createActions(self):
        self.openFileMenu = QtGui.QAction(self.tr("&Open file"),self)
        self.openFileMenu.setShortcut('Ctrl+O')
        self.setStatusTip('Open GraphXml File')
        self.connect(self.openFileMenu,QtCore.SIGNAL('triggered()'),self.openFile)

        self.exitMenu = QtGui.QAction(QtGui.QIcon('../images/close.png'),self.tr("&Exit"), self)
        self.exitMenu.setShortcut('Ctrl+Q')
        self.exitMenu.setStatusTip('Exit application')
        self.connect(self.exitMenu,QtCore.SIGNAL('triggered()'),
                     QtGui.qApp,QtCore.SLOT('quit()'))

        self.addNodeMenu = QtGui.QAction(self.tr("&Add New Node"),self)
        self.addNodeMenu.setShortcut('Ctrl+N')
        self.connect(self.addNodeMenu,QtCore.SIGNAL("triggered()"),self.addNode)

        self.addEdgeMenu = QtGui.QAction(self.tr("&Add New Edge"),self)
        self.addEdgeMenu.setShortcut('Ctrl+E')
        self.connect(self.addEdgeMenu,QtCore.SIGNAL("triggered()"),self.addEdge)

        self.aboutActMenu = QtGui.QAction(self.tr("&About"), self)
        self.aboutActMenu.setStatusTip(self.tr("Show the application's About box"))
        self.connect(self.aboutActMenu, QtCore.SIGNAL("triggered()"), self.about)

        self.aboutQtActMenu = QtGui.QAction(self.tr("About &Qt"), self)
        self.aboutQtActMenu.setStatusTip(self.tr("Show the Qt library's About box"))
        self.connect(self.aboutQtActMenu, QtCore.SIGNAL("triggered()"), QtGui.qApp, QtCore.SLOT("aboutQt()"))

    def createMenus(self):
        self.filemenu = self.menuBar().addMenu(self.tr("&File"))
        self.filemenu.addAction(self.openFileMenu)
        self.filemenu.addAction(self.exitMenu)


        self.graphmenu = self.menuBar().addMenu(self.tr("&Graph"))
        self.graphmenu.addAction(self.addNodeMenu)
        self.graphmenu.addAction(self.addEdgeMenu)

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

    def about(self):
        QtGui.QMessageBox.about(self, self.tr("About Application"),
            self.tr("The <b>Application</b> example demonstrates how to "
                    "write modern GUI applications using Qt, with a menu bar, "
                    "toolbars, and a status bar."))
    def addNode(self):
        nodeName, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter node name:')
        if ok:
            self.mygraph.addNode(str(nodeName))
    def addEdge(self):
        source, ok1 = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter source node name:')
        dest, ok2 = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Enter destination node name:')
        if ok1 and ok2:
            self.mygraph.addEdge(str(source), str(dest))
    def openFile(self):
        filename = QtGui.QFileDialog.getOpenFileName(self, 'Open file',
                    '.',"XML File (*.xml *.graphML)")
        if filename != "":
            file=open(filename)
            data = file.read()
            file.close()
            self.graphML(data)
    def saveFile(self):
        pass
    def graphML(self,inputText):
        inputXML = minidom.parseString(inputText)
        nodes = inputXML.getElementsByTagName('node')
        edges = inputXML.getElementsByTagName('edge')
        for node in nodes:
            self.mygraph.addNode(str(node.attributes['id'].value))
        for edge in edges:
            self.mygraph.addEdge(str(edge.attributes['source'].value),str(edge.attributes['target'].value))

'''Dummy function for test create graph'''
#if this is main module do this
if __name__ == "__main__":
    #Create Object application need for Qt apps
    app = QtGui.QApplication(sys.argv)
    #Create main window
    mainWin = MainWindow()
    #call method show to show main window
    mainWin.show()
    #clear all when exit
    sys.exit(app.exec_())