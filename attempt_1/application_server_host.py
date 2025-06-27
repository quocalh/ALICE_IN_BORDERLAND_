import json
import _thread
import socket

from components.host import TCPServer
from components.settings import *

"""
ABOUT SERVER DATABASE:
the server database will be divided based on the number of game states

in the gameplay:
    disconnected players will be replaced by bots

about starter packet, player sends:
    - name
    - id
    - color
    - avatar
    
"""

sever_database = {
    "lobby_packet": {
        "players": {}, # soon be filled with bots

    },
    "gameplay_packet":{
        "player": {}, # bot are handled by the server

    },

}

"""
NOTE:
    everything, every resource that need to be in synced, MUST be here, in this file.

this process must involve some kind of multithread in multithread
although it jobs is sending data,
    it has to process some information in the background
        hence, i think multithread or async is needed
"""

class Host:
    def __init__(self):
        self.state_dict: dict = {}
        self.current_state
        self.sever_running = True

        self.socket = TCPServer(ipV4, port)
    
    def ThreadClientServerCommunication(self):
        pass

    def ThreadGameStateManager(self):
        pass

    def Mainloop_run(self):
        self.socket.Bind()
        self.socket.Listen()

        while self.sever_running:
            connection_socket, address = self.socket.socket.accept()




"""
tcp_server = TCPServer(ipV4, port)

tcp_server.Bind()
tcp_server.Listen()

def ThreadClientServerLobby():
    pass

while True:
    connection_socket, address = tcp_server.socket.accept()
    print(f"{address} joined the server")

    #...
    _thread.start_new_thread(ThreadClientServerLobby, ())
"""
    



