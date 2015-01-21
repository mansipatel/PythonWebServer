# PythonWebServer
This is a multi-threaded web server written in python. I am experimenting by hosting my personal website [mansi.im](http://mansi.im) on it. It is a simple server which `creates a socket`, `binds` and `starts listening` at a port(provided in the input).

In the server code, function **inject_header()** logs all the requests in the following format:

```[Date and Time] [Request sent by the client] [IP address of client] [User-Agent]```

Function **inject_header()** prepends an HTML message in every response which specifies the time taken to generate each response in &micro;s.


