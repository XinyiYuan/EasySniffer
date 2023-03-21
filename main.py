import os, sys, time
from queue import Queue
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem as QTItem
from PyQt5.QtWidgets import QTreeWidgetItem as QRItem
from scapy.all import *
from scapy.arch.common import compile_filter
from scapy.utils import hexdump

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
        self.ui.filterText.setPlaceholderText('Filter')

        self.showPacketSig = Signal()
        self.showPacketSig.recv.connect(self.showPacket)

        self.ui.packetList.setColumnWidth(0, 150)
        self.ui.packetList.setColumnWidth(1, 150)
        self.ui.packetList.setColumnWidth(2, 100)
        self.ui.packetList.setColumnWidth(3, 80)
        self.ui.packetList.setColumnWidth(4, 600)
        # select a cell in packetList
        # then display the content of each layer
        # in packetOverview (treeWidget)
        # similar to packet.show()
        self.ui.packetList.cellClicked.connect(self.loadOverview)

        # select an item in packetOverview
        # then display the original hexadecimal content of the selected layer
        # in packetContent (QTextEdit)
        self.ui.packetOverview.itemClicked.connect(self.loadContent)

        self.ui.packetContent.setPlaceholderText("Packet Content")

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
            if self.queue:
                self.queue.queue.clear()
                self.queue = Queue()

            self.ui.filterText.setStyleSheet('QLineEdit { background-color: rgb(33, 186, 69);}')
            self.ui.startButton.setEnabled(True)
            self.ui.resetButton.setEnabled(False)

            # clear all
            if self.queue:
                self.queue.queue.clear()
                self.queue = Queue()
            self.ui.packetList.setRowCount(0)
            self.ui.packetList.clearContents()
            # Notice that clear() clears ALL information in the table,
            # INCLUDING header of the table
            # clearContents() only clears contents of the table

            self.ui.packetOverview.clear()
            self.ui.packetContent.clear()
        except Exception:
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

        # protocol
        protocol = self.getProtocol(packet)
        self.ui.packetList.setItem(row, 2, QTItem(str(protocol)))

        # source & destination
        if protocol == 'ARP' or protocol == 'Ether':
            src = packet.src
            dst = packet.dst
        else:
            if 'IPv6' in packet:
                src = packet['IPv6'].src
                dst = packet['IPv6'].dst
            elif 'IP' in packet:
                src = packet['IP'].src
                dst = packet['IP'].dst
            else:
                src = packet.src
                dst = packet.dst
        self.ui.packetList.setItem(row, 0, QTItem(src))
        self.ui.packetList.setItem(row, 1, QTItem(dst))

        # length
        length = f"{len(packet)}"
        self.ui.packetList.setItem(row, 3, QTItem(length))

        # info
        info = str(packet.summary())
        item = QTItem(info)
        item.packet = packet
        self.ui.packetList.setItem(row, 4, item)

    def getProtocol(self, packet):
        # packet.show()
        proto_list = ['TCP', 'UDP', 'ICMP', 'IPv6', 'IP', 'ARP', 'Ether', 'Unknown']
        for proto in proto_list:
            if proto in packet:
                protocol = proto
                return protocol

    def getAllLayers(self, packet):
        counter = 0
        while True:
            layer = packet.getlayer(counter)
            if layer is None:
                break
            yield layer
            counter += 1

    def handelPacket(self, packet):
        # packet.show()
        self.queue.put(packet)
        self.showPacketSig.recv.emit('show packet list')

    def loadContent(self, item, column):
        # print('packetOverview.itemClicked')
        if not hasattr(item, 'layer'):
            return
        layer = item.layer
        self.ui.packetContent.setText(hexdump(layer, dump=True))

    def loadOverview(self, x, y):
        # print('packetList.itemClicked')
        # print(x, y)
        item = self.ui.packetList.item(x, 4)
        if not hasattr(item, 'packet'):
            return
        packet = item.packet
        # packet.show()
        self.ui.packetContent.setText(hexdump(packet, dump=True))

        self.ui.packetOverview.clear()
        for layer in self.getAllLayers(packet):
            item = QRItem(self.ui.packetOverview)
            item.layer = layer
            item.setText(0, layer.name)
            # self.ui.packetOverview.addTopLevelItem(item)

            for name, value in layer.fields.items():
                child = QRItem(item)
                child.setText(0, f"{name}: {value}")

        # self.ui.packetOverview.expandAll()
    def startSniff(self):
        print('start sniff')
        # iface = self.getIface()
        filter = self.ui.filterText.text()
        print('filter:', str(filter))
        self.sniffer = AsyncSniffer(filter=filter, prn=self.handelPacket, count=0)
        self.sniffer.start()

        self.ui.filterText.setEnabled(False)
        self.ui.startButton.setEnabled(False)
        self.ui.stopButton.setEnabled(True)
        self.ui.resetButton.setEnabled(False)

    def stopSniff(self):
        print('stop sniff')
        if self.sniffer:
            # self.sniffer.stop()
            self.sniffer = None
            self.ui.filterText.setEnabled(True)
            self.ui.startButton.setEnabled(True)
            self.ui.stopButton.setEnabled(False)
            self.ui.resetButton.setEnabled(True)
        else:
            print('already stop')

    def clearList(self):
        print('clear all')

        if self.queue:
            self.queue.queue.clear()
            self.queue = Queue()

        self.ui.resetButton.setEnabled(False)
        self.ui.packetList.setRowCount(0)

def main():
    app = QApplication(sys.argv)
    myMainPage = MainPage()
    myMainPage.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()