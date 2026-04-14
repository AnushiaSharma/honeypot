import socket
from logger import log_attack

HOST = "0.0.0.0"
PORT = 2222 #safe port (no admin needed)

def start_honeypot():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[+] SSH Honeypot running on port {PORT}")

    while True:
        client, addr = server.accept()
        print(f"[!] Connection from {addr}")

        log_attack(f"Connection from {addr}")

        client.send(b"Fake SSH Server\nLogin: ")
        username = client.recv(1024).decode().strip()

        client.send(b"Password: ")
        password = client.recv(1024).decode().strip()

        log_attack(f"Login attempt → {username}:{password}")

        print(f"[LOGGED] {username}:{password}")

        client.close()

        
       
       
         
    
       