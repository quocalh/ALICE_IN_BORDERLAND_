import socket
from _thread import *
import time

from settings_net import *

class Network:
    def __init__(self, ipv4: str = IPv4, port: int = port):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = ipv4
        self.port = port
        self.address = (self.server, self.port)
        self.data_receive = self.ConnectToServer()
            
    def ConnectToServer(self):
        try:
            self.socket.connect(self.address)
        except:
            print("If you see this message, we cannot find the server. Otherwise, you suck, hope you know that 🥰")
    
    def Send(self, data):
        try:
            self.socket.send(str.encode(data))
        except socket.error as error:
            print(error)
            
    def Receive(self):
        try:
            return self.socket.recv(2048).decode()
        except:
            print("unexpected problems")

    def Send_n_Receive(self, data: str):
        try:
            self.socket.send(str(data).encode()) # send
        except socket.error as socket_error:
            print(socket_error)
        except:
            print(f"[{type(self)}]: unexpected problem!")
        return self.socket.recv(2048).decode() # receive

if __name__ == "__main__":
    network = Network()

    reponse = network.Receive()
    start_new_thread(network.Send, ("nigger",)) 
    reponse = network.Receive()
    print(f"Response from server: {reponse}")
    
    while True:
        msg = input("=> Type message to send: ")
        if msg.lower() == "exit":
            break
        
        response = network.Send(msg)
        response = network.Receive()

        print("<= Response from server:", response)