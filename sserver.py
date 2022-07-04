import socket

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)


server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen(5)
while True:
    print("[LISTENING]")
    client,addr = server.accept()
    print(f"[CONNECTION] {addr[0]}:{addr[1]}")

    config = client.recv(1024)
    config = config.decode("utf-8")
    print(f"[MESSAGE] {config}")
    client.close()