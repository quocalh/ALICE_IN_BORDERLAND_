import time
import pygame as pg
import numpy as np
from pygame.locals import *
import json
import _thread
import threading
import queue
import random

# from components.settings import *
from components.settings import *
from components.networks import Network
from components.UI import *
from components.async_threads import AsyncThreads
from components.animation_and_event import * 
from components.gameplay import *

"""
NOTE for the game

QUESTION: how to deal with new game state and TCP connection?
    just make sure that there is no game state changed in the middle of the send-receive section
        send-receive section means the code between the send command and the receive command
            send(){...}receive()

NOTE the gameloop rule should be ran in the client side, not in the host side

NOTE the host.py json packets should be designed to suit with the demand data of the clients

NOTE I have no idea how this would turn out but the animation event manager should takes place in the host side
    It would activate all the client to do the same thing at once!
        Using Enum, let the  function id be an integer -> send the integer to the client, 
            and have it decoded, turning into a function again!
QUESTION: how can we deal with time, seconds in game,
    creating a class to execute it, return a flag? to execute?

QUESTION: dont know whether if "input" game state and "gameshow" game state should be combined togther
    - uncertain

    
QUESTION: for people who left mid game, we just change the players bool and the game phase according to it

QUESTION: about the internet socket connection (just giving the architecture, not certain about how it will work)
in the server, create a application for the server first through the main thread
i think connecting socket (def ClientServerCommunicatingFunction(connecting socket, Server, ID, ...))
    - OBJECTION: sending info based on the universal dict

"""


"""
UPDATE LOG:
    SETTING UP GAME STATES

UPDATE LOG (26/5/25):
    FIXING THE PLAYER TEXTURE PROBLEM
        I THINK THE PLAYER LOBBY GRAPHIC ATTRIB MUST BE CREATED IN THE PLAYER CREATION 
            - WE WONT ACCOUNT FOR IT POSITION AND WIDTH, AND HEIGHT, BUT TEXTURES AND COLOR
"""

class Player:
    def __init__(self, name: str):
        self.name = name
        self.number: int = -1
        self.vitality: int = 0
    
    def GetNumber(self, number: int):
        assert 0 <= number <= 100, Exception("invalid number input!")
        self.number = number
        return number
        

class Bot(Player):
    Bot_id: int = 1

    def __init__(self):
        self.id = Bot.Bot_id
        name = f"Bot{self.id}"
        super().__init__(name)
        Bot.Bot_id += 1

    def GetNumber(self, phase: int = 5):
        time.sleep(2)
        assert phase < 5 or phase > -1, Exception(f"{self.GetNumber.__name__} assert error!")
        number =  random.randint(0, 100)
        self.number = number
        print(f"[BACKGROUND THREAD]: the bot({self.id}) has chosen the number {self.number}")
        return self.number
    


class ClientApplication:
    def __init__(self, offline: bool = True, client_id = 0, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        self.client_id: int = client_id

        "local data"
        self.running: bool = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()
        pg.init()

        self.time: float = 0
        
        self.WIDTH: int = WIDTH
        self.HEIGHT: int = HEIGHT

        "fonts"
        # self.game_font = pg.font.SysFont("Arial", 25, True) 
        # print(pg.font.get_fonts())
        self.game_font = pg.font.SysFont("newcomputermodern08book", int(min(25 * self.WIDTH / 800, 25 * self.HEIGHT / 800)), False)



        # universal graphic shared among game states                
        self.lobby_color_frame_sequence: list[tuple[int, int, int]] = [(230, 124, 115), (247, 203, 77), (65, 179, 117), (123, 170, 247), (186, 103, 200)]
        self.lobby_pposition_sequence: list[np.ndarray] = [np.array((0.5 + 1/6 * (i - 2), 0.5), dtype = np.float64) for i in range(5)]
        self.lobby_graphic_frame_players: list[GraphicFrame] = []
        for i in range(5): 
            self.lobby_graphic_frame_players.append(GraphicFrame(self.lobby_pposition_sequence[i], 1/8, 1/6, self.lobby_color_frame_sequence[i]))

        "player pool"
        self.players_pool: list[Player] = []
        self.previous_players_pool: list[Player] = [] # "this list gonna refreshed every loop at LobbyRenderPlalyerLobby"

        "the main player"
        self.number_input: int = -1

        "streaming data"
        if not offline:
            "if online"
            self.socket = Network(ipV4, port)        

        self.dt: float = 0
        self.previous_time: float = time.time()

        "state"
        self.state_dict: dict = {}
        self.state_dict["lobby"] = GameStateLobby(self)
        self.state_dict["input"] = GameStateInputPhrase(self)
        self.state_dict["result"] = GameStateResultPhrase(self)
        self.current_state: GameState = self.state_dict["lobby"]

    def Gameloop_run(self):
        while self.running: 
            self.get_dt()
            try:
                game_state: GameState = self.current_state
                game_state.Update(self.dt)
                game_state.Render(self.screen, WIDTH, HEIGHT)
            except Exception as error:
                repr(error)
                raise Exception("killer queen daisan no bakudan baitsa dasto")


    def Gameloop_update(self):
        for event in pg.event.get():
            pass


    def Gameloop_render(self):
        pg.display.flip()
        self.clock.tick(FPS)


    def get_dt(self):
        self.dt = time.time() - self.previous_time
        self.previous_time = time.time()



class GameState:
    def __init__(self, application):
        self.application: ClientApplication = application


    def Update(self, dt: float):
        raise NotImplementedError


    def Render(self, surface: pg.surface.Surface):
        raise NotImplementedError


    def EnterState():
        raise NotImplementedError

    


class GameStateLobby(GameState):
    """
    Just like game application this only being created once, when the game is started. Hence not much consideration in performance
    """

    def __init__(self, application):
        super().__init__(application)   
        self.waiting_for_players_text: GraphicText = GraphicText((0.5, 0.2), self.application.game_font, "Waiting for players...", True, (255, 255, 255), self.application.WIDTH, self.application.HEIGHT)



        self.lobby_graphic_text_player_names: list[GraphicText] = []
        
        

        # obsolete attribs, it is advised not to use it anywhere
        # self.lobby_graphic_frame_bots: list[GraphicFrame] = []
        # for i in range(5): 
        #     self.lobby_graphic_frame_bots.append(GraphicFrame(self.lobby_pposition_sequence[i], 1/8, 1/6, (200, 200, 200)))

        # self.lobby_graphic_text_bot_names: list[GraphicText] = []
        # for i in range(5): self.lobby_graphic_text_bot_names.append(
        #     GraphicText(
        #         (self.lobby_pposition_sequence[i][0], self.lobby_pposition_sequence[i][1] + 1/9), self.application.game_font, f"Bot{i}", True, (255, 255, 255)))
        
        

        # time
        self.local_time: float = 0
        self.original_remaining_time: float = 11 # "think of a number then plus 1 (if the time cooldown is 30 seconds, type 31)"
        self.remaining_time: float = self.original_remaining_time

        self.graphic_text_time: GraphicText = GraphicText((0.5, 0.85), self.application.game_font, str(self.local_time), True, (255, 255, 255), WIDTH, HEIGHT)


    def Update(self, dt: float):
        for event in pg.event.get():
            if event.type == QUIT:
                self.application.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.application.running = False
                if event.key == K_p:
                    self.application.current_state = self.application.state_dict["input"]
                    self.local_time = 0
                    self.remaining_time = self.original_remaining_time
                    
                # stress test the multithread in rendering players
                # if event.key == K_q:
                #     self.previous_players_pool = []
        
                
        self.local_time += dt
        self.remaining_time -= dt

        if self.remaining_time <= 1:
            self.application.current_state = self.application.state_dict["input"]
            self.local_time = 0
            self.remaining_time = self.original_remaining_time            
        


    def Render(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        
        surface.fill((0, 0, 0))
        
        self.graphic_text_time.ChangeMessage(f"time remaining: {int(self.remaining_time)}", WIDTH, HEIGHT)
        self.graphic_text_time.Draw(self.application.screen, WIDTH, HEIGHT)

        self.waiting_for_players_text.Draw(surface, WIDTH, HEIGHT)

        self.LobbyRenderPlayerLobby(surface, WIDTH, HEIGHT)

        pg.display.flip()
        pg.display.set_caption(f"{self.application.clock.get_fps() // 1}")
        self.application.clock.tick(FPS)



    def Thread_UpdateSinglePlayerBannerGraphicText(self, player: Player, i: int): # internal uses only
        self.lobby_graphic_text_player_names.append(GraphicText(
            (self.application.lobby_pposition_sequence[i][0], self.application.lobby_pposition_sequence[i][1] + 1/9), self.application.game_font, player.name, True, (255, 255, 255)))



    def LobbyUpdatePlayerBannerGraphicTexts(self):
        players_pool: list[Player] = self.application.players_pool
        assert len(players_pool) <= 5, Exception("The maximum human clients of this game is 5!")
        if self.application.previous_players_pool != players_pool: # "check if it is the same secquence of players, if it is updated, then change names"
            self.lobby_graphic_text_player_names: list[Player] = []
            # for i in range(len(players_pool)):
            #     player: Player = players_pool[i]
            #     self.lobby_graphic_text_player_names.append(GraphicText(
            #         (self.application.lobby_pposition_sequence[i][0], self.application.lobby_pposition_sequence[i][1] + 1/9), self.application.game_font, player.name, True, (255, 255, 255)))
            # trying out new multithread method (almost no improve in performance whatsoever, but just to try it out)
            for i in range(len(players_pool)):
                player: Player = players_pool[i]
                threads_pool[i%len(threads_pool)].queue.put({"function": self.Thread_UpdateSinglePlayerBannerGraphicText, "args": (player, i)})          
            AsyncThreads.join_custom_all(threads_pool, thread_condition)  



    def LobbyRenderPlayerLobby(self, surface: pg.surface.Surface, WIDTH: int, HEIGHT: int):
        players_pool: list[Player] = self.application.players_pool
        assert len(players_pool) <= 5, Exception("The maximum human clients of this game is 5!")
        # "update player's banners"
        self.LobbyUpdatePlayerBannerGraphicTexts()

        # "drawing the player banners and colors"
        for i in range(len(self.application.players_pool)): 
            # "render the banner"
            self.application.lobby_graphic_frame_players[i].Draw(surface, WIDTH, HEIGHT)
            self.lobby_graphic_text_player_names[i].Draw(surface, WIDTH, HEIGHT)
        self.previous_players_pool = players_pool 



class GameStateInputPhrase(GameState):
    def __init__(self, application):
        """
        draft for the UI nodes
        root node -> node:
            - 1 to 0 numbers
            - back space
            - are u sure button -> node
                {
                    yes button
                    no button
                }

        """
        super().__init__(application)
        self.graphic_drawing_queue: list[Graphic] = []
        self.event_button_pool: list[Buttons] = []

        self.data_input: str = ""
        self.graphic_text_data_input: GraphicText = GraphicText((0.75, 0.2), self.application.game_font, self.data_input, True, (255, 255, 255), WIDTH = self.application.WIDTH, HEIGHT = self.application.HEIGHT)

        self._UI_root_node: UI_Nodes = UI_Nodes()
        self._focused_UI_node: UI_Nodes = self._UI_root_node        

        # list of key pads
        self.graphic_frame_keypad_pad: GraphicFrame = GraphicFrame((0.25, 0.45), 0.4, 0.75, WIDTH = self.application.WIDTH, HEIGHT = self.application.HEIGHT)

        self.pposition_list: list[np.ndarray] = [np.array((0.15 + (i % 3) * 1/3 * 0.3, 
                                                  0.2 + (i // 3) * 1/3 * 0.5), dtype = np.float64) 
                                                  for i in range(12)]
        self.graphic_frame_keypad_list: list[GraphicFrame] = [GraphicFrame(self.pposition_list[i], 0.075, 0.075, color = (255, 255, 255), WIDTH = self.application.WIDTH, HEIGHT = self.application.HEIGHT) 
                                                            for i in range(10)]
        self.button_keypad_list: list[Buttons] = [Buttons(np.array((self.pposition_list[i]), dtype = np.float64), 0.1, 0.1, self.graphic_frame_keypad_list[i]) 
                                                            for i in range(10)]
        self.graphic_text_keypad_list: list[GraphicText] = [GraphicText(self.pposition_list[i], self.application.game_font, str((i+1)%10), True, color = (0, 0, 0), WIDTH = self.application.WIDTH, HEIGHT = self.application.HEIGHT)
                                                            for i in range(10)]
        # make another one for backspace and submit buttons
        self.button_keypad_backspace: Buttons = Buttons(self.pposition_list[10], 0.1, 0.1, GraphicFrame(self.pposition_list[10], 0.075, 0.075, (255, 255, 255), self.application.WIDTH, self.application.HEIGHT))
        self.graphic_text_keypad_backspace: GraphicText = GraphicText(self.pposition_list[10], self.application.game_font, "C", True, (0, 0, 0), self.application.WIDTH, self.application.HEIGHT)

        self.button_keypad_submit: Buttons = Buttons(self.pposition_list[11], 0.1, 0.1, GraphicFrame(self.pposition_list[11], 0.075, 0.075, (255, 255, 255), self.application.WIDTH, self.application.HEIGHT))
        self.graphic_text_keypad_submit: GraphicText = GraphicText(self.pposition_list[11], self.application.game_font, ">", True, (0, 0, 0), self.application.WIDTH, self.application.HEIGHT)

        self._UI_root_node.buttons = self.button_keypad_list
        self._UI_root_node.buttons.append(self.button_keypad_backspace)
        self._UI_root_node.buttons.append(self.button_keypad_submit)

        self.text_graphic_chosing_number = GraphicText((0.5, 0.04), self.application.game_font, "choosing numbers...", True, (255, 255, 255), self.application.WIDTH, self.application.HEIGHT)

        # yes no frame after press submit button
        self._decision_UI_node: UI_Nodes = UI_Nodes(parent = self._UI_root_node)
        self.button_yes: Buttons = Buttons(np.array((0.4375, 0.5), dtype = np.float64), 0.3 / 3, 0.15 / 3, GraphicFrame(np.array((0.4375, 0.5), dtype = np.float64),  0.3 / 3, 0.15 / 3, WIDTH = self.application.WIDTH, HEIGHT = self.application.HEIGHT))
        self.button_no: Buttons = Buttons(np.array((0.5625, 0.5), dtype = np.float64), 0.3 / 3, 0.15 / 3, GraphicFrame(np.array((0.5625, 0.5), dtype = np.float64),  0.3 / 3, 0.15 / 3, WIDTH = self.application.WIDTH, HEIGHT = self.application.HEIGHT))
        self.graphic_text_button_yes: GraphicText = GraphicText((0.4375, 0.5), self.application.game_font, "yes", True, WIDTH = self.application.WIDTH, HEIGHT = self.application.HEIGHT)
        self.graphic_text_button_no: GraphicText = GraphicText((0.5625, 0.5), self.application.game_font, "no", True, WIDTH = self.application.WIDTH, HEIGHT = self.application.HEIGHT)
        self.graphic_text_are_u_sure: GraphicText = GraphicText((0.5, 0.425), self.application.game_font, "are you sure?", True, (0, 0, 0), self.application.WIDTH, self.application.HEIGHT)
        self.graphic_frame_decision_node: GraphicFrame = GraphicFrame((0.5, 0.45), 0.4, 0.2, (255, 255, 255), self.application.WIDTH, self.application.HEIGHT)
        self._decision_UI_node.buttons = [self.button_yes, self.button_no]

        # command log UI
        
        # self.graphic_text_comand_log # HERE HER EHER EHRE RHER EHREHRE HERE HERE HERE HERE
        
        # count down time system
        self.local_time: float = 0
        self.original_remaining_time = 41
        self.remaining_time: float = 41

        self.graphic_text_remaining_time: GraphicText = GraphicText((0.25, 0.85), self.application.game_font, f"remaining time: {int(self.remaining_time)}", True, (255, 255, 255), self.application.WIDTH, self.application.HEIGHT)


    def KeyPadInputValues(self):

        def CheckValidNumber(number: int):
            if number > 100 or  0 > number:
                return False
            return True
            

        branch: list[UI_Nodes] = self._focused_UI_node.TraceBack() # the heart of the ui nodes system

        for node in branch: # activate nodes (the parent nodes those realted to the focused node)
            node.activated = True
        
        
        # Layer 1: root node
        self.event_button_pool = self._focused_UI_node.buttons # really uncertain about whether if it turns out to be good or bad thing | i think it is good!
        

        if self._UI_root_node.activated == True:
            "always has been :skull:"

            # rendering key pads
            self.graphic_drawing_queue.append(self.graphic_frame_keypad_pad)
            for i in range(10):
                self.graphic_drawing_queue.append(self.button_keypad_list[i])
                self.graphic_drawing_queue.append(self.graphic_text_keypad_list[i])
            self.graphic_drawing_queue.append(self.button_keypad_backspace)
            self.graphic_drawing_queue.append(self.button_keypad_submit)
            self.graphic_drawing_queue.append(self.graphic_text_keypad_backspace)
            self.graphic_drawing_queue.append(self.graphic_text_keypad_submit)
            
            # handling events
            if self._focused_UI_node == self._UI_root_node:
                for i in range(len(self.button_keypad_list)):
                    button: Buttons = self.button_keypad_list[i]
                    if button.is_clicked == True:

                        if i == 10: # hit the backspace
                            self.data_input = self.data_input[:-1] if self.data_input != "" else self.data_input

                        elif i == 11: # submited
                            isValid = False if self.data_input == "" else CheckValidNumber(int(self.data_input))
                            if not isValid:
                                print("not a valid number")
                            else:                                
                                self._focused_UI_node = self._UI_root_node.children[0] # keep in mind that  self._UI_root_node.children[0] = self._decision_UI_node
                                

                        else:
                            self.data_input = self.data_input + str((i+1)%10)
                    self.graphic_text_data_input.ChangeMessage("chosen number: " + self.data_input, self.application.WIDTH, self.application.HEIGHT)

            else:
                # Layer 2.0: yes no button (are u sure)

                if self._decision_UI_node.activated == True:
                    # redering yes no buttons and the label
                    self.graphic_drawing_queue.append(self.graphic_frame_decision_node)
                    self.graphic_drawing_queue.append(self.button_no)
                    self.graphic_drawing_queue.append(self.button_yes)
                    self.graphic_drawing_queue.append(self.graphic_text_button_yes)
                    self.graphic_drawing_queue.append(self.graphic_text_are_u_sure)
                    self.graphic_drawing_queue.append(self.graphic_text_button_no)

                    if self._decision_UI_node == self._focused_UI_node:
                        if self.button_yes.is_clicked:
                            self._focused_UI_node = self._UI_root_node
                                # lock the keyboard by
                                    # change state to waiting room state
                            self.application.number_input = int(self.data_input)
                            print(f"[MAIN THREAD]: You have made your choice: {self.application.number_input}")
                            self.application.players_pool[self.application.client_id].number = self.application.number_input # i think it is fucking dumb but i cant figure out the better way
                        if self.button_no.is_clicked:
                            self._focused_UI_node = self._UI_root_node            
                            self.application.number_input = -1
                                        
                    

                
        # deactivate all of the node, preserving the program's reliability 
        # before going out the room, human must turn off their light | otherwise the whole cities while have a daily session of daily electricity cuts 
        # the same thing is going on here, the node must be deactivated after one loop, it only should be switching based on the current focused node. 
        # otherwise, it will not work correctly
        for node in branch: 
            node.activated = False

        # raise "i can do watever i want"
        pass

    
    def ButtonEventChecking(self, MousePosition: np.ndarray):
        for button in self.event_button_pool:
            button.ClickCheck(MousePosition)



    def RenderInputValues(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        self.graphic_text_data_input.Draw(surface, WIDTH, HEIGHT)

    

    def RenderGraphicDrawingQueue(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        for graphic in self.graphic_drawing_queue:
            graphic.Draw(surface, WIDTH, HEIGHT)
        self.graphic_drawing_queue.clear()


    def PlayerGetMove_once(self):
        # offline things, function will only be called in offline mode
        self.PlayerGetMove_once_reserved = self.PlayerGetMove_once # used to revive the funcion if needed
        players_pool: list[Player] = self.application.players_pool

        thread_id = 0 # i have to manuallly assign queue for each thread ;-;
        for i in range(len(players_pool)):
            player = players_pool[i]
            if type(player) == Bot:
                print(f"hello thread {thread_id % len(threads_pool)}")
                # threads_pool[thread_id].queue.put({"function": Your_func, "args": ()})
                threads_pool[thread_id % len(threads_pool)].queue.put({"function": player.GetNumber, "args": ()})
                thread_id += 1
        print()

        self.PlayerGetMove_once = lambda: None # make sure that it will only be called once in the loop

    def ResetPlayerNumber_once(self):
        self.ResetPlayerNumber_once_reserved = self.ResetPlayerNumber_once
        for player in self.application.players_pool:
            player.number = - 1
        self.ResetPlayerNumber_once = lambda: None

    def ReviveOneTimeFunction(self):
        self.ResetPlayerNumber_once = self.ResetPlayerNumber_once_reserved
        self.PlayerGetMove_once = self.PlayerGetMove_once_reserved

    def Update(self, dt: float):

        self.ResetPlayerNumber_once() # this could also be multi-threaded if it causes performance issue.
        self.PlayerGetMove_once()
        
        press_p = False

        for event in pg.event.get():
            if event.type == QUIT:
                self.application.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.application.running = False

                if event.key == K_o:
                    if all([not thread.is_busy for thread in threads_pool]): # if all threads all free, proceed to next stage check
                        self.application.current_state = self.application.state_dict["lobby"]
                        self.ReviveOneTimeFunction()
                        self.local_time = 0
                        self.remaining_time = self.original_remaining_time
                    else:
                        print("the threads have not done their jobs")

                if event.key == K_p:
                    press_p = True
                    
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_LEFT:
                    self.ButtonEventChecking(pg.mouse.get_pos())


        self.local_time += dt
        self.remaining_time -= dt

        if self.remaining_time <= 1 or press_p == True:
            if all([not thread.is_busy for thread in threads_pool]): # if all threads all free, proceed to next stage check 
                            if self.application.players_pool[self.application.client_id] == -1 or self.application.number_input == -1: 
                                print("not yet able to moving onto next stage!")
                            else:
                                self.application.current_state = self.application.state_dict["result"]
                                threads_pool[0].queue.put({"function": self.application.current_state.game_loop.Gameloop, "args": ()})
                                self.ReviveOneTimeFunction()
                                self.local_time = 0
                                self.remaining_time = self.original_remaining_time

                                self.application.number_input = -1
                                self.data_input = ""

            else:
                print("the threads have not done their jobs")
            # raise Exception("Out of time, u took too much time to zink")

        self.KeyPadInputValues()

        for button in self.event_button_pool:
            button.is_clicked = False



    def Render(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        surface.fill((0, 0, 0))

        self.RenderGraphicDrawingQueue(surface, WIDTH, HEIGHT)

        self.text_graphic_chosing_number.Draw(self.application.screen, WIDTH, HEIGHT)
        
        self.graphic_text_remaining_time.ChangeMessage(f"remaining time: {int(self.remaining_time)}", WIDTH, HEIGHT)
        self.graphic_text_remaining_time.Draw(self.application.screen, WIDTH, HEIGHT)

        self.RenderInputValues(surface, WIDTH, HEIGHT)


        pg.display.flip()
        pg.display.set_caption(f"{self.application.clock.get_fps() // 1}")
        self.application.clock.tick(FPS)
    
    









class GameStateResultPhrase(GameState):
    """
    this will be activated when the server sends signal to enter this state
    before this state, all of the players must have chosen their numbers. Violating this rule would result in a crash or an error log in return
    This state makes use a lot of animation stuffs, or just repeated phase in phase out :pensive:
        => before this, make sure that 
            - the bot threads is running good (daemon of course) # DONE
            - the machine has done computing the result (after the bot and player have done choosing a number)
                -> we can perform waiting procedure {visualize waiting icon (loading), create a thread to do compute the result}

        /* not really sure about threading either */ DONE easy as fuck :smirk:

    WE DOING GRAPHIC TOMMOROW ;-; DONE

    HOW CAN I DEAL WITH ANIMATION?
    a queue?
    animation particle that manipulates graphic texture position based on the 0 and 1
    e.g. 
        GraphicClass.run(graphic, t)
            with some additional attributes
        TimeClass(delay)

    queue: list[list[Graphic]] (powerpoint presentation ahh struct)
    {
        [Graphic, Graphic],
        [time],
        [Graphic, Graphic],
        [cut_scene_click_trigger],
        [Graphic, Graphic],
        [time],
        ...
    }

    [[]]
    """
    def __init__(self, application):
        super().__init__(application)
        # graphic
        self.graphic_text_round_over: GraphicText = GraphicText((0.5, 0.1), self.application.game_font, "[ROUND OVER]", True, (255, 255, 255), self.application.WIDTH, self.application.HEIGHT)
        
        # not sure if that is the good practice
        # NOTE: the 0th thread run for ans and the 1st thread crafting for animation tree | while the main thread show loading icon 
        # self explanation                                      | meanwhile, one thread should be running 
        # firstly, [round over] tile fade in                    | (has been ran since the player submit their answers), computing for the winners
        # the banners appear consecutively, players by players  | if had finnished computing for the ans, the responds then be store in the main application, 
        #                                                       | ready to be overwritten in the next round.
        
        self.graphic_text_be_patient: GraphicText = GraphicText((0.5, 0.5), self.application.game_font, "Computing for results...", True)
         

        # later work for the 1st thread
        # self.action_list: TimeLineTree = TimeLineTree(
        #     [TimelineLeaves(CustomAnimation(1000), 2000),
             
        #      ]
        # )
        self.game_loop: GameLoop = GameLoop(self.application.players_pool)

        self.local_dt: float = 0

    def CreateActionList(self):
        self.action_list: TimeLineTree = TimeLineTree(
            [TimelineLeaves(CustomAnimation(1000), 2000), ])
        for player in self.application.players_pool:
            pass
        pass

    def Thread_UpdateSinglePlayerBannerGraphicText(self, player: Player, i: int): # internal uses only
        self.lobby_graphic_text_player_names.append(GraphicText(
            (self.application.lobby_pposition_sequence[i][0], self.application.lobby_pposition_sequence[i][1] + 1/9), self.application.game_font, player.name, True, (255, 255, 255)))
    
    def LobbyUpdatePlayerBannerGraphicTexts(self):
        players_pool: list[Player] = self.application.players_pool
        assert len(players_pool) <= 5, Exception("The maximum human clients of this game is 5!")
        # "check if it is still the same secquence of players | if it is updated, then change names"
        if self.application.previous_players_pool != players_pool: 
            self.lobby_graphic_text_player_names: list[Player] = []
            for i in range(len(players_pool)): 
                player: Player = players_pool[i]
                self.lobby_graphic_text_player_names.append(GraphicText(
                    (self.application.lobby_pposition_sequence[i][0], self.application.lobby_pposition_sequence[i][1] + 1/9), self.application.game_font, player.name, True, (255, 255, 255)))
            # trying out new multithread method (almost no improve in performance whatsoever, but just to try it out)
            # for i in range(len(players_pool)):
            #     player: Player = players_pool[i]
            #     threads_pool[i%len(threads_pool)].queue.put({"function": self.Thread_UpdateSinglePlayerBannerGraphicText, "args": (player, i)})          
            # AsyncThreads.join_custom(threads_pool)  

    def LobbyRenderPlayerLobby(self, surface: pg.surface.Surface, WIDTH: int, HEIGHT: int):
        players_pool: list[Player] = self.application.players_pool
        assert len(players_pool) <= 5, Exception("The maximum human clients of this game is 5!")
        # "update player's banners"
        self.LobbyUpdatePlayerBannerGraphicTexts()

        # "drawing the player banners and colors"
        for i in range(len(self.application.players_pool)): 
            # "render the banner"
            self.application.lobby_graphic_frame_players[i].Draw(surface, WIDTH, HEIGHT)
            self.lobby_graphic_text_player_names[i].Draw(surface, WIDTH, HEIGHT)
        self.previous_players_pool = players_pool 
        

    def CheckIfAllPlayersHaveChosenTheirNumbers_once(self):
        self.CheckIfAllPlayersHaveChosenTheirNumbers_once_reserved = self.CheckIfAllPlayersHaveChosenTheirNumbers_once # this is used to revive it once again
        for player in self.application.players_pool:
            assert player.number != -1, Exception("Somehow, spotted a player whose number is -1 (they have not chosen their number :sob:).")
        self.CheckIfAllPlayersHaveChosenTheirNumbers_once = lambda: None # this func only runs once in the loop
    


    def Update(self, dt: float):
        # self.CheckIfAllPlayersHaveChosenTheirNumbers_once()

        for event in pg.event.get():
            if event.type == QUIT:
                self.application.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.application.running = False
                if event.key == K_o:
                    self.application.current_state = self.application.state_dict["input"]
                
        "ANYWAYS, KEEP THINKING ABOUT ANIMATION PROCEDURES AND HOW CAN SERVER COMMUNICATE WITH THAT INFORMATION"
        # i think the server should not really cares about if the player miss an UI cutscene or a game cutscene or what
        # they just need to give the current state of the cutscene
        # give the result of the cutscene (new items, ...)
        # overall, the server sends life-long flag to the clients - differ by game staate and packet size (differ from state to state)
        # one more thing, animation particle should not die :pensive:


    def Render(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        surface.fill((0, 0, 0))
        
        self.graphic_text_round_over.Draw(surface, WIDTH, HEIGHT)

        self.LobbyRenderPlayerLobby(surface, WIDTH, HEIGHT)

        pg.display.flip()   
        pg.display.set_caption(f"{self.application.clock.get_fps() // 1}")
        self.application.clock.tick(FPS)



if __name__ == "__main__":

    threads_pool: list[AsyncThreads] = []
    thread_condition = threading.Condition()
    for i in range(CLIENT_MAX_CPU_CORE):
        compute_thread = AsyncThreads(queue.Queue(), thread_condition)
        threads_pool.append(compute_thread)
        compute_thread.start()

    game = ClientApplication()
    game.players_pool.append(Player("you"))
    game.players_pool.append(Bot())
    game.players_pool.append(Bot())
    game.players_pool.append(Bot())
    game.players_pool.append(Bot())
    game.Gameloop_run()

pg.quit()
print()
for thread in threads_pool:
    thread.close()
print("Sucessfully terminated all the threads! Closing the program...")
exit()

