import sys
from PyQt4 import QtCore, QtGui
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        QtGui.QMainWindow.__init__(self)
        self.createActions()
        self.createMenus()
        self.resize(250,250)
        #set icon of the application
        self.setWindowIcon(QtGui.QIcon('../images/app_icon.png'))
        #set title of the application
        self.setWindowTitle('Hello Qt')
        self.setCenterScreen()
        self.statusBar().showMessage('Not ready')
    def createActions(self):
        self.exit = QtGui.QAction(QtGui.QIcon('../images/close.png'),self.tr("&Exit"), self)
        self.exit.setShortcut('Ctrl+Q')
        self.exit.setStatusTip('Exit application')
        self.connect(self.exit,QtCore.SIGNAL('triggered()'),
                     QtGui.qApp,QtCore.SLOT('quit()'))

        self.aboutAct = QtGui.QAction(self.tr("&About"), self)
        self.aboutAct.setStatusTip(self.tr("Show the application's About box"))
        self.connect(self.aboutAct, QtCore.SIGNAL("triggered()"), self.about)

        self.aboutQtAct = QtGui.QAction(self.tr("About &Qt"), self)
        self.aboutQtAct.setStatusTip(self.tr("Show the Qt library's About box"))
        self.connect(self.aboutQtAct, QtCore.SIGNAL("triggered()"), QtGui.qApp, QtCore.SLOT("aboutQt()"))

    def createMenus(self):
        self.filemenu = self.menuBar().addMenu(self.tr("&File"))
        self.filemenu.addAction(self.exit)
        self.helpMenu = self.menuBar().addMenu(self.tr("&Help"))
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

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