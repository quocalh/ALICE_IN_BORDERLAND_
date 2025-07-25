import numpy as np
import pygame as pg

from components.settings import *

class Graphic:
    def __init__(self, pposition: tuple,
                 pw: float = 0.05,
                 ph: float = 0.05,
                 ):
        self.pposition: tuple = pposition
        self.pw: float = pw
        self.ph: float = ph

        self.original_texture = None
        self.texture = None

        self.visible = True
        self.a: int = 255

    def TextureSetAlpha(self, new_a: int):
        pg.surface.Surface.set_alpha(self.texture, new_a)
        

    def Draw(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        raise Exception(NotImplemented)


class GraphicFrame(Graphic):
    def __init__(self, pposition, pw = 0.05, ph = 0.05, 
                 color: tuple[int, int, int] = ((255, 255, 255)),
                 WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        super().__init__(pposition, pw, ph)
        self.color: tuple[int, int, int] = color
        
        self.texture: pg.surface.Surface = pg.surface.Surface((self.pw * WIDTH, self.ph * HEIGHT))
        self.texture.fill(color)

        self.original_texture: pg.surface.Surface = pg.surface.Surface((self.pw * WIDTH, self.ph * HEIGHT))
        self.original_texture.fill(color)
        
    
    def Draw(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        if self.visible == False:
            return
        x = WIDTH * (self.pposition[0] - self.pw / 2)
        y = HEIGHT * (self.pposition[1] - self.ph / 2)

        surface.blit(self.texture, (x, y))

class GraphicText(Graphic):
    def __init__(self, pposition, 
                 font, 
                 message: str, 
                 anti_alias: bool,
                 color: tuple[int, int, int] = (255, 255, 255),
                 WIDTH: int = WIDTH,
                 HEIGHT: int = HEIGHT
                 ):
        super().__init__(pposition, 0, 0)
        self.font: pg.font.Font = font
        self.message = message

        self.anti_alias = anti_alias

        self.color: tuple[int, int, int] = color

        self.texture: pg.surface.Surface = self.font.render(message, self.anti_alias, self.color)
        self.original_texture = self.font.render(message, self.anti_alias, self.color)

        self.pw = self.texture.get_width() / WIDTH
        self.ph = self.texture.get_height() / HEIGHT
    

    def ChangeMessage(self, overwriting_message: str, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        self.message = overwriting_message
        self.texture = self.font.render(overwriting_message, self.anti_alias, self.color)
        self.original_texture = self.font.render(overwriting_message, self.anti_alias, self.color)
        self.pw = self.texture.get_width() / WIDTH
        self.ph = self.texture.get_height() / HEIGHT

    def Draw(self, surface: pg.surface.Surface):
        x = WIDTH * (self.pposition[0] - self.pw / 2)
        y = HEIGHT * (self.pposition[1] - self.ph / 2)
        surface.blit(self.texture, (x, y))

class GraphicTexture(Graphic):
    def __init__(self, pposition: tuple, 
                 texture: pg.surface.Surface, 
                 pw = 0.05, ph = 0.05,
                 WIDTH: int = WIDTH,
                 HEIGHT: int = HEIGHT,
                 ):
        super().__init__(pposition, pw, ph)
        self.texture = texture
        self.texture = pg.transform.scale(self.texture, (pw * WIDTH, ph * HEIGHT))
        self.original_texture = texture
        self.original_texture = pg.transform.scale(self.original_texture, (pw * WIDTH, ph * HEIGHT))
    
    def Draw(self, surface: pg.surface.Surface):
        x = WIDTH * (self.pposition[0] - self.pw / 2)
        y = HEIGHT * (self.pposition[1] - self.ph / 2)
        surface.blit(self.texture, (x, y))









class Button:
    def __init__(self, pposition: tuple,
                 pw: float  = 0.05,
                 ph: float = 0.05,
                 graphic: Graphic = None,
                 WIDTH: int = WIDTH,
                 HEIGHT: int = HEIGHT,
                 ):
        self.pposition: tuple = list(pposition)
        self.pw: float = pw
        self.ph: float = ph

        if graphic == None:
            self.graphic = GraphicFrame(self.pposition, self.pw, self.ph, (0, 255, 100), WIDTH, HEIGHT)
        else:
            graphic.pposition = list(graphic.pposition)
            self.graphic: Graphic = graphic
        
        self.activated: bool = True
        self.is_clicked: bool = False
    
    def ClickCheck(self, MouseClickingPosition: tuple, WIDTH: int, HEIGHT: int):
        if not self.activated:
            return False
        if - self.pw / 2 <= MouseClickingPosition[0] / WIDTH - self.pposition[0] <= self.pw / 2:
            if - self.ph / 2 <= MouseClickingPosition[1] / HEIGHT -  self.pposition[1] <= self.ph / 2:
                self.is_clicked = True
                return True
        self.is_clicked = False
        return False

    def Draw(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        self.graphic.pposition[0] = self.pposition[0]
        self.graphic.pposition[1] = self.pposition[1]
        self.graphic.Draw(surface, WIDTH, HEIGHT)
    



class UI_Node: ...
class UI_Node: 
    def InsertChildren(self, children_node: UI_Node): pass
class UI_Node:
    """
    Ideas:
        we can have a tree as a ui_node 
            when the focused_node is pointed at the node (that is another UI_tree)
                the focused_node will receive the info dumped from the small tree, trace it back to the main tree
    """
    def __init__(self,
                 buttons_list: list[Button] = None,
                 parent: UI_Node = None,
                 children: list[UI_Node] = None,
                 occupation: str = "yes no ui handling", # sample
                 ):
        self.buttons_list: list[Button] = buttons_list if buttons_list else []
        self.occupation = occupation

        self.parent = parent
        if parent != None:
            parent.InsertChildren(self)

        self.children_list = children if children else []
        self.generation = 0 if self.parent == None else - 1

        self.activated: bool = False

        for children in self.children_list:
            self.InsertChildren(children)
            

    def InsertChildren(self, children_node: UI_Node):
        children_node.generation = self.generation + 1
        children_node.parent = self
        self.children_list.append(children_node)

    
    @staticmethod
    def PrintTreeNode(root_node: UI_Node):
        root_node: UI_Node = root_node
        print("\t" * root_node.generation + root_node.occupation)
        for children in root_node.children_list:
            UI_Node.PrintTreeNode(children)

    def TraceBack(self, trace_list: list[UI_Node] = None):
        trace_list = trace_list if trace_list else []
        trace_list.append(self)

        if self.parent == None:
            return trace_list
        
        return self.parent.TraceBack(trace_list)
    




            
    

        
     