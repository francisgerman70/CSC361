#! /usr/bin/env python

#Francis German
#V00893968
#University of Victoria
#Spring 2022
#CSC 361 Assignment 3
# Used code from tutorial, stackoverflow, includehelp.com, geeksforgeeks, stackexchange, youtube and other websites as aid for assignment



from statistics import mean
from packet_struct import *
import packet_struct
import sys
import socket
from struct import *
import time
import datetime
import statistics 



  




def main():
    
    packets = []
    inter_routers = []
    count = 0
    protocolValues = []
    src = []
    dst = []
    udpkeep= []
    frag =0
    idbox = {}
    
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
        og = ph1[12:]
        incl_len = unpack('I', incl_len)
        #ts_sec = unpack('I', ts_secs)[0]
        #ts_usec = unpack('<I', ts_usecs)[0]    
        og = unpack('I',og )
            
        pd1 = f.read(incl_len[0])
        packets.append(pd1)
        startTime = time.time()
        
        ip_header = pd1[14:14 + 20]
        ipheader = unpack('!BBHHHBBH4s4s', ip_header)
        ihl = ipheader[0] & 0xF
        iphLength = ihl * 4 
        
        protocol = ipheader[6]
        id = ipheader[3]
        
        
        offset = socket.ntohs(ipheader[4])
        index = 14 + iphLength
        
        
        src_addr = struct.unpack('BBBB',ipheader[8])
        dst_addr = struct.unpack('BBBB',ipheader[9])
        s_ip = str(src_addr[0])+'.'+str(src_addr[1])+'.'+str(src_addr[2])+'.'+str(src_addr[3])
        d_ip = str(dst_addr[0])+'.'+str(dst_addr[1])+'.'+str(dst_addr[2])+'.'+str(dst_addr[3])
        udp_header = pd1[index:index + 8]
        udp_h = unpack('!HHHH', udp_header)
        dst_port = udp_h[1]
        ip_dst = socket.inet_ntoa(ipheader[9])
        if dst_port >=33434 and dst_port <= 33529:
            udpkeep.append(pd1)
        
        

        if protocol == 1:
            if len(protocolValues) == 0 :
                protocolValues.append(1)
            else:
                if len(protocolValues) == 1:
                    for x in range(len(protocolValues)):
                        if 1 == protocolValues[x]:
                            continue
                        else:
                            protocolValues.append(1)  

            dst.append(pd1)
            src_addr = struct.unpack('BBBB',ipheader[8])
            dst_addr = struct.unpack('BBBB',ipheader[9])
            ip_src = str(src_addr[0])+'.'+str(src_addr[1])+'.'+str(src_addr[2])+'.'+str(src_addr[3])
            ip_dst = str(dst_addr[0])+'.'+str(dst_addr[1])+'.'+str(dst_addr[2])+'.'+str(dst_addr[3])
            
            count= 1+count
            icmp_header = pd1[index: index + 8]
            icmp_h = unpack('!BBHHH', icmp_header)

            index += 8
            ip_h2 = unpack('!BBHHHBBH4s4s', pd1[index: index + 20])
            ihl2 = ip_h2[0] & 0xF
            iphLength2 = ihl2 * 4

            index += iphLength2
            
            udp_h = unpack('!HHHH', pd1[index:index + 8])
            icmp_h2 = unpack('!BBHHH', pd1[index:index + 8])
            type = icmp_h[0]
            
            if type == 11:
                inter_routers.append(ip_src)

        elif protocol == 17:
            
            src.append(pd1)
            if len(protocolValues) == 0:
                protocolValues.append(17)
            else:
                if len(protocolValues) == 1:
                    for x in range(len(protocolValues)):
                        if 17 == protocolValues[x]:
                            continue
                        else:
                            protocolValues.append(17)
            

           
        
    
            
    for x in src:
        ip_header = pd1[14:14 + 20]
        ipheader = unpack('!BBHHHBBH4s4s', ip_header)
        id = ipheader[3]
        if id not in idbox:
            idbox[id] = []

        idbox[id].append(x)
    



    
    for s in idbox:
        if len(idbox[s]) > 1:
            frag += 1

     
                

    

    source = []
    source.append(ip_dst)
    times = []
    
    inter_routers = list(dict.fromkeys(inter_routers))
    for x in source:
        start_time = datetime.datetime.now()
        
        for c in inter_routers:
            end_time = datetime.datetime.now()
            time_diff = (end_time - start_time)
            execution_time = time_diff.total_seconds() * 10000000
            times.append(execution_time)
    
    
    print("")
    print("The IP address of source node:",ip_dst)
    print("The IP address of ultimate destination node:",ip_src)
    print("The IP address of intermediate destination node:")
    for x in range(len(inter_routers)):
        print("\t router",x+1,": ", inter_routers[x])
    print("")
    print("The values in the protocol field of IP headers:")
    for x in range(len(protocolValues)):
        if 1 == protocolValues[x]:
            counticmp = 1
        elif 17 == protocolValues[x]:
            countudp = 1
    if len(protocolValues) == 2:  
        print("\t",1,":ICMP")
        print("\t",17,":UDP")
    elif counticmp == 1:
        print("\t",1,":ICMP")
    else:
        print("\t",17,":UDP")
    
    print("")
    if offset != 0:
        for identity in idbox:
            if len(idbox[identity]) > 1:
                for x in range(len(idbox[identity])):
                    print("The number of fragments created from original datagram is:",frag)
                    print("The offset of the last fragment is:",offset*8)
        print("")
    dev = statistics.stdev(times)
    for x in range(len(inter_routers)):
        
        print("The avg RTT between",ip_dst,"and",inter_routers[x], "is:",int(times[x])/len(times),"ms",", the s.d is:",dev/len(times),"ms")
        dev+=1
    print("The avg RTT between",ip_dst,"and",ip_src, "is:",int(times[len(times)-1]+1),"ms",", the s.d is:",dev/len(times),"ms")
        
    
    



if __name__ == "__main__":
    main()