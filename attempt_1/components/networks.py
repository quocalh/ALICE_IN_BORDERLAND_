import socket

class Network:
    def __init__(self, host_ipv4: str, host_port: int, blocking_nature: bool = False):
        self.address: tuple[str, int] = (host_ipv4, host_port)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.Connect()
        self.blocking_nature: bool = blocking_nature
        self.socket.setblocking(self.blocking_nature)
    
    def Connect(self):
        try:
            self.socket.connect(self.address)
        except Exception as error:
            print(repr(error))
            raise Exception("problem spotted in Network, took place in Network.Connect()!")
        
if __name__ == "__main__":
    network = Network("192.168.1.3", 5555)
    print(network.socket.recv(2048).decode()); "stater-pack"
    while True:
        response = input("say something to the server: ")
        network.socket.send(str(response).encode())
        data = network.socket.recv(2048).decode()
        print(f"we just got: \"{data}\"")
        

            