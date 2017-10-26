import socket
import threading

ip = "0.0.0.0"
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(5)

print "[*] Listeneing on %s:%d" % (ip, port)

def handle_client(client_socket):
    response = client_socket.recv(1024)
    print "[*] Reveived: %s" % response
    client_socket.send("ACK!")
    client_socket.close()
    
while True:
    client,addr = server.accept()
    print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])
    
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()