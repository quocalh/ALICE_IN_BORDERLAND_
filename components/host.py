import socket
import _thread
import json

from settings import *

class TCPServer:
    """
    UDP protocol fits this project better, but i want to get familier with TCP, i can change it to UDP later on if needed
    """
    def __init__(self, ipv4: str, port: int):
        self.address: tuple[str, int] = (ipv4, port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Bind(self):
        try:
            self.socket.bind(self.address)
        except Exception as error:
            print(repr(error))
            raise Exception("Socket problems, took place at Bind() function.")

    def Listen(self, overwrite_number_of_clients: int = MAX_CLIENT):
        try:
            max_number_of_clients: int = overwrite_number_of_clients if overwrite_number_of_clients else 2

            self.socket.listen(max_number_of_clients)
        except Exception as error:
            print(repr(error))
            raise Exception("Socket problems, took place at Listen() function.")
            
    
    

# server = Server("string", 5555)



if __name__ == "__main__":
    ID_counter: int = 0
    def MessageTextingSample(connection_socket: socket.socket, address: tuple[str, int], client_id: int):
        "send em the starter-pack"
        connection_socket.send("hello my nigga".encode())
        while True:
            try:
                data = connection_socket.recv(2048)
                data = data.decode()
                
                print(f"data received: {data}")
                reply: str = "the server sends you this data"
                connection_socket.sendall(str(reply).encode())
                print(f"you just send you with: \"{data}\"")
            except Exception as error:
                "in case there are any error occurs"
                print(repr(error))
                break
        
        print(f"{address}: Disconnected")
        connection_socket.close()
        return
        

    server = TCPServer("192.168.1.3", 5555)

    server.Bind()
    server.Listen()
    print("server created")

    while True:
        connection_socket, address = server.socket.accept()
        _thread.start_new_thread(MessageTextingSample, (connection_socket, address, ID_counter))
        ID_counter += 1

    