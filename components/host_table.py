import pygame as pg
from pygame.locals import *
from random import shuffle
import numpy as np


# from UI import *
from components.UI import * 
pg.init() 
pg.display.set_mode((WIDTH, HEIGHT))

"""
ABOUT THE VALUE IN CARDS:
IT SUPPOSES TO TELL YOU BOTH THE RANK AND SUIT
FLOAT VALUE IS VALID IN THE FORMAT : <RANK>.<SUIT> 
    FOR EXAMPLE, 0.0 INDICATE 3.0 (THE SMALLEST) 
    IN ANOTHER EXAMPLE, 12.4 INDICATE 2 WITH THE HEART (THE LARGEST)
OBVIOUSLY, THE CONSTRIANT EXIST! 
    RANK ONLY VARIES FROM 0 TO 12. 
    FOR SUITS, IT WOULD BE ONLY FROM 0 TO 3  


ABOUT PROPORTION:
- MOBILE PLAYERS EXIST
- STORE IN PROPORTION, SO MOBILE USER WONT GET ANY UI GLITCHES 


THE FIRST MAOJOR ROAD BLOCK
FIGURE OUT THE BEST WAY TO HANDLE BOTH GRAPHIC AND BUTTONS     
DRAWN BUTTON MUST BE CLICKABLE? NAH ONLY CLICKABLE IN A CERTAIN, CURRENT LAYER

I THINK I FIGURE IT OUT
GAME LOOP SECTOR

5/1/2024 EASY AS FUCK, FIXED THE UI NODE, DONE A SAMPLE ULTILIZING THEM TO PLAY BLACK JACK
NOW TURN TO GRAPHIC | SHOULD BE DONE IN THE NEXT MORNING 

5/4/2025:
finisih animaiton, fade in fade out | let us sketch the games
"""

name_rank = "3 4 5 6 7 8 9 10 Jack Queen King Arch 2".split()
name_suit = "Spades Clubs Diamonds Hearts".split()

string_rank = "3 4 5 6 7 8 9 10 J Q K A 2".split()
string_suit = "S C D H".split()

Dict_index_card = []

# Load card texture (front)
Dict_Index_CardsImages: list = [] 
for i in range(len(string_rank)):
    for j in range(len(string_suit)):
        image = pg.image.load(f"assets/cards/{string_rank[i]}{string_suit[j]}.png").convert_alpha()
        image = pg.transform.scale(image, (CARD_PROPORTION_X * WIDTH, CARD_PROPORTION_Y * HEIGHT)).convert_alpha()
        Dict_Index_CardsImages.append(image)
# Load card texture (back)
Back_CardImages = pg.image.load(r"assets\back\ril_back.png").convert_alpha()
Back_CardImages = pg.transform.scale(Back_CardImages, (CARD_PROPORTION_X * WIDTH, CARD_PROPORTION_Y * HEIGHT)).convert_alpha()
"""

pg.surface.Surface.set_alpha(Back_CardImages, 50) 
valid function! light weight overall, pretty fast!
"""


# Create class for cards
class Cards:
    def __init__(self, value: float, pposition: np.ndarray = np.zeros(2, dtype = np.float64), WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        self.value = value
        self.index = int((value // 1) * 4 + (value % 1) * 10)

        self.texture: GraphicTextureNotOptimizedYet = GraphicTextureNotOptimizedYet(pposition, Dict_Index_CardsImages[self.index], CARD_PROPORTION_X, CARD_PROPORTION_Y, WIDTH, HEIGHT)
        self.back_texture: GraphicTextureNotOptimizedYet = GraphicTextureNotOptimizedYet(pposition, Back_CardImages, CARD_PROPORTION_X, CARD_PROPORTION_Y, WIDTH, HEIGHT)

        self.pposition = pposition
        self.position = np.zeros(2, dtype = np.float64)
        self.hidden = False

        self.visible = True
        self.interactable = False

    def Draw(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        if not self.visible:
            return
        
        if self.hidden:
            self.back_texture.pposition[0] = self.pposition[0]
            self.back_texture.pposition[1] = self.pposition[1]
            self.back_texture.Draw(surface, WIDTH, HEIGHT)
        else:
            self.texture.pposition[0] = self.pposition[0]
            self.texture.pposition[1] = self.pposition[1]
            self.texture.Draw(surface, WIDTH, HEIGHT)

    def __repr__(self) -> str:
        rank = int(self.value // 1)
        suit = int(self.value % 1 * 10)
        return f"{name_rank[rank]} of {name_suit[suit]}"


FullDeck = []
for i in range(len(string_rank)):
    for j in range(len(string_suit)):
        Card = Cards(i + j / 10)
        FullDeck.append(Card)


class CardDeck:
    def __init__(self):
        self.deck: list[Cards] = FullDeck
        shuffle(self.deck)
        self.drawn_deck = []
    
    def DrawCard(self):
        card = self.deck.pop()
        self.drawn_deck.append(card)
        return card

    def ResetDeck(self):
        self.deck = FullDeck
    
    def DrawCards(self, surface: pg.surface.Surface, px: float = 0.5, py: float = 0.5):
        """"""
        for i in range(len(self.deck)):
            Card: Cards = self.deck[i]
            Card.pposition[0] = px
            Card.pposition[1] = py + CARD_DECK_WIDTH * i
            Card.Draw(surface, WIDTH, HEIGHT)


class Player:
    def __init__(self):
        self.cards = []
        self.score = 0
    
    def DrawCardFromDeck(self, card_deck: CardDeck):
        if len(card_deck.deck) == 0:
            print("there is no card to pull, lol")
            return None
        else:
            drawn_card = card_deck.DrawCard()
            self.cards.append(drawn_card)
            # not done yet (self.score)

    def MaximizeScore(self):
        """ Finn | hashmap detected """
        pass
    
    def DrawCards(self, surface: pg.surface.Surface, topleft_px: float, topleft_py: float, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        """px, py are top left proportional abitraries :sob: | the position is not right either but would fix later"""
        for i in range(len(self.cards)):
            card: Cards = self.cards[i]
            card.pposition[0] = topleft_px + i * CARD_PWIDTH_INTERVAL
            card.pposition[1] = topleft_py
            card.Draw(surface, WIDTH, HEIGHT)

    def GetScore(self):
        return self.score
    


class Host(Player):
    def __init__(self):
        super().__init__()

    def DrawCardFromDeck(self, card_deck: CardDeck):
        if len(card_deck.deck) == 0:
            return None
        else:
            drawn_card = card_deck.DrawCard()
            drawn_card.hidden = True
            self.cards.append(drawn_card)            

    def Gambit(self):
        pass



# constructing a UI Node
"""LAYER 1"""
default_font = pg.font.SysFont("Arial", 50, True)

root_node = UI_Nodes()
button1 = Buttons(np.array((1/3, 0.8), dtype = np.float64), 0.25, 0.15) # draw
button2 = Buttons(np.array((2/3, 0.8), dtype = np.float64), 0.25, 0.15) # stand
# text1_draw = GraphicText((1/3, 0.8), default_font, "DRAW", 0.25, 0.15, True)
# text1_stand = GraphicText((2/3, 0.8), default_font, "STAND", 0.25, 0.15, True)
text1_draw = GraphicText((1/3, 0.8), default_font, "DRAW", True)
text1_stand = GraphicText((2/3, 0.8), default_font, "STAND", True)

root_node.buttons.append(button1)
root_node.buttons.append(button2)

"""LAYER 2"""
are_u_sure_node = UI_Nodes([], parent = root_node, children = [], occupation = "Are you sure?")
root_node.InsertChildren(are_u_sure_node)

button2_sure = Buttons(np.array((0.25, 0.5), dtype = np.float64), 0.2, 0.1)
button2_no   = Buttons(np.array((0.75, 0.5), dtype = np.float64), 0.2, 0.1)
# text2_are_u_sure = GraphicText((0.55, 0.15), default_font, "ARE U SURE?", 0.5, 0.2, True)
# text2_sure = GraphicText((0.25, 0.5), default_font, "SURE", 0.2, 0.1, True)
# text2_no = GraphicText((0.75, 0.5), default_font, "NO", 0.2, 0.1, True)
text2_are_u_sure = GraphicText((0.55, 0.15), default_font, "ARE U SURE?", True)
text2_sure = GraphicText((0.25, 0.5), default_font, "SURE", True)
text2_no = GraphicText((0.75, 0.5), default_font, "NO", True)

are_u_sure_node.buttons.append(button2_sure)
are_u_sure_node.buttons.append(button2_no)

# UI_Nodes.PrintTreeNode(root_node)

class GameLoopBlackJack:
    """
    SAMPLE CLASS FOR GAME LOOP | NOTE: THIS IS A CUSTOM CLASS | THE CLIENT CLASS
    """
    def __init__(self, root_node: UI_Nodes = root_node):
        self.node_path = [] # storing child nodes
        self.root_node = root_node

        self.card_deck = CardDeck()
        self.player = Player()
        self.host = Host()

        self.score = 0

        self.button_click_check_queue: Buttons = []
        self.graphic_drawing_queue: Buttons = []


        # logic
        self.has_stood = False
        self.reveal_host: bool = False
        self.focused_node: UI_Nodes = root_node

    def Loop(self):
        """
        
        ON YOUR WAY TO REACH THE FOCUSED NODE, YOU WOULD REACH THE PREVIOUS CHOICES -> RENDER GRAPHICS, BUTTONS ON THE WAY
        SAMPLE OF 2 LAYER DIALOUGE OVERLAY 
        """

        # not being constraint to mouse button event
        """
        main 
        {
        self.focused node (***)
        self.node path
        self.activated (used to be so, not now)

        }
        """

        """
        LAYER 1
        """
        for button in self.root_node.buttons:
            self.graphic_drawing_queue.append(button)
            button.visible = True 
        text1_draw.visible = True
        text1_stand.visible = True

        self.graphic_drawing_queue.append(text1_draw)
        self.graphic_drawing_queue.append(text1_stand)

        if self.root_node == self.focused_node:
            # self.root_node.activated = True
            self.button_click_check_queue = self.root_node.buttons
            if self.root_node.buttons[0].is_clicked == True: # draw
                self.player.DrawCardFromDeck(self.card_deck)
            # elif self.root_node.buttons[1].is_clicked == True: # stand 
            elif self.root_node.buttons[1].is_clicked == True: # stand 
                self.focused_node = root_node.children[0]
                self.node_path.append(0)
                # self.focused_node.activated = True
        else:

            """
            LAYER 2
            """
            node_2nd: UI_Nodes = self.root_node.children[self.node_path[0]]  
            
            for button in self.root_node.buttons:
                button.visible = False
            text1_draw.visible = False
            text1_stand.visible = False

            for button in node_2nd.buttons:
                self.graphic_drawing_queue.append(button)

            self.graphic_drawing_queue.append(text2_are_u_sure)
            self.graphic_drawing_queue.append(text2_sure)
            self.graphic_drawing_queue.append(text2_no)

            if node_2nd == self.focused_node:
                self.button_click_check_queue = node_2nd.buttons
                if node_2nd.buttons[0].is_clicked == True:
                    for card in self.host.cards:
                        card: Cards = card
                        card.hidden = not card.hidden
                elif node_2nd.buttons[1].is_clicked == True:
                    print("no?")
                    self.focused_node = self.root_node
                    self.node_path.pop()
                    for _ in range(len(node_2nd.parent.buttons)):
                        self.graphic_drawing_queue.pop()
            
            
        
    
    def Draw(self, surface: pg.surface.Surface, MousePosition: np.ndarray, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        self.player.DrawCards(surface, 0.1, 0.5, WIDTH, HEIGHT)
        self.host.DrawCards(surface, 0.1, 0.2, WIDTH, HEIGHT)

        for graphic in self.graphic_drawing_queue:
            graphic: Graphic = graphic
            graphic.Draw(surface, WIDTH, HEIGHT)
        self.graphic_drawing_queue = []

        

        
    def HandleButtonCheck(self, is_mouse_clicked: bool, MousePosition, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        for button in self.button_click_check_queue:
            button: Buttons = button
            button.is_clicked = is_mouse_clicked
            if is_mouse_clicked:
                button.ClickCheck(MousePosition, WIDTH, HEIGHT)
        self.button_click_check_queue = []
                

    def DrawButtons(self, buttons_list, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        for button in buttons_list:
            button: Buttons = button
            button.Draw(surface, WIDTH, HEIGHT)
        



                

