# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainpage.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 681)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(21, 10, 1201, 51))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filterText = QtWidgets.QLineEdit(self.widget)
        self.filterText.setObjectName("filterText")
        self.horizontalLayout.addWidget(self.filterText)
        self.startButton = QtWidgets.QPushButton(self.widget)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)
        self.stopButton = QtWidgets.QPushButton(self.widget)
        self.stopButton.setObjectName("stopButton")
        self.horizontalLayout.addWidget(self.stopButton)
        self.resetButton = QtWidgets.QPushButton(self.widget)
        self.resetButton.setObjectName("resetButton")
        self.horizontalLayout.addWidget(self.resetButton)
        self.widget1 = QtWidgets.QWidget(self.centralwidget)
        self.widget1.setGeometry(QtCore.QRect(11, 71, 1211, 531))
        self.widget1.setObjectName("widget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.packetList = QtWidgets.QTableWidget(self.widget1)
        self.packetList.setObjectName("packetList")
        self.packetList.setColumnCount(5)
        self.packetList.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.packetList.setHorizontalHeaderItem(0, item)
        self.packetList.setColumnWidth(0, 150)
        item = QtWidgets.QTableWidgetItem()
        self.packetList.setHorizontalHeaderItem(1, item)
        self.packetList.setColumnWidth(1, 150)
        item = QtWidgets.QTableWidgetItem()
        self.packetList.setHorizontalHeaderItem(2, item)
        self.packetList.setColumnWidth(2, 150)
        item = QtWidgets.QTableWidgetItem()
        self.packetList.setHorizontalHeaderItem(3, item)
        self.packetList.setColumnWidth(3, 80)
        item = QtWidgets.QTableWidgetItem()
        self.packetList.setHorizontalHeaderItem(4, item)
        self.packetList.setColumnWidth(4, 600)
        self.verticalLayout.addWidget(self.packetList)
        self.packetInfo = QtWidgets.QListWidget(self.widget1)
        self.packetInfo.setObjectName("packetInfo")
        item = QtWidgets.QListWidgetItem()
        self.packetInfo.addItem(item)
        self.verticalLayout.addWidget(self.packetInfo)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 24))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "SimpleSniffer"))
        self.filterText.setText(_translate("MainWindow", "filter:"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.stopButton.setText(_translate("MainWindow", "Stop"))
        self.resetButton.setText(_translate("MainWindow", "Reset"))
        item = self.packetList.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "源结点"))
        item = self.packetList.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "目标结点"))
        item = self.packetList.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "协议"))
        item = self.packetList.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "长度"))
        item = self.packetList.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "内容"))
        __sortingEnabled = self.packetInfo.isSortingEnabled()
        self.packetInfo.setSortingEnabled(False)
        item = self.packetInfo.item(0)
        item.setText(_translate("MainWindow", "内容"))
        self.packetInfo.setSortingEnabled(__sortingEnabled)
