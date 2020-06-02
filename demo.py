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
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(66, 50, 481, 451))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.label_2 = QtWidgets.QLabel(self.tab)
        self.label_2.setGeometry(QtCore.QRect(70, 80, 281, 311))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("assets/res/mmexport1586532194360.webp"))
        self.label_2.setScaledContents(True)
        self.label_2.setObjectName("label_2")
        self.label = QtWidgets.QLabel(self.tab)
        self.label.setGeometry(QtCore.QRect(100, 30, 271, 20))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea.setGeometry(QtCore.QRect(60, 50, 341, 331))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 339, 329))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.tabWidget.addTab(self.tab_2, "")
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
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Juno)

    def retranslateUi(self, Juno):
        _translate = QtCore.QCoreApplication.translate
        Juno.setWindowTitle(_translate("Juno", "MainWindow"))
        self.label.setText(_translate("Juno", "Welcome!"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Juno", "Tab 1"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Juno", "Tab 2"))
        self.menuFile.setTitle(_translate("Juno", "File"))
        self.menuEdit.setTitle(_translate("Juno", "Edit"))
        self.menuHelp.setTitle(_translate("Juno", "Help"))

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    MainWindow = Ui_Juno()
    MainWindow.setupUi(window)
    window.show()
    sys.exit(app.exec_())