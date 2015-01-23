#!/usr/bin/python
from socket import *

hostName=''
serverPort = 8081

def send_response(conn, addr):
        request=conn.recv(1024)
        if len(request) == 0:
        	exit(0)
        #capturing the response and splitting the array to determine the type of request
        req_arr = request.split()
        verb = req_arr[0]
        resource = req_arr[1]
        filename = resource[1:]		#checking the file requested by the client
        #checking the type of request to generate the appropriate response
        if verb =='GET':		
                try:
                        response = "HTTP/1.1 200 OK\r\n\r\n"
                        file = open(filename, 'r')
                        response += file.read()
                        conn.send(response)                                          
                        file.close()
                except IOError:
                        response = "HTTP/1.1 404 Page not found\r\n\r\n"
                        file = open('errorPage.html', 'r')
                        response += file.read()
                        conn.send(response)
                        file.close()
                conn.close()

if __name__=='__main__':
        try:
                serverSocket = socket(AF_INET, SOCK_STREAM)#Socket created
                serverSocket.bind((hostName, serverPort)) #Binding the socket
                serverSocket.listen(1)#server listening at the socket
                print 'Socket created'
                print 'Socket bound.'
                print'The server is listening.'
                while(1):
                        conn, addr = serverSocket.accept()
                        send_response(conn, addr)  
                serverSocket.close()
        except KeyboardInterrupt:
                print ' received, shutting down the web server'
                serverSocket.close()
	

