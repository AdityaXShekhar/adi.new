import socket

HOST = "127.0.0.1"
PORT = 5001
BUFFER_SIZE = 1024

def upload(client, filename):
    client.send(f"UPLOAD {filename}".encode())
    file = open(filename, "rb")
    while True:
        data = file.read(BUFFER_SIZE)
        if not data:
            break
        client.send(data)
    file.close()
    print("Uploaded!")

def download(client, filename):
    client.send(f"DOWNLOAD {filename}".encode())
    response = client.recv(BUFFER_SIZE).decode()

    if response == "ERROR":
        print("File not found on server")
        return

    file = open("downloaded_" + filename, "wb")
    while True:
        data = client.recv(BUFFER_SIZE)
        if not data:
            break
        file.write(data)
    file.close()
    print("Downloaded!")

def list_files(client):
    client.send("LIST".encode())
    data = client.recv(BUFFER_SIZE).decode()
    print("\nServer Files:\n", data)

while True:
    print("\n1 Upload\n2 Download\n3 List\n4 Exit")
    choice = input("Enter choice: ")

    if choice == "4":
        break

    client = socket.socket()
    client.connect((HOST, PORT))

    if choice == "1":
        filename = input("Enter file name: ")
        upload(client, filename)

    elif choice == "2":
        filename = input("Enter file name: ")
        download(client, filename)

    elif choice == "3":
        list_files(client)

    client.close()
