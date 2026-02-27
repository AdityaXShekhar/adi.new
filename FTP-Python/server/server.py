import socket
import os

HOST = "0.0.0.0"
PORT = 5001
BUFFER_SIZE = 1024
FILES_DIR = "../files/"

server = socket.socket()
server.bind((HOST, PORT))
server.listen(5)

print("FTP Server Started...")

def send_file(client, filename):
    path = FILES_DIR + filename
    if not os.path.exists(path):
        client.send("ERROR".encode())
        return
    
    client.send("OK".encode())
    file = open(path, "rb")
    
    while True:
        data = file.read(BUFFER_SIZE)
        if not data:
            break
        client.send(data)
    
    file.close()

def receive_file(client, filename):
    file = open(FILES_DIR + filename, "wb")
    while True:
        data = client.recv(BUFFER_SIZE)
        if not data:
            break
        file.write(data)
    file.close()

def list_files(client):
    files = os.listdir(FILES_DIR)
    file_list = "\n".join(files)
    client.send(file_list.encode())

while True:
    client, addr = server.accept()
    print("Connected:", addr)

    command = client.recv(BUFFER_SIZE).decode()
    parts = command.split()

    if parts[0] == "UPLOAD":
        receive_file(client, parts[1])
        print("Uploaded:", parts[1])

    elif parts[0] == "DOWNLOAD":
        send_file(client, parts[1])
        print("Download request:", parts[1])

    elif parts[0] == "LIST":
        list_files(client)

    client.close()