import socket

def create_server(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    s.listen()
    return s

def accept_connection(server_socket):
    conn, addr = server_socket.accept()
    return conn, addr

def create_client(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s

def send_data(socket, data):
    socket.sendall(data.encode())

def receive_data(socket, buffer_size=1024):
    data = socket.recv(buffer_size)
    return data.decode()
