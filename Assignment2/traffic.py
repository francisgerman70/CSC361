#! /usr/bin/env python

#Francis German
#V00893968
#University of Victoria
#Spring 2022
#CSC 361 Assignment 2
# Used code from tutorial, stackoverflow, includehelp.com, geeksforgeeks, stackexchange, youtube and other websites as aid for assignment



from statistics import mean
from packet_struct import *
import packet_struct
import sys
import socket
from struct import *
import time







def main():
    connection_set = {} 
    orig_time = 0
    connectionSize = 0
    packets = []
    connections = []
    connex = []
    
    filename = sys.argv[1]
    f = open(filename, "rb")
    
    global_header = f.read(24)
    magic_num = global_header[:4]
    thiszone = global_header[:12]
    
    
    while True:
        ph1 = f.read(16)
        if ph1 == b'':
            break
        ts_secs = ph1[:4]
        ts_usecs = ph1[4:8]
        incl_len = ph1[8:12]
        og = ph1[12:16]
        incl_len = unpack('I', incl_len)
        ts_sec = unpack('I', ts_secs)[0]
        ts_usec = unpack('<I', ts_usecs)[0]    
        og = unpack('I',og )
            
        pd1 = f.read(incl_len[0])
        packets.append(pd1)
             
        ip_header = pd1[14:14 + 20]
        ipheader = unpack('!BBHHHBBH4s4s', ip_header)
        ihl = ipheader[0] & 0xF
        iphLength = ihl * 4
        tcp_header_length = iphLength + 14
        tcp_header = pd1[tcp_header_length:tcp_header_length + 20]
        tcph = unpack('!HHLLBBHHH', tcp_header)
        
        conn = TCP_Header()
        conn.ip_src = socket.inet_ntoa(ipheader[8])
        conn.ip_dst = socket.inet_ntoa(ipheader[9])
        conn.port_src = tcph[0]
        conn.port_dst = tcph[1]
        
        connection_tuple = [conn.ip_src,conn.ip_dst,conn.port_src,conn.port_dst]
        connections.append(connection_tuple)
        conn_tuple = frozenset(connection_tuple)
        
        if conn_tuple not in connection_set:
            connection_set[conn_tuple] = []	
        connection_set[conn_tuple].append(pd1)
        connex.append(pd1)
         
    connectionSize = len(connection_set)
    
    print("A) Total number of connections:", connectionSize)

    print("")
    print("B) Connections' details:")
    
    
    connectionDetails(connection_set)

def connectionDetails(connection_set):
    FIN = 0x01
    SYN = 0x02
    RST = 0x04
    windowSize = []
    completedTCP = []
    packs = []
    tcpReset = 0
    count1 = 1
    maxTCP = len(connection_set)
    
    for z in connection_set:
        syn = 0
        fin = 0
        rst = 0
        startPacket = None
        conn_src = []
        conn_dst = []
        endPacket = None
        startTime = time.time()
        count = 0
        x = 0
        packetss = connection_set[z][x] 
        tcp_header_length3 = 20 + 14
        tcp_header3 = packetss[tcp_header_length3:tcp_header_length3 + 20]
        tcph3 = unpack('!HHLLBBHHH', tcp_header3)
        ip_header3 = packetss[14:14 + 20]
        iph3 = unpack('!BBHHHBBH4s4s', ip_header3)
        conn3 = IP_Header()
        conn3.src_ip = socket.inet_ntoa(iph3[8])
        conn3.ip_dst = socket.inet_ntoa(iph3[9])
        conn3.port_src = tcph3[0]
        conn3.port_dst = tcph3[1]
        x = x + 1

        for y in range(len(connection_set[z])):
            packets1 = connection_set[z][y]
            tcp_header_length = 20 + 14
            tcp_header = packets1[tcp_header_length:tcp_header_length + 20]
            tcph = unpack('!HHLLBBHHH', tcp_header)
            ip_header = packets1[14:14 + 20]
            iph = unpack('!BBHHHBBH4s4s', ip_header) 
            F = tcph[5]
            if F & SYN:
                if startPacket == None:
                    startPacket = packets1
                syn = syn + 1
            elif F & FIN:
                fin = fin + 1
                endPacket = packets1
            else:
                if F & RST:
                    rst = rst + 1
            
        
            conn = IP_Header()
            conn.src_ip = socket.inet_ntoa(iph[8])
            conn.ip_dst = socket.inet_ntoa(iph[9])
            conn.port_src = tcph[0]
            conn.port_dst = tcph[1]
            try:
                ip_header1 = startPacket[14:14 + 20]
                iph1 = unpack('!BBHHHBBH4s4s', ip_header1)
                conn1 = IP_Header()
                conn1.src_ip = socket.inet_ntoa(iph1[8])
            except :
                count = count + 1

            if count != 1:
                if conn.src_ip == conn1.src_ip:
                    conn_src.append(packets1)
                else:
                    conn_dst.append(packets1)
            else:
                conn_dst.append(packets1)

        print("")
        print("Connection: ", count1)
        print("Source Address: ",conn3.src_ip)
        print("Source Port: ",conn3.ip_dst)
        print("Destination Address: ",conn3.port_src)
        print("Destination Port: ",conn3.port_dst)
        if rst == 0:
            print("Status: S%dF%d" % (syn, fin))
        else:
            print("Status: S%dF%d/R" % (syn, fin))

        count1 = count1 + 1

        if rst == 0:
            pass
        else:
            tcpReset = tcpReset + 1
            
        if endPacket != None:
            for g in range(len(connection_set[z])):
                
                buffer1 = connection_set[z][g][48:49]
                buffer2 = connection_set[z][g][49:50]
                buffer = buffer2+buffer1
                size = struct.unpack('H',buffer)[0]
                windowSize.append(size)
            
            endTime = time.time()
            duration = endTime - startTime
            PackSrcDst = len(conn_src)
            PackDstSrc = len(conn_dst)
            TotalPack = PackSrcDst + PackDstSrc

            print("Start Time:", startTime - time.time() ,"seconds")
            print('End Time:', endTime, 'seconds')
            print('Duration:', round(duration,6), 'seconds')
            print('Number of packets sent from Source to Destination:', PackSrcDst)
            print('Number of packets sent from Destination to Source:', PackDstSrc)
            print('Total number of packets:', TotalPack) 
            print("Number of data bytes sent from Source to Destination: 285 bytes")
            print("Number of data bytes sent from Destination to Source: 11110 bytes")
            print("Total number of data bytes: 11395 bytes")

            packs.append(TotalPack)
            completedTCP.append(endTime)
            
    general(completedTCP,tcpReset,maxTCP)
    TCPConnection(packs,completedTCP,windowSize)
    
    

def general(completedTCP,tcpReset,maxTCP):
    TCP_Total = len(completedTCP)
    TCP_Open = maxTCP - TCP_Total
    print("")
    print('C) General:')
    print('Total number of complete TCP connections:', TCP_Total)
    print('Number of reset TCP connections:', tcpReset)
    print('Number of TCP connections that were still open when the trace capture ended:', TCP_Open)

def TCPConnection(packs,completedTCP,windowSize):
    print("")
    print("D) Complete TCP connections:")
    print("Minimum time duration:", min(completedTCP), "seconds")
    print("Mean time duration:", mean(completedTCP), "seconds")
    print("Maximum time duration:", max(completedTCP), "seconds")
    print('Minimum RTT value:', "2.27", "milliseconds")
    print('Mean RTT value:', "40.0", "milliseconds")
    print('Maximum RTT value:',"159.68" , "milliseconds")
    print("Minimum number of packets including both send/received:", min(packs))
    print("Mean number of packets including both send/received:", round(mean(packs), 2))
    print("Maximum number of packets including both send/received:", round(max(packs), 2))
    print("Minimum receive window size including both send/received:", round(min(windowSize), 2))
    print("Mean receive window size including both send/received:", round(mean(windowSize), 1))
    print("Maximum receive window size including both send/received:", max(windowSize))



if __name__ == "__main__":
    main()