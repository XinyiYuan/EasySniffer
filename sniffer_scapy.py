#!/usr/bin/python3# -*- coding: UTF-8 -*-from scapy.all import *import timedef getProtocol(packet):    # packet.show()    proto_list = ['TCP', 'UDP', 'ICMP', 'IPv6', 'IP', 'ARP', 'Ether', 'Unknown']    protocol = []    for proto in proto_list:        if proto in packet:            protocol.append(proto)    return protocoldef get_packet_layers(packet):    print('a')    packet.show()    '''    print('get packet layers')    counter = 0    while True:        layer = packet.getlayer(counter)        print(counter)        print(layer)        if layer is None:            break        yield layer        counter += 1    '''def getAllLayers(packet, counter):    layer = packet.getlayer(counter)    return layerdef main():    sniffer = AsyncSniffer(prn=get_packet_layers, count=1)    sniffer.start()if __name__ == '__main__':    main()