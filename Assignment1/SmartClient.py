#! /usr/bin/env python
#Used online resource as aid on this assignment some of which are lsited below
#https://www.geeks3d.com/hacklab/20190110/python-3-simple-http-request-with-the-socket-module/
#https://geekflare.com/python-script-http2-test/
#stack overflow
#Francis Orobosa German
#V00893968

import sys
import socket
import ssl

password = ''
substring = "/"
COUNT = 0

def main():
    if len(sys.argv) != 2:
        print("Wrong Input Format")
        return
    b = ''
    result = sys.argv[1]
    if substring in result:
        global COUNT
        COUNT = 1
        path = [(x) for x in result.split('/')]
        host_ip = socket.gethostbyname(path[0])
        print("")
        print('Website: ' + result)
        data = checkHttp2(path[0])
        
        
        
        data2 = port80(result,host_ip)
        

        # connect the client 
        # Establish TCP connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        output = s.connect((path[0] , 80))
        # send some data 
        request = "GET / HTTP/1.1\r\nHost: "+ result+" \r\n\r\n"
        #request = "GET "+result +"/index.html HTTP/1.1\n\n"
        
        s.send(request.encode())  
        
        

        # receive some data 
        response = s.recv(1000) 
        b = response.decode() 
        
        print("")
        print("---Request begin---")
        index = b.find('\n')
        
        date3 = [(x) for x in b.split('\n')]
        count = len(date3)-1
        y = []               # make the list
        for z in date3:          # loop through the list
            y.append(z[:10])
        
        print("GET "+result +"/index.html HTTP/1.1")
        print("host: "+ result)
        
        
        for x in range(count):
            if y[x] == 'Connection':
                print(date3[x])
        print("")
        print("---Request end---")
        print("HTTP request sent, awaiting response...")
        print("")
        print("---Request header---")
        print(data2)
        print("")
        print("---Request body---")
        print(data2)


    else:
        
    
        host_ip = socket.gethostbyname(result)
        print("")
        print('Website: ' + result)
        data = checkHttp2(result)
        
        
        
        data2 = port80(result,host_ip)
        

        # connect the client 
        # Establish TCP connection
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
        output = s.connect((result , 80))
        # send some data 
        request = "GET / HTTP/1.1\r\nHost: "+ result+" \r\n\r\n"
        #request = "GET "+result +"/index.html HTTP/1.1\n\n"
        
        s.send(request.encode())  
        
        

        # receive some data 
        response = s.recv(1000) 
        b = response.decode() 
        
        print("")
        print("---Request begin---")
        index = b.find('\n')
        
        date3 = [(x) for x in b.split('\n')]
        count = len(date3)-1
        y = []               # make the list
        for z in date3:          # loop through the list
            y.append(z[:10])
        
        print("GET "+result +"/index.html HTTP/1.1")
        print("host: "+ result)
        
        
        for x in range(count):
            if y[x] == 'Connection':
                print(date3[x])
        print("")
        print("---Request end---")
        print("HTTP request sent, awaiting response...")
        print("")
        print("---Request header---")
        print(data2)
        print("")
        print("---Request body---")
        print(data2)

    
            
      
    
def checkHttp2(domainName):
    
    if COUNT == 1:
        
        path = [(x) for x in domainName.split('/')]
        HOST = path[0]
        PORT = 443
        ctx = ssl.create_default_context()
        ctx.set_alpn_protocols(['h2', 'spdy/3', 'http/1.1'])
        conn = ctx.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=HOST)
        conn.connect((HOST, PORT))
        pp = conn.selected_alpn_protocol()
        if pp == "h2":
            print ("1. Supports http2: yes")
        else:
            print ("1. Supports http2: no")
        return pp
    else:

        HOST = domainName
        PORT = 443
        ctx = ssl.create_default_context()
        ctx.set_alpn_protocols(['h2', 'spdy/3', 'http/1.1'])
        conn = ctx.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=HOST)
        conn.connect((HOST, PORT))
        pp = conn.selected_alpn_protocol()
        if pp == "h2":
            print ("1. Supports http2: yes")
        else:
            print ("1. Supports http2: no")
        return pp
   

def listCookies(a):
    index = a.find('\n')
    s2 = a[:index]
    s7 = s2[9:12]
    index1 = a.find('Set-Cookie')
    index2 = a.find(';')
    
    date1 = [(x) for x in a.split('\n')]
    count = len(date1)-1
    y = []               # make the list
    for z in date1:          # loop through the list
        y.append(z[:10])
    print("2. List of Cookies:")
    for x in range(count):
        if y[x] == 'Set-Cookie':
            print(date1[x])
            
    

def port443(domainName, host_ip):
    if COUNT == 1:
        
        q = "/"
        path = [(x) for x in domainName.split('/')]
        newPath = q + path[1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = ssl.wrap_socket(sock)  
        
        address = (path[0], 443)  
        sock.connect(address)
        request1 = "GET "+newPath+" HTTP/1.1\r\nHost: "+ path[0] +"\r\n\r\n"
        #request1 = "GET / HTTP/1.1\r\nHost: "+ domainName +"\r\n\r\n"
        #request1 = "GET http://"+domainName +"/index.html HTTP/1.1\n\n"
        sock.send(request1.encode())
        response1 = sock.recv(1000)
        a = response1.decode()
        
        
        date3 = [(x) for x in a.split('\n')]
        
        b =''
        b = date3[0]
        b= b[9:12]
        
        if b == "401":
            password = " yes"
        else:
            password = " no"
        listCookies(a)
        print("Password-protected:" + password)
        return a
    else:

    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock = ssl.wrap_socket(sock)  
        
        address = (host_ip, 443)  
        sock.connect(address)
        request1 = "GET / HTTP/1.1\r\nHost: "+ domainName +"\r\n\r\n"
        #request1 = "GET http://"+domainName +"/index.html HTTP/1.1\n\n"
        sock.send(request1.encode())
        response1 = sock.recv(4000)
        a = response1.decode()
        
        
        date3 = [(x) for x in a.split('\n')]
        
        b =''
        b = date3[0]
        b= b[9:12]
        
        if b == "401":
            password = " yes"
        else:
            password = " no"
        listCookies(a)
        print("Password-protected:" + password)
        return a
    

def port80(domainName,host_ip):
    if COUNT == 1:
        
        q = "/"
        path = [(x) for x in domainName.split('/')]
        newPath = q + path[1]
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (path[0], 80)  
        sock.connect(address)
        request1 = "GET "+newPath+" HTTP/1.1\r\nHost: "+ path[0] +"\r\n\r\n"
        #request1 = "GET http://"+domainName +"/index.html HTTP/1.1\n\n"
        sock.send(request1.encode())
        response1 = sock.recv(4000)
        a = response1.decode()
        date3 = [(x) for x in a.split('\n')]
        b =''
        b = date3[0]
        b= b[9:12]
        if b == "401":
            password = " yes"
        else:
            password = " no"
        
        if b == "301" or "302":
            data2 = port443(domainName,host_ip)
            return data2
        else:
            listCookies(a)
            print("Password-protected:" + password)
            return a
    else:

    
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (host_ip, 80)  
        sock.connect(address)
        request1 = "GET / HTTP/1.1\r\nHost: "+ domainName +"\r\n\r\n"
        #request1 = "GET http://"+domainName +"/index.html HTTP/1.1\n\n"
        sock.send(request1.encode())
        response1 = sock.recv(1000)
        a = response1.decode()
        date3 = [(x) for x in a.split('\n')]
        b =''
        b = date3[0]
        b= b[9:12]
        if b == "401":
            password = " yes"
        else:
            password = " no"
        
        if b == "301" or "302":
            data2 = port443(domainName,host_ip)
            return data2
        else:
            listCookies(a)
            print("Password-protected:" + password)
            return a



if __name__ == "__main__":
    main()