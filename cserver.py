import socket
import json
HOST = "10.39.13.91"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.connect((HOST,PORT))



config = {"TID":"CASHSFDSD1231","STATUS":"on"}
server.send(bytes(json.dumps   (config),"utf-8"))
