# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sample.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        MainWindow.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionProcess = QtWidgets.QAction(MainWindow)
        self.actionProcess.setObjectName("actionProcess")
        self.actionFeatures = QtWidgets.QAction(MainWindow)
        self.actionFeatures.setObjectName("actionFeatures")
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.actionTreatments = QtWidgets.QAction(MainWindow)
        self.actionTreatments.setObjectName("actionTreatments")
        self.menuEdit.addAction(self.actionTreatments)
        self.menuEdit.addAction(self.actionFeatures)
        self.menuEdit.addSeparator()
        self.menuEdit.addAction(self.actionExit)
        self.menuAbout.addAction(self.actionAbout)
        self.menuAbout.addAction(self.actionHelp)
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.actionExit.triggered['bool'].connect(MainWindow.close)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuEdit.setTitle(_translate("MainWindow", "设置"))
        self.menuAbout.setTitle(_translate("MainWindow", "关于"))
        self.actionProcess.setText(_translate("MainWindow", "编辑"))
        self.actionFeatures.setText(_translate("MainWindow", "指标集"))
        self.actionExit.setText(_translate("MainWindow", "退出"))
        self.actionAbout.setText(_translate("MainWindow", "Juno简介"))
        self.actionHelp.setText(_translate("MainWindow", "帮助"))
        self.actionTreatments.setText(_translate("MainWindow", "工艺集"))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow() #this may not be TabWidget, it depends.
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
