import socket
import threading

ip = "0.0.0.0"
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((ip, port))
server.listen(5)

print "[*] Listeneing on %s:%d" % (ip, port)

def client_handler(client):
    response = client.recv(1024)
    print "[*] Reveived: %s" % response
    client.send("ACK!")
    client.close()
    
while True:
    client,addr = server.accept()
    print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])
    
    client_thread = threading.Thread(target=client_handler, args=(client,))
    client_thread.start()