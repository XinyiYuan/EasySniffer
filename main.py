import os, sys, time
from queue import Queue
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem as QTItem
from scapy.all import *
from scapy.all import IP
from scapy.arch.common import compile_filter

from pages import mainpage

MAXSIZE = 1024

class Signal(QtCore.QObject):
    recv = QtCore.pyqtSignal(str)

class MainPage(QMainWindow):
    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)

        self.ui = mainpage.Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.startButton.clicked.connect(self.startSniff)
        self.ui.startButton.setEnabled(True)

        self.ui.stopButton.clicked.connect(self.stopSniff)
        self.ui.stopButton.setEnabled(False)

        self.ui.resetButton.clicked.connect(self.clearList)
        self.ui.resetButton.setEnabled(False)

        self.ui.filterText.editingFinished.connect(self.getFilter)
        self.ui.filterText.setEnabled(True)

        self.showPacketSig = Signal()
        self.showPacketSig.recv.connect(self.showPacket)

        self.sniffer = None
        self.queue = Queue()


    def getIface(self):
        iface = get_working_ifaces()[0]
        return iface

    def getFilter(self):
        filter = self.ui.filterText.text().strip()
        if not filter:
            self.ui.filterText.setStyleSheet('')
            self.ui.startButton.setEnabled(True)
            return

        try:
            compile_filter(filter_exp=filter)
            # 输入框背景变绿
            self.ui.filterText.setStyleSheet('QLineEdit { background-color: rgb(33, 186, 69);}')
            self.ui.startButton.setEnabled(True)
        except Exception:
            # 将输入框背景变红
            self.ui.startButton.setEnabled(False)
            self.ui.filterText.setStyleSheet('QLineEdit { background-color: rgb(219, 40, 40);}')
            return
    def showPacket(self):
        packet = self.queue.get(False)
        if not packet:
            return

        if self.ui.packetList.rowCount() >= MAXSIZE:
            self.ui.packetList.removeRow(0)

        row = self.ui.packetList.rowCount()
        self.ui.packetList.insertRow(row)

        # source & destination
        if IP in packet:
            src = packet[IP].src
            dst = packet[IP].dst
        else:
            src = packet.src
            dst = packet.dst

        self.ui.packetList.setItem(row, 0, QTItem(src))
        self.ui.packetList.setItem(row, 1, QTItem(dst))

        # protocol
        layer = None
        for var in self.getPacketLayers(packet):
            if not isinstance(var, (Padding, Raw)):
                layer = var

        protocol = layer.name
        self.ui.packetList.setItem(row, 2, QTItem(str(protocol)))

        # length
        length = f"{len(packet)}"
        self.ui.packetList.setItem(row, 3, QTItem(length))

        # info
        info = str(packet.summary())
        item = QTItem(info)
        item.packet = packet
        self.ui.packetList.setItem(row, 4, item)

    def getPacketLayers(self, packet):
        count = 0
        while True:
            layer = packet.getlayer(count)
            if layer is None:
                break
            yield layer
            count += 1
    def handelPacket(self, packet):  # p捕获到的数据包
        # packet.show()
        self.queue.put(packet)
        self.showPacketSig.recv.emit('show packet list')

    def startSniff(self):
        print('start sniff')
        # iface = self.getIface()
        # filter = self.ui.filterText.text()
        self.sniffer = AsyncSniffer(filter=None, prn=self.handelPacket, count=0)
        self.sniffer.start()

        self.ui.filterText.setEnabled(False)
        self.ui.startButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)
        self.ui.resetButton.setEnabled(False)

    def stopSniff(self):
        print('stop sniff')
        if self.sniffer:
            self.sniffer.stop()
            self.sniffer = None
            self.ui.filterText.setEnabled(True)
            self.ui.startButton.setEnabled(True)
            self.ui.stopButton.setEnabled(False)
            self.ui.resetButton.setEnabled(True)
        else:
            print('already stop')

    def clearList(self):
        print('clear all')
        self.ui.resetButton.setEnabled(False)
        self.ui.packetList.clear()
        self.ui.packetList.setRowCount(0)
        self.ui.packetInfo.clear()

def main():
    app = QApplication(sys.argv)
    myMainPage = MainPage()
    myMainPage.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()