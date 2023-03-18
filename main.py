import os, sys, time
# from logger import logger
from queue import Queue
from PyQt5.QtWidgets import QApplication, QMainWindow
from scapy.all import *
from scapy.arch.common import compile_filter

from pages import mainpage

class MainPage(QMainWindow):
    def __init__(self, parent=None):
        super(MainPage, self).__init__(parent)
        self.ui = mainpage.Ui_MainWindow()
        self.ui.setupUi(self)
        self.queue = Queue()

    def getIface(self):
        iface = get_working_ifaces()[0]
        return iface

    def getFilter(self):
        filter = self.ui.filterEdit.text().strip()
        if not filter:
            self.ui.filterEdit.setStyleSheet('')
            self.ui.startButton.setEnabled(True)
            return

        try:
            compile_filter(filter_exp=filter)
            # 输入框背景变绿
            self.ui.filterEdit.setStyleSheet('QLineEdit { background-color: rgb(33, 186, 69);}')
            self.ui.startButton.setEnabled(True)
        except Exception:
            # 将输入框背景变红
            self.ui.startButton.setEnabled(False)
            self.ui.filterEdit.setStyleSheet('QLineEdit { background-color: rgb(219, 40, 40);}')
            return

    def handelPacket(self, packet):  # p捕获到的数据包
        # packet.show()

        self.queue.put(packet)
        # self.signal.recv.emit()

        if packet.haslayer('TCP'):
            print('TCP Packet!')
            '''
            print(packet['TCP'].sport)
            print(packet['TCP'].dport)
            print(packet['TCP'].seq)
            print(packet['TCP'].dataofs)
            '''
        if packet.haslayer('UDP'):
            print('UDP Packet!')

        if packet.haslayer('IP'):
            print('IP Packet!')

        if packet.haslayer('HTTP'):
            print('HTTP Packet!')

        if packet.haslayer('ARP'):
            print('ARP Packet!')
            '''
            print(packet['ARP'].psrc)
            print(packet['ARP'].pdst)
            print(packet['ARP'].hwsrc)
            print(packet['ARP'].hwdst)
            '''

    def startSniff(self):
        print('start sniff')
        # iface = self.getIface()
        # filter = self.ui.filterEdit.text()
        self.sniffer = AsyncSniffer(filter=None, prn=self.handelPacket, count=10)
        self.sniffer.start()

def main():
    app = QApplication(sys.argv)
    myMainPage = MainPage()
    myMainPage.show()
    myMainPage.startSniff()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()