import socket
import os
from threading import Thread
import threading

clients = set()
clients_lock = threading.Lock()


def check_user(ip):
    global name
    name = "Inconnu "
    file_ips = open("ip_list.txt", mode = 'r')
    lines = file_ips.readlines()
    for line in lines :
        r_ip, r_name = line.split(',')
        if r_ip == ip:
            name = r_name
    
    
def listener(client, address):
    print("Accepted connection from: ", address)
    with clients_lock:
        clients.add(client)
        info = "  Nouvelle connexion :"+str(address)
        message_complet = "Serveur "+"#-#"+str(info)+"1"
        message_complet_encodé = message_complet.encode()
        for c in clients:
            c.sendall(message_complet_encodé)
            
    try:    
        while True:
            message_content = client.recv(1024)
            print(socket.socket.getpeername(client))
            l = len(socket.socket.getpeername(client))
            author = str(socket.socket.getpeername(client))
            print(author)
            ip = author[:-9]
            print(f"ip1 = {ip}")
            ip = ip[2:]
            print(f"ip2 = {ip}")
            check_user(ip = ip)
            message_content.decode()
            print(message_content)
            user_data = str(name)+str("#-#")+str(message_content)
            user_data = user_data.encode()
            if not message_content:
                break
            else:
                print(repr(user_data))
                with clients_lock:
                    for c in clients:
                        c.sendall(user_data)
    finally:
        with clients_lock:
            clients.remove(client)
            client.close()
            
host = socket.gethostname()
port = 8236

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((host,port))
s.listen(3)
th = []

while True:
    print ("Server is listening for connections...")
    client, address = s.accept()
    th.append(Thread(target=listener, args = (client,address)).start())

s.close()
