#!/usr/bin/python

from PyQt4 import QtGui,QtCore
import sys
import qdacc_ui
import numpy as np
import pylab
import time
import socket
import struct
import pyqtgraph

class QRobotControlCenterApp(QtGui.QMainWindow, qdacc_ui.Ui_MainWindow):
    def __init__(self, parent=None):
        #pyqtgraph.setConfigOption('background', 'w') #before loading widget
        super(QRobotControlCenterApp, self).__init__(parent)
        self.setupUi(self)
        self.connectBtn.clicked.connect(self.connect)
        self.updateBtn.clicked.connect(self.updateParameters)
        self.plot_ul.plotItem.showGrid(True, True, 0.7)
        self.connected = False

    def updateParameters(self):
        print("Updating Parameters")
        self.sock.send("Hello")
        #self.sock.recv()
        #TODO Set Values

    def handleConnectBtn(self):
        if(self.connected):
            disconnect()
        else:
            connect()

    def connect(self):
        print(self.hostAddressEdit.text())
        host = self.hostAddressEdit.text()
        port = int(self.portEdit.text())
        self.sock = socket.socket()
        self.sock.connect((host, port))
        self.connected = True
        self.connectBtn.setText("Disconnect")

    def disconnect(self):
        self.sock.close()
        self.connected = False;
        self.connectBtn.setText("Connect")

    def update(self):
        t1=time.clock()
        points=100 #number of data points
        X=np.arange(points)
        Y=np.sin(np.arange(points)/points*3*np.pi+time.time())
        C=pyqtgraph.hsvColor(time.time()/5%1,alpha=.5)
        pen=pyqtgraph.mkPen(color=C,width=2)
        self.plot_ul.plot(X,Y,pen=pen,clear=True)
        print("update took %.02f ms"%((time.clock()-t1)*1000))
	#QtCore.QTimer.singleShot(1, self.update)

if __name__=="__main__":
    app = QtGui.QApplication(sys.argv)
    form = QRobotControlCenterApp()
    form.show()
    form.update() #start with something
    app.exec_()
    print("DONE")
