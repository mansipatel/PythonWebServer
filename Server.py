#!/usr/bin/python                                                                                                                                        
from socket import *
import thread, time, sys

hostName=''
serverPort = int(sys.argv[1])

WEB_ROOT = "/var/www/"

def send_response(conn, addr):
        try:
                request=conn.recv(1024) # request received
                log_requests(request, conn) # function call to log the request
                start_time = time.time()
                if len(request) == 0:
                        conn.close()
                        return
                req_arr = request.split()
                verb = req_arr[0] # checking request type
                resource = req_arr[1] # page requested
                if (resource.endswith("/")):
                    resource += "index.htm"
                filename = WEB_ROOT + resource[1:] # appending absolute path
                # checking for directory traversal
                for i in filename.split("/"):
                        if(i.startswith(".")):
                                filename = WEB_ROOT + "mansi.im/index.htm"
                        else:
                                continue
                # generating response
                if verb =='GET':
                        response = "HTTP/1.1 200 OK\r\n\r\n"
                        file = open(filename, 'r')
                        if (filename.split('.')[-1] == "htm"):
                                response += inject_header(start_time)
                        response += file.read()
                        conn.send(response)
                        file.close()
                else:
                        response = "HTTP/1.1 404 Page not found\r\n\r\n"
                        file = open('errorPage.html', 'r')
                        response += file.read()
                        conn.send(response)
                        file.close()
        except IOError:
                response = "HTTP/1.1 404 Page not found\r\n\r\n"
                conn.send(response)
        conn.close()

# This function logs the requested Page, Time, IP and User-Agent in a log file
def log_requests(r, c):
        target = open("pythonWebServerTemp.log", "a")
        req_time =  time.strftime("%d/%b/%Y:%H:%M:%S %z")
        req_split = (r.split("\r\n"))
        req_string = req_split[0]
        user_agent = ""        
        ip_addr = c.getpeername()
        # determining user-agent
        for i in req_split:
                if(i.startswith("User-Agent")):
                        user_agent = i
                        break
        req = "[" + req_time + "] " + req_string + " " + ip_addr[0] + " "  + user_agent + "\n"
        target.write(req)
        target.close
        
# This function prepends an HTML message in every response which specifies micro seconds taken to generate the response
def inject_header(start_time):
        return "<html><div class='container alert alert-warning'>This Website is running on a minimilistic multi-threaded python web server I've built. \
<a>Github code</a>, <a href=""/python-web-server.htm"">blog</a>.<br />Time taken by the server to generate this page:  " + format(((time.time() - start_time)*1000*1000),".2f") + "&micr\
o;s.</div>"


if __name__=='__main__':
        try:
                serverSocket = socket(AF_INET, SOCK_STREAM)#Socket created
                serverSocket.bind((hostName,serverPort)) #Binding the socket
                serverSocket.listen(1)#server listening at the socket
                print 'Socket created'
                print 'Socket bound.'
                print'The server is listening.'
                while(1):
                        conn, addr = serverSocket.accept()
                        #multithreading: for every request that hits the server a new thread spawns
                        thread.start_new_thread(send_response, (conn, addr))
                serverSocket.close()
        except KeyboardInterrupt:
                print '\n ^C received, shutting down the web server'
                serverSocket.close()





