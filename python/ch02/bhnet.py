# encoding: UTF-8

import logging
import sys
import socket
import getopt
import threading
import subprocess

listen = False
command = False
execute = ""
target = ""
upload = ""
port = 0

def usage():
    print "BHP Net Tool"
    print
    print "Usage: bhpnet.py -t target_host -p port"
    print "-l --listen"
    print "-e --execute=file_to_run"
    print "-c --command shell"
    print "-u --uoload=destination"
    print
    print
    print "Examples: "
    print ""
    sys.exit(0)
    
def main():
    global listen
    global command
    global execute
    global target
    global upload
    global port
    
    if not len(sys.argv[1:]):
        usage()
    
    try:
        opts,args = getopt.getopt(sys.argv[1:], "h:l:e:t:p:c:u:",
                                   ["help", "listen", "execute", "target", "port", "command", "upload"])
    except getopt.GetoptError as err:
        print str(err), "\n"
        usage()
        
    for o,a in opts:
        print o,a
        if o in ("-h", "--help"):
            usage()
        elif o in ("-l", "--listen"):
            listen = True
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p", "--port"):
            port = int(a)        
        elif o in ("-e", "--execute"):
            execute = a
        elif o in ("-c", "--command"):
            command = True
        elif o in ("-u", "--upload"):
            upload = a
        else:
            assert False, "Unhandled Option"
            
    print "listen=%s, target=%s, port=%s, execute=%s, command=%s, upload=%s" % (listen, target, port, execute, command, upload)
      
    if listen:
        server_loop()
    elif len(target) and port > 0:
        print "client_sender\n"
        buffer = sys.stdin.read()
        client_sender(buffer)
            
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        client.connect((target,port))
        print "[*] Connecting to %s:%d" % (target,port)
        
        buffer_len = len(buffer)
        print "buffer=%s, len(buffer)=%d\n" % (buffer,buffer_len)
        
        if buffer_len:
            print "Connected first send:%s" % buffer
            client.send(buffer)
        
        while True:
            recv_len = 1
            response = ""
            
            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response += data
                
                if recv_len < 4096:
                    #print "break response=%s" % response
                    break
                
            #print response
            
            buffer = raw_input(response)
            buffer += "\n"
            buffer_len = len(buffer)
            #print "buffer=%s, len(buffer)=%d\n" % (buffer,buffer_len)            
            client.send(buffer)
            
    except Exception as e:
        print "\n[*] Exception! Exiting."
        logging.exception(e)
    
    print "[*] Client close!"
    client.close()
    
def server_loop():
    global target
    
    if not len(target):
        target = "0.0.0.0"
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    
    server.listen(5)
    print "[*] Listeneing on %s:%d" % (target,port)
    
    while True:
        client,addr = server.accept()
        print "[*] Accepted connection from: %s:%d" % (addr[0], addr[1])
        client_thread = threading.Thread(target=client_handler, args=(client,))
        client_thread.start()
        
def client_handler(client):
    global command
    global upload
    global execute
    
    if len(upload):
        file_buffer = ""
        while True:
            data = client.recv(1024)
            if not data:
                break
            
            file_buffer += data
        
        try:
            file_desc = open(upload, "wb")
            file_desc.write(file_buffer)
            file_desc.close()
            
            client.send("Successfully saved file to %s\n" % upload)
        except:
            client.send("Failed to saved file to %s\n" % upload)
            
    if len(execute):
        output = run_command(execute)
        client.send(output)
        
    if command:
        #提示客户端输入命令
        prompt = "<BHP:#>"
        client.send(prompt)        
        while True:
            #等待客户端输入命令，直到发现换行符
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client.recv(1024)
                
            #cmd_buffer_len = len(cmd_buffer)
            #print "1 cmd_buffer=%s, len(cmd_buffer)=%s\n" % (cmd_buffer,cmd_buffer_len)
            #cmd_buffer = cmd_buffer.strip()
            #cmd_buffer_len = len(cmd_buffer)
            #print "2 cmd_buffer=%s, len(cmd_buffer)=%s\n" % (cmd_buffer,cmd_buffer_len)
            response = run_command(cmd_buffer)
            print response
            
            client.send(response+"\n"+prompt)
        
def run_command(command):
    #换行
    command = command.rstrip()
    
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    except:
        output = "Failed to execute command:%s\n" % command
        
    return output

main()