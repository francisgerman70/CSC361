A python program for parsing and processing the trace file, and tracking TCP state information. The program should process the trace file and compute summary information about TCPconnections. Note that a TCP connection is identified by a 4-tuple (IP source address, source port,IP destination address, destination port), and packets can flow in both directions on a connection(i.e., duplex). Also note that the packets from different connections can be arbitrarily interleavedwith each other in time, so the program will need to extract packets and associate them with thecorrect connection.

How to use programs:
Step 1: execute python3 traffic.py sample-capture-file.cap
