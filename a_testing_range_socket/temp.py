import socket

from _thread import *
# shark bite that listens and accepts to the thread of senko sendall

IPv4 = ""
port = 5555
address = (IPv4, port)
Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    Socket.bind(address)
except socket.error as e:
    print(e)

Socket.listen(2)
print("waiting for clients...")

def client_contact(connection_socket: socket.socket):
    pass

while True:
    connection_socket, address = Socket.accept()
    start_new_thread( client_contact, (connection_socket, ))



