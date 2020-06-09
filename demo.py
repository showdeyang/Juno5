# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.12
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Juno(object):
    def setupUi(self, Juno):
        Juno.setObjectName("Juno")
        Juno.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(Juno)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(80, 50, 54, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(100, 120, 281, 311))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("assets/res/mmexport1586532194360.webp"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        Juno.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Juno)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        Juno.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(Juno)
        self.statusbar.setObjectName("statusbar")
        Juno.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(Juno)
        QtCore.QMetaObject.connectSlotsByName(Juno)

    def retranslateUi(self, Juno):
        _translate = QtCore.QCoreApplication.translate
        Juno.setWindowTitle(_translate("Juno", "MainWindow"))
        self.label.setText(_translate("Juno", "Welcome!"))
        self.menuFile.setTitle(_translate("Juno", "File"))
        self.menuEdit.setTitle(_translate("Juno", "Edit"))
        self.menuHelp.setTitle(_translate("Juno", "Help"))


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    window = Ui_Juno()
    window.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
