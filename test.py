from scapy.all import *


def CallBack(packet):
    print(packet.show())

    if packet.haslayer('TCP'):
        print(packet['TCP'].sport)
        print(packet['TCP'].dport)
        print(packet['TCP'].seq)
        print(packet['TCP'].dataofs)


filter = "tcp"

sniff(filter=filter, prn=CallBack, count=0)