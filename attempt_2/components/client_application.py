import pygame as pg
from pygame.locals import *

import time
import queue
import random

from components.settings import *
from components.UI import *
from components.async_threads import *
from components.gameplay import *
from components.animations import *


class Player:
    def __init__(self, name: str):
        self.name: str = name
        self.number: int = -1
        self.vitality: int = 0

    
class Bot(Player):
    id_couter: int = 0
    def __init__(self, name: str = None):
        if name:
            name = name
        else:
            name = "bot" + str(Bot.id_couter)
            Bot.id_couter += 1
        super().__init__(name)
        
    
    def get_number(self, phase: int = 5):
        print("calculating best number")
        self.number = random.randint(0, 100)
        time.sleep(1)
        print(f"The bot {self.name}  has chosen {self.number}")


class ClientApplication:
    def __init__(self, client_id: int, offline: bool, threads_pool: list[AsyncThread] = [], WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        self.client_id: int = client_id
        self.offline: bool = offline
        self.threads_pool: list[AsyncThread] = threads_pool
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.running = True
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        self.clock = pg.time.Clock()

        self.players_pool: list[Player] = []
        
        pg.init()
        self.game_font: pg.font.Font = pg.font.Font(r"attempt_2\assets\font\NewCM08-Book.otf", int(min(25 * self.WIDTH / 800, 25 * self.HEIGHT / 800)))
        
        self.lobby_player_themecolor_sequence: list[tuple[int, int, int]] =  [(230, 124, 115), (247, 203, 77), (65, 179, 117), (123, 170, 247), (186, 103, 200)]
        self.lobby_pposition_sequence: list[np.ndarray] = [(0.5 + 1/6 * (i - 2), 0.5) for i in range(5)]

        self.graphic_frame__lobby_player_banners: list[GraphicFrame] = [GraphicFrame(
            self.lobby_pposition_sequence[i], 
            1/8, 
            1/6, 
            self.lobby_player_themecolor_sequence[i], 
            self.WIDTH, 
            self.HEIGHT) 
            for i in range(5)]
        
        self.graphic_text__lobby_player_names: list[GraphicText] = [GraphicText(
            self.lobby_pposition_sequence[i], 
            self.game_font, 
            f"{self.players_pool[i]}", 
            True, 
            self.lobby_player_themecolor_sequence[len(self.players_pool)], 
            self.WIDTH, 
            self.HEIGHT) 
            for i in range(len(self.players_pool))]
        
        self.data_input: int = -1

        # streamming  datad
        # abandon offline, online mode, since i scrapped the idea away

        self.dt: float = 0
        self.previous_time: float = time.time()

        # state
        self.state_dict: dict = {}
        self.state_dict["lobby"] = GameStateLobby(self)
        self.state_dict["input"] = GameStateInput(self)
        self.state_dict["result"] = 0

        self.current_state = self.state_dict["lobby"]
    
    def Run(self):
        self.previous_time = time.time()
        while self.running:
            self.dt = time.time() - self.previous_time
            self.previous_time = time.time()
            try:
                game_state: GameState = self.current_state
                game_state.Update(self.dt)
                game_state.Render(self.screen)
            
            except Exception as error:
                self.running = False
                print(error)
                print("[NOTE]: the problem took place somewhere in the client code.")
                raise(Exception("Bug"))





class GameState:
    def __init__(self, application):
        self.application: ClientApplication = application

    def Update(self, dt: float):
        raise Exception(NotImplemented)
    
    def Render(self, surface: pg.surface.Surface):
        raise Exception(NotImplemented)
    
    def EnterState(self):
        raise Exception(NotImplemented)
    




class GameStateLobby(GameState):

    def __init__(self, application: ClientApplication):
        super().__init__(application)
    
        self.graphic_text__waiting_for_player: GraphicText = GraphicText((0.5, 0.2), 
                                                                         self.application.game_font, 
                                                                         "waiting for players...", 
                                                                         True, 
                                                                         (255, 255, 255), 
                                                                         self.application.WIDTH, 
                                                                         self.application.HEIGHT)
        self.local_time: float = 0
        self.graphic_text__time: GraphicText = GraphicText((0.5, 0.85), 
                                                           self.application.game_font, 
                                                           str(self.local_time), 
                                                           True, 
                                                           (255, 255, 255), 
                                                           self.application.WIDTH, 
                                                           self.application.HEIGHT)
        self.remaining_time: float = 11
        self.initial_set_remaining_time: float = 11


    def Update(self, dt: float):
        def EnterInputState(self):
            self.application.current_state = self.application.state_dict["input"]
            self.local_time = 0
            self.remaining_time = self.initial_set_remaining_time

        def Thread__update_a_player_banner(player: Player, index: int):
            # self.application.graphic_frame__lobby_player_banners[index]
            self.graphic_frame__lobby_player_banners= [GraphicFrame(
                self.lobby_pposition_sequence[i], 
                1/8, 
                1/6, 
                self.lobby_player_themecolor_sequence[i], 
                self.WIDTH, 
                self.HEIGHT) 
                for i in range(5)]
        
        def Thread__update_a_player_name(player: Player, index: int):
            self.graphic_text__lobby_player_names = [GraphicText(
                self.lobby_pposition_sequence[i], 
                self.game_font, 
                f"{self.players_pool[i]}", 
                True, 
                self.lobby_player_themecolor_sequence[len(self.players_pool)], 
                self.WIDTH, 
                self.HEIGHT) 
                for i in range(len(self.players_pool))]

        for event in pg.event.get():
            if event.type == QUIT:
                self.application.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.application.running = False
                if event.key == K_p:
                    EnterInputState(self)             
        
        self.local_time += dt
        self.remaining_time -= dt

        self.graphic_text__time.ChangeMessage(f"{int(self.remaining_time)}")

        self.application.graphic_frame__lobby_player_banners= [GraphicFrame(
            self.application.lobby_pposition_sequence[i], 
            1/8, 
            1/6, 
            self.application.lobby_player_themecolor_sequence[i], 
            self.application.WIDTH, 
            self.application.HEIGHT) for i in range(len(self.application.players_pool))]
        
        self.application.graphic_text__lobby_player_names = [GraphicText(
            (self.application.lobby_pposition_sequence[i][0], self.application.lobby_pposition_sequence[i][1] + 1/10), 
            self.application.game_font, 
            f"{self.application.players_pool[i].name}", 
            True, 
            (255, 255, 255), 
            self.application.WIDTH, 
            self.application.HEIGHT) for i in range(len(self.application.players_pool))]

        if self.remaining_time <= 1:
            EnterInputState(self)
    
    def LobbyRenderPlayerLobby(self, surface: pg.surface.Surface):
        for i in range(len(self.application.players_pool)):
            self.application.graphic_frame__lobby_player_banners[i].Draw(surface, self.application.WIDTH, self.application.HEIGHT)
            self.application.graphic_text__lobby_player_names[i].Draw(surface)

    def Render(self, surface: pg.surface.Surface):
        surface.fill((0, 0, 0))

        self.graphic_text__time.ChangeMessage(f"time remaining: {int(self.remaining_time)}")
        self.graphic_text__time.Draw(surface)

        self.graphic_text__waiting_for_player.Draw(surface)
        
        self.LobbyRenderPlayerLobby(surface)

        pg.display.flip()
        pg.display.set_caption(f"{self.application.clock.get_fps() // 1}")
        self.application.clock.tick(FPS)





class GameStateInput(GameState):
    """
    the UI node structure (straight-forward - literally)

        numpad_node (0) (root node)
            |
        yes_no_node (1)

    """
    def __init__(self, application: ClientApplication):
        self.application: ClientApplication = application

        self.graphical_drawing_queue: list[Graphic] = []
        self.active_buttons_pool: list[Button] = []

        self.input_field: str = ""
        self.graphic_text__data_input: GraphicText = GraphicText((0.75, 0.2), 
                                                                    self.application.game_font, 
                                                                    self.input_field, 
                                                                    True, 
                                                                    (255, 255, 255), 
                                                                    self.application.WIDTH, 
                                                                    self.application.HEIGHT)
        

        self.position_list: list[tuple] = [
            (0.15 + (i%3) * 1/3 * 0.3, 
             0.2 + (i//3) * 1/3 * 0.5) 
            for i in range(12)]
        
        self.graphic_frame__pad: GraphicFrame = GraphicFrame(
            (0.25, 0.45), 
            0.4, 
            0.75, 
            (55, 182, 255), 
            self.application.WIDTH, 
            self.application.HEIGHT)
        self.key_pad_icon: list[str] = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "C", ">"]
        self.graphic_frame__keypads: list[GraphicFrame] = [GraphicFrame(
            (self.position_list[i]), 
            0.075, 
            0.075, 
            (255, 255, 255), 
            self.application.WIDTH, 
            self.application.HEIGHT) for i in range(12)]
        self.button__keypads: list[Button] = [Button(
            (self.position_list[i]), 
            0.075, 
            0.075, 
            self.graphic_frame__keypads[i], 
            self.application.WIDTH, 
            self.application.HEIGHT) for i in range(12)]
        self.graphic_text__keypads: list[GraphicText] = [GraphicText(
            self.position_list[i], 
            self.application.game_font, 
            self.key_pad_icon[i], 
            True, 
            (0, 0, 0), 
            self.application.WIDTH, 
            self.application.HEIGHT) for i in range(12)]
        

        self.UI_Node__numpad_node: UI_Node = UI_Node(buttons_list = self.button__keypads)

        self.button__yes: Button = Button(
            (0.4375, 0.5), 
            0.3 / 3, 
            0.15 / 3, 
            GraphicFrame(
                (0.4375, 0.5),
                0.3 / 3,
                0.15 / 3,
                (255, 255, 255), self.application.WIDTH, self.application.HEIGHT))
        self.button__no: Button = Button(
            (0.5625, 0.5), 
            0.3 / 3, 
            0.15 / 3, 
            GraphicFrame(
                (0.4375, 0.5),
                0.3 / 3,
                0.15 / 3,
                (255, 255, 255), self.application.WIDTH, self.application.HEIGHT))
        self.graphic_text__button_yes: GraphicText = GraphicText(
            (0.4375, 0.5), 
            self.application.game_font, 
            "yes", 
            True, 
            (0, 0, 0), 
            self.application.WIDTH, 
            self.application.HEIGHT)
        self.graphic_text__button_no: GraphicText = GraphicText(
            (0.5625, 0.5), 
            self.application.game_font, 
            "no", 
            True, 
            (0, 0, 0), 
            self.application.WIDTH, 
            self.application.HEIGHT)
        self.graphic_text__are_u_sure: GraphicText = GraphicText(
            (0.5, 0.425), 
            self.application.game_font, 
            "are you sure?", 
            True, 
            (0, 0, 0), 
            self.application.WIDTH, 
            self.application.HEIGHT)
        self.graphic_frame__are_u_sure: GraphicFrame = GraphicFrame(
            (0.5, 0.45), 
            0.4, 
            0.2, 
            (55, 182, 255), 
            self.application.WIDTH, 
            self.application.HEIGHT)
        

        self.UI_Node_yes_no_node: UI_Node = UI_Node(
            buttons_list = [self.button__yes, self.button__no], 
            parent = self.UI_Node__numpad_node)
        
        self.local_time: float = 0
        self.initial_set_remaining_time: float = 41
        self.remaining_time: float = 41

        self.graphic_text__remaining_time: GraphicText = GraphicText(
            (0.25, 0.85), 
            self.application.game_font, 
            f"remaining time: {int(self.remaining_time)}", 
            True, 
            (255, 255, 255), 
            self.application.WIDTH, 
            self.application.HEIGHT)
        
        self.graphic_text__choosing_number: GraphicText = GraphicText(
            (0.5, 0.04), 
            self.application.game_font, 
            "choosing number:...", 
            True, 
            (255, 255, 255), 
            self.application.WIDTH, 
            self.application.HEIGHT)

        self._focused_node: UI_Node = self.UI_Node__numpad_node

        self.reserve_ThreadsPoolChossingNumberForBots = self.ThreadsPoolChoosingNumberForBots_once
        self.reserve_ResetPlayersPoolNumbers = self.ResetPlayersPoolNumbers_once
        self.reserve_ResetApplicationInputData = self.ResetApplicationInputData_once


    def KeyPads_InputingValues(self):
        """
        What is a focused node?
            That is the node that the player currently interacts with (the top UI layer), the node whose UI components is on top
                <Visual of what is a focused node, ask me i will explain>

        What can we derive from the foccused node?
            A focused node is useful, especially in the tree nodes, where thing altogether links to the root node
                with a focused node, we can trace back to the root node, 
                    displaying the previous UI layers, 
                    layers by layers, 
                    before laying on top the UI components of the focused node
            Additionally, it also helps to deal with event checking, you just have to check buttons binded in the focused node <focused_node.buttons>
                no need to trace what button should be on demanded, what should be retired
            

        To deal with nodes (with a focused node as a parameters):

            first:
                create a "parent trace", tracing nodes from the focused node all the way back to the root node
                    activate node in trace, deactivate node in trace, 
                    encapsulating it 
                        like this: <activates nodes> {do your thing} <deactivates nodes>

            next, put the focused node button on demand, checking it every frame
                
            next, from the basic layer, we will if else check (is the node activated) the entire tree
                think of it like a framework, when a specific ui_node is activated, something will happen
                    e.g. when <a specific node> is activated, the dt_time automatically equals 0, some text will appears,...
                thing all comes down to your creativity, organizational skills
        """
        def ValidCheckValue(number: int):
            try:
                number = int(number)
                return False if (number > 100 or number < 0) else True
            except Exception as error:
                print(f"the fuck you tryna put in ({error})")
        
        Trace: list[UI_Node] = self._focused_node.TraceBack()
        
        for node in Trace:
            node.activated = True

        self.active_buttons_pool: list[Button] = self._focused_node.buttons_list # only a pointer to the list

        # Layer 1: root node
        if self.UI_Node__numpad_node.activated == True:
            # event takes place (drawing UI components)
            self.graphical_drawing_queue.append(self.graphic_frame__pad)
            self.graphical_drawing_queue = self.graphical_drawing_queue + self.button__keypads
            self.graphical_drawing_queue = self.graphical_drawing_queue + self.graphic_text__keypads

            # event takes place (handling button)
            if self._focused_node == self.UI_Node__numpad_node:
                for i in range(12):
                    button: Button = self.button__keypads[i]
                    if button.is_clicked == True:
                        if i == 11: # submit button
                            isValid = ValidCheckValue(self.input_field)
                            if not isValid:
                                pass
                            else:
                                self._focused_node = self.UI_Node_yes_no_node
                                print("activation")

                        elif i == 10: # backspace button
                            self.input_field = self.input_field if self.input_field == "" else self.input_field[:-1]
                        else:
                            self.input_field = self.input_field + f"{str((i + 1) % 10)}"
                        self.graphic_text__data_input.ChangeMessage(f"number: {self.input_field}")
            else:
                # Layer 2: yes no button
                if self.UI_Node_yes_no_node.activated == True:
                    # even takes place (drawing UI components)
                    self.graphical_drawing_queue.append(self.graphic_frame__are_u_sure)
                    self.graphical_drawing_queue.append(self.graphic_text__are_u_sure)
                    self.graphical_drawing_queue.append(self.button__yes)
                    self.graphical_drawing_queue.append(self.button__no)
                    self.graphical_drawing_queue.append(self.graphic_text__button_yes)
                    self.graphical_drawing_queue.append(self.graphic_text__button_no)
                    
                    if self._focused_node == self.UI_Node_yes_no_node:
                        if self.button__yes.is_clicked:
                            print(f"[MAIN THREAD]: u have made your choice ({self.input_field})")
                            self.application.data_input = int(self.input_field)
                            self._focused_node = self.UI_Node__numpad_node
                            self.input_field = ""
                            self.graphic_text__data_input.ChangeMessage(f"number: {self.input_field}", 
                                                                        self.application.WIDTH, 
                                                                        self.application.HEIGHT)
                        if self.button__no.is_clicked:
                            self._focused_node == self.UI_Node__numpad_node
                            self.application.data_input = -1 

        for node in Trace:
            node.activated = False



    def Update(self, dt: float):
        self.ResetPlayersPoolNumbers_once()
        self.ThreadsPoolChoosingNumberForBots_once(self.application.threads_pool)
        self.ResetApplicationInputData_once()

        mouse_leftclick: bool = False

        for event in pg.event.get():
            if event.type == QUIT:
                self.application.running = False
            if event.type == KEYDOWN:
                if event.key== K_ESCAPE:
                    self.application.running = False
                if event.key == K_p:
                    self.NextStage()
                if event.key == K_o:
                    self.PreviousStage()
            
            if event.type == MOUSEBUTTONDOWN:
                if event.button == BUTTON_LEFT:
                    mouse_leftclick = True
        self.remaining_time -= dt
        self.local_time += dt

        for button in self.active_buttons_pool:
            button.ClickCheck(pg.mouse.get_pos(), self.application.WIDTH, self.application.HEIGHT)
            if button.is_clicked and mouse_leftclick:
                button.is_clicked = True
            else:
                button.is_clicked = False

        if self.remaining_time <= 1:
            self.NextStage()

        self.KeyPads_InputingValues()



    def ThreadsPoolChoosingNumberForBots_once(self, threads_pool: list[AsyncThread] = []):
        """This function runs only once in the game state duration"""
        if not threads_pool:
            raise Exception("no thread available to compute for bot numbers")
        i = 0
        j = 0
        while i < len(self.application.players_pool):
            number_choser: Player = self.application.players_pool[i]
            if type(number_choser) == Bot:
                index = (j % len(threads_pool))
                print(f"hello thread {index}")
                threads_pool[index].action_queue.put({"function": number_choser.get_number, "args": ()})
                j += 1
            i += 1
        self.ThreadsPoolChoosingNumberForBots_once = lambda threads_pool: None
    
    def ResetApplicationInputData_once(self):
        self.application.data_input = -1
        self.ResetApplicationInputData_once = lambda: None
     
    def ResetPlayersPoolNumbers_once(self):
        for player in self.application.players_pool:
            player.number = -1
        self.ResetPlayersPoolNumbers_once = lambda: None

    def ReviveOneTimeFunctions(self):
        self.ThreadsPoolChoosingNumberForBots_once = self.reserve_ThreadsPoolChossingNumberForBots
        self.ResetPlayersPoolNumbers_once = self.reserve_ResetPlayersPoolNumbers
        self.ResetApplicationInputData_once = self.reserve_ResetApplicationInputData

    def NextStage(self):
        if all([not thread.is_busy for thread in self.application.threads_pool]):
            if self.application.data_input == -1:
                print("not yet able to pass into next stage")
            else:
                self.application.current_state = self.application.state_dict["result"]
                # start to calculate result phase gameloop function
                self.application.threads_pool[0].action_queue.put({"function": self.application.current_state.gameloop.run, "args": ()})
                self.ReviveOneTimeFunctions()
                self.local_time = 0
                self.remaining_time = self.initial_set_remaining_time
                self.application.data_input = -1
                self.input_field = ""
            

    def PreviousStage(self):
        # all of the threads are free from works
        if all([not thread.is_busy for thread in self.application.threads_pool]): 
            self.application.current_state = self.application.state_dict["lobby"]
            self.ReviveOneTimeFunctions()
            self.local_time = 0
            self.remaining_time = self.initial_set_remaining_time
            self.application.data_input = -1
            self.input_field = ""
        else:
            print("the threads have not done their jobs")
    
    def Render(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        surface.fill((0, 0, 0))
        
        for graphic in self.graphical_drawing_queue:
            graphic.Draw(surface)
        self.graphical_drawing_queue.clear()

        self.graphic_text__remaining_time.ChangeMessage(f"{int(self.remaining_time)}", self.application.WIDTH, self.application.HEIGHT)
        self.graphic_text__remaining_time.Draw(surface)

        self.graphic_text__choosing_number.Draw(surface)
        self.graphic_text__data_input.Draw(surface)

        pg.display.flip()
        pg.display.set_caption(f"{self.application.clock.get_fps() // 1}")
        self.application.clock.tick(FPS)
