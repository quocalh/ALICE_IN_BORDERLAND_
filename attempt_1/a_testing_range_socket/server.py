
"""
Create socket
Bind the socket (not optional) - get the error (optional)
Socket match making
while True:
{
    Accept connectiton from clients 
    Create a thread (synchornization)- running in background
        {
            send em pipe bombs (message)
            while True
            {

            }
        }
}
"""


"""
NOTE:
- SUCCESSFULLY RUN ON SERVER (IPV4)| 
- IDK IF IT CAN BUT SEND ID FIRST, MAKE A THREAD CLIENT RUN, RETURN BASED ON ID 
"""
import socket
from _thread import *
import sys

from settings_net import *
from string_manipulation import *

# server = "26.208.177.248"
# port = 5555

class LANServer:
    def __init__(self, ipv4: str = IPv4, port: int = port):
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ipv4 =  ipv4
        self.port = port
        self.address = (ipv4, port)

        self.connection_socket: socket.socket = None
        self.number_of_client: int = 0

        # state
        self.is_binded: bool = False
        self.is_started: bool = True
    
    def Bind(self):
        try:
            self.socket.bind(self.address)
            self.is_binded = True
        except socket.error as error:
            print(error)

    
    def Listen(self, max_connection: int):
        assert type(max_connection) == int, "erm, max_connection needs to be an integer!"
        if not self.is_binded: # if not binded yet
            raise "The server need to be binded with the address (tuple[your IPv4: str, port_ID: int = 5555])"
        print("Waiting for connections, server started!")
        self.socket.listen(max_connection)
        
    def Accept(self):
        self.connection_socket, self.address = self.socket.accept()
        print(f"Connected to: {self.address}")
        self.number_of_client += 1
        return self.connection_socket, self.address

    def Close(self):
        if self.connection_socket == None:
            raise "[Close]: there is nothing to close, literally"
        self.connection_socket.close()
        self.number_of_client -= 1
    
    def SendString(self, string: str):
        assert self.connection_socket != None, "you didnt connect the client to the server"
        self.connection_socket.send(str.encode(string))

    def SendallString(self, string: str):
        assert self.connection_socket != None, "You didnt connect the client to the server"
        self.connection_socket.sendall(str.encode(string))

    def ReceiveEncodedData(self, buffer_size: int = 2048) -> str:
        assert self.connection_socket != None, "you didnt connect the client to the server"
        return self.connection_socket.recv(buffer_size)

    def ClientReceiveID(self):
        print(self.number_of_client)
        self.SendString(str(self.number_of_client - 1))




ClientServerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # think of it like a recuiter, (almost) constantly looking for clients

def thread_contact_client(connection_socket): # we send same data back to the client through this
    connection_socket.send(str.encode("Connected"))
    received_data = "tung buoc anh di"
    while True:
        try:
            receive_decoded_data = connection_socket.recv(2048) 
            if not receive_decoded_data: 
                pass
            else: 
                received_data = receive_decoded_data.decode("utf-8")
                print("<= Received from client: ", received_data)
                print("=> Sending to client: ", received_data, ". NOTE: will be sent next interaction.")
            connection_socket.sendall(str.encode(received_data))

        except:break
    print("Lost connection")
    
    print()
    connection_socket.close()

def server_thread_contact_client(server: LANServer):
    server.SendString("Connected")
    receive_data = ""
    while True:
        try:
            receive_data = server.ReceiveEncodedData()
            receive_data = receive_data.decode("utf-8")
            print(f"=> [SERVER] RECEIVE FROM CLIENT: {receive_data}")
            print(f"<= [SERVER] SEND TO CLIENT:      {receive_data}. NOTE: will be sent next interaction.")
            server.SendallString(receive_data)
        except:
            print(f"Unexpected error, took place in {server_thread_contact_client.__name__}. Otherwise, someone just lost connection.")
            break
    print("Lost connection")
    print()
    server.Close()

temp_player_locket = [(0, 0), (0, 0)]

def player_server_thread_contact(server: LANServer, player_id: int):
    assert -1 < player_id < 2, "Player id for now, only vary from 0 to 1, in integers."
    while True:
        try:
            if player_id == 0: # then send pos player 2, receive pos player 1
                contact_id = 1
                receive_encoded_string_data = server.ReceiveEncodedData()
                print(temp_player_locket)
                temp_player_locket[player_id] = int_the_pos(receive_encoded_string_data.decode("utf-8")) # convert string to arrays
                sending_string_data = string_the_pos(temp_player_locket[contact_id])
            elif player_id == 1: # then send pos player 1, receive pos player 2
                contact_id = 0
                receive_encoded_string_data = server.ReceiveEncodedData()
                temp_player_locket[player_id] = int_the_pos(receive_encoded_string_data.decode("utf-8"))
                sending_string_data = string_the_pos(temp_player_locket[contact_id])
            server.SendallString(sending_string_data)
        except: 
            print(f"Unexpected error, took place in [{server_thread_contact_client.__name__}]. Otherwise, someone just lost connection.")
            break
    print("lost connection")
    print()
    server.Close()


lan_server = LANServer()
lan_server.Bind()
lan_server.Listen(max_connection)

while True:
    connection, address = lan_server.Accept()
    # lan_server.connection_socket.send(str(lan_server.number_of_client).encode())
    # print(f"number of clients: {lan_server.number_of_client}")
    # start_new_thread(lan_server.ClientReceiveID, tuple())
    
    start_new_thread(server_thread_contact_client, (lan_server, ))

    # start_new_thread(player_server_thread_contact, (lan_server, lan_server.number_of_client - 1))



# shock - bind - listen - while true - accept - thread {recv; send; sendall}
# shark bite (that) listens and accepts the threat (of) senda senko