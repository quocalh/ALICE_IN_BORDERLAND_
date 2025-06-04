import numpy as np
import pygame as pg

from components.settings import *
from components.settings import CARD_PROPORTION_X, CARD_PROPORTION_Y


"""
NOTE: for both graphic text an graphic texture:
    {
    if int(self.texture.width - self.pw * WIDTH) != 0 or int(self.texture.height - self.ph * HEIGHT) != 0:
            self.Transfrom(WIDTH, HEIGHT)
    }
        - that line was meant to check whether if self.pw and self.ph have been changed or not, so we can scale it to match the changed resolution
            however, since self.pw * WIDTH and ph * HEIGHT can produce float, idk if the texture width and height can do so.
                => be cautious, these are only an approximation, quick fix for the code
                    <=> if something weird happens in the Graphic Texture and Graphic Text code, consider that line of code.
"""

# print(pg.SRCALPHA)
class Graphic:
    """
    SUPPOSED TO BE AN INDEPENDENT INSTANCES
    """
    def __init__(self, pposition: np.ndarray, 
                 pw: float = CARD_PROPORTION_X, 
                 ph: float = CARD_PROPORTION_Y
                 ):
        self.pposition = pposition
        self.pw = pw
        self.ph = ph

        self.texture: pg.surface.Surface = None
        
        self.visible = True # if done implementing alpha value, this gonna be dumped
        self.a: int = 255 # alpha_value

        self.previous_a: int = self.a
        self.previous_pposition: tuple[float, float] = np.array(self.pposition, dtype = np.float64)
        self.previous_pw: float = self.pw
        self.previous_ph: float = self.ph

    def TextureGetSetAlpha(self, new_a: int = None):
        
        if new_a == None or self.a == new_a:
            pg.surface.Surface.set_alpha(self.texture, self.a)
        else:
            pg.surface.Surface.set_alpha(self.texture, new_a)
            self.a = new_a


    def Draw(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        raise f"No draw function found in the class ({self.__class__})"

class GraphicFrame(Graphic):
    def __init__(self, pposition: np.ndarray, 
                 pw: float = CARD_PROPORTION_X, 
                 ph: float = CARD_PROPORTION_Y,
                 color: tuple[int, int, int] = (55,182,255),
                 WIDTH: int =  WIDTH,
                 HEIGHT: int = HEIGHT,
                 ):
        super().__init__(pposition, pw, ph)
        self.texture: pg.surface.Surface = pg.surface.Surface((self.pw * WIDTH, self.ph * HEIGHT))
        pg.surface.Surface.set_alpha(self.texture, self.a)
        self.texture.fill(color)

        self.color = color
        self.previous_color = self.color
        
    def Draw(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        if self.visible == False:
            return
        
        x = WIDTH * (self.pposition[0] - self.pw / 2)
        y = HEIGHT * (self.pposition[1] - self.ph / 2)

        if self.previous_pw != self.pw or self.previous_ph != self.ph:
            self.previous_pw = self.pw
            self.previous_ph = self.ph
            self.texture: pg.surface.Surface = pg.surface.Surface((self.pw * WIDTH, self.ph * HEIGHT))

        if self.previous_a != self.a:
            self.TextureGetSetAlpha()
            self.previous_a = self.a

        if self.color != self.previous_color:
            self.previous_color = self.color
            self.texture.fill(self.color)

        surface.blit(self.texture, (x, y))

class GraphicTextureNotOptimizedYet(Graphic):
    def __init__(self, pposition: np.ndarray, 
                 texture: pg.surface.Surface = None,
                 pw: float = CARD_PROPORTION_X, 
                 ph: float = CARD_PROPORTION_Y,
                 WIDTH: int = WIDTH,
                 HEIGHT: int = HEIGHT,
                 ):
        super().__init__(pposition, pw, ph)
        
        if texture == None:
            print(f"warning! the texture has not been defined yet, ({self.Name()})")
        else:
            self.texture: pg.surface.Surface = texture.convert_alpha()
            self.TextureGetSetAlpha()
            self.Transfrom(WIDTH, HEIGHT)

    def Transfrom(self, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        self.texture = pg.transform.scale(self.texture, (self.pw * WIDTH, self.ph * HEIGHT)).convert_alpha()

    def Draw(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        if int(self.texture.width - self.pw * WIDTH) != 0 or int(self.texture.height - self.ph * HEIGHT) != 0:
            self.Transfrom(WIDTH, HEIGHT)
        if self.visible == False:
            return
        x =  WIDTH * (self.pposition[0] - self.pw / 2)
        y =  HEIGHT * (self.pposition[1] - self.ph / 2)
        self.TextureGetSetAlpha()
        surface.blit(self.texture, (x, y))

    @classmethod
    def Name(self):
        return self.__name__

class GraphicText(Graphic):
    def __init__(self, pposition: np.ndarray, 
                 font: pg.font.Font,
                 message: str = "Im vincing it, so good!",
                 anti_alias: bool = False,
                 color: tuple[int, int, int] = (255, 255, 255),
                 WIDTH: int = WIDTH, 
                 HEIGHT: int = HEIGHT
                 ):
        super().__init__(pposition, 0, 0)
        self.font = font
        self.message = message
        self.anti_alias = anti_alias
        self.color = color

        self.texture: pg.surface.Surface = self.font.render(self.message, anti_alias, self.color).convert_alpha()
        self.TextureGetSetAlpha()
        self.pw = self.texture.get_width() / WIDTH
        self.ph = self.texture.get_height() / HEIGHT

    def ChangeMessage(self, new_message: str, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        """ IDK if this was finnished or not """
        self.texture: pg.surface.Surface = self.font.render(new_message, self.anti_alias, self.color).convert_alpha()
        self.TextureGetSetAlpha()
        self.pw = self.texture.get_width() / WIDTH
        self.ph = self.texture.get_height() / HEIGHT

    def Transfrom(self, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        self.texture = pg.transform.scale(self.texture, (self.pw * WIDTH, self.ph * HEIGHT)).convert_alpha()

    def Draw(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        if int(self.texture.width - self.pw * WIDTH) != 0 or int(self.texture.height - self.ph * HEIGHT) != 0:
            print(f"hello | {self.texture.width} vs {self.pw * WIDTH}")
            self.Transfrom(WIDTH, HEIGHT) 

        if self.visible == False:
            return 
        
        x =  WIDTH * (self.pposition[0] - self.pw / 2)
        y =  HEIGHT * (self.pposition[1] - self.ph / 2)

        if self.previous_a != self.a:
            self.TextureGetSetAlpha()

        surface.blit(self.texture, (x, y))

    @classmethod
    def Name(self):
        return self.__name__


"""

██████╗░██╗░░░██╗███╗░░██╗░█████╗░███╗░░░███╗██╗░█████╗░  ░█████╗░██████╗░░░░░░██╗███████╗░█████╗░████████╗░██████╗
██╔══██╗╚██╗░██╔╝████╗░██║██╔══██╗████╗░████║██║██╔══██╗  ██╔══██╗██╔══██╗░░░░░██║██╔════╝██╔══██╗╚══██╔══╝██╔════╝
██║░░██║░╚████╔╝░██╔██╗██║███████║██╔████╔██║██║██║░░╚═╝  ██║░░██║██████╦╝░░░░░██║█████╗░░██║░░╚═╝░░░██║░░░╚█████╗░
██║░░██║░░╚██╔╝░░██║╚████║██╔══██║██║╚██╔╝██║██║██║░░██╗  ██║░░██║██╔══██╗██╗░░██║██╔══╝░░██║░░██╗░░░██║░░░░╚═══██╗
██████╔╝░░░██║░░░██║░╚███║██║░░██║██║░╚═╝░██║██║╚█████╔╝  ╚█████╔╝██████╦╝╚█████╔╝███████╗╚█████╔╝░░░██║░░░██████╔╝
╚═════╝░░░░╚═╝░░░╚═╝░░╚══╝╚═╝░░╚═╝╚═╝░░░░░╚═╝╚═╝░╚════╝░  ░╚════╝░╚═════╝░░╚════╝░╚══════╝░╚════╝░░░░╚═╝░░░╚═════╝░ (they handle events)
"""


class Buttons: 
    def __init__(self, pposition: np.ndarray, 
                 pw: float = CARD_PROPORTION_X, 
                 ph: float = CARD_PROPORTION_Y,
                 graphic: Graphic = None):
        self.pposition = pposition
        self.position = np.zeros(2, dtype = np.float64)
        self.pw = pw
        self.ph = ph

        self.rect = pg.rect.Rect(0, 0, 0, 0)
        self.graphic = graphic
        if self.graphic == None:
            self.graphic = GraphicFrame(self.position, pw, ph)

        self.visible = True
        self.activated = True
        self.is_clicked = False
    
    def ClickCheck(self, MousePosition: np.ndarray, WIDTH: float = WIDTH, HEIGHT: float = HEIGHT):
        """ 
        the function is not good, since it looks simpler than it must be 
        in order for it to work correctly, u have to understand that the is_clicked wont reset until u manually switch it back to False lol
        
        i dont know if i would spend time rework this function
        """
        if not self.activated:
            return False
        
        MousePPositionX = MousePosition[0] / WIDTH
        MousePPositionY = MousePosition[1] / HEIGHT
        
        if - self.pw / 2 <= MousePPositionX - self.pposition[0] <= self.pw / 2:
            if - self.ph / 2 <= MousePPositionY - self.pposition[1] <= self.ph / 2:
                self.is_clicked = True
                return True
        self.is_clicked = False
        return False

    def IsClicked(self):
        return self.is_clicked

    def Execute(self):
        print("hello")

    def Draw(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        if self.visible ==  False:
            return 
        # print(self.graphic.pposition)
        self.graphic.pposition[0] = self.pposition[0]
        self.graphic.pposition[1] = self.pposition[1]
        self.graphic.Draw(surface, WIDTH, HEIGHT)

class NumberTablet:
    pass

class Time:
    def __init__(self, allocated_tick: int):
        self.allocated_second: int = allocated_tick / 1000
        self.second_passed: int = 0
    
    def GetRemaingTime(self):
        pass

    def Tick(self, dt: float):
        self.second_passed += dt
        

"""

░██████╗████████╗██████╗░██╗░░░██╗░█████╗░████████╗
██╔════╝╚══██╔══╝██╔══██╗██║░░░██║██╔══██╗╚══██╔══╝
╚█████╗░░░░██║░░░██████╔╝██║░░░██║██║░░╚═╝░░░██║░░░
░╚═══██╗░░░██║░░░██╔══██╗██║░░░██║██║░░██╗░░░██║░░░
██████╔╝░░░██║░░░██║░░██║╚██████╔╝╚█████╔╝░░░██║░░░
╚═════╝░░░░╚═╝░░░╚═╝░░╚═╝░╚═════╝░░╚════╝░░░░╚═╝░░░
"""
class UI_Nodes: ...
class UI_Nodes:
    root: UI_Nodes = None
    def __init__(self, 
                 buttons: list[Buttons] = None, 
                 parent: UI_Nodes = None, 
                 children: list[UI_Nodes] = None,
                 occupation: str = "Im omning it, so good!"
                 ):
        self.parent: UI_Nodes = parent
        self.buttons: list = buttons if buttons is not None else [] # bro, it could be a set, why use list?
        self.children: list = children if children is not None else [] # bro, it could be a set, why use list?

        if self.parent == None: # if you re the first node to be generated
            self.root = self
            self.generation = 0
        else: 
            self.generation = parent.generation + 1
            assert self.parent != None, "This node lacks the parent parameter" # would be wrong if u have no parent at all      
            self.parent.children.append(self)       

        self.occupation = occupation
        
        self.activated: bool = False 
        


    def InsertChildren(self, Node: UI_Nodes):
        Node.parent = self
        self.children.append(Node)



    @staticmethod
    def PrintTreeNode(node_root: UI_Nodes):
        host: UI_Nodes = node_root
        indent = "\t\t" * host.generation
        print(indent + f"- {host.occupation}")
        for children in host.children:
            UI_Nodes.PrintTreeNode(children)

    def TraceBack(self, trace_list: list[UI_Nodes] = None):
        """tracing from this to the root node"""
        if trace_list == None:
            trace_list = []

        trace_list.append(self)
            
        if self.parent == None: # if the node itself is the root
            return trace_list
        
        return self.parent.TraceBack(trace_list)

class UI_Nodes_rework:
    def __init__(self):
        pass


"""
░█████╗░███╗░░██╗██╗███╗░░░███╗░█████╗░████████╗██╗░█████╗░███╗░░██╗
██╔══██╗████╗░██║██║████╗░████║██╔══██╗╚══██╔══╝██║██╔══██╗████╗░██║
███████║██╔██╗██║██║██╔████╔██║███████║░░░██║░░░██║██║░░██║██╔██╗██║
██╔══██║██║╚████║██║██║╚██╔╝██║██╔══██║░░░██║░░░██║██║░░██║██║╚████║
██║░░██║██║░╚███║██║██║░╚═╝░██║██║░░██║░░░██║░░░██║╚█████╔╝██║░╚███║
╚═╝░░╚═╝╚═╝░░╚══╝╚═╝╚═╝░░░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═╝░╚════╝░╚═╝░░╚══╝
"""
class AnimationRegistry:
    "work like a particle system (QUEUE), once its job is done, the animation_particle disappears into thin air"
    def __init__(self):
        self.animation_queue: list[Animation] = []
        self.rigid_animation: RigidAnimation = None
        

    def Animating(self, dt: float):
        # self.animation_queue here
        for i in range(len(self.animation_queue) - 1, -1, -1):   

            animation_particle: Animation = self.animation_queue[i]
            animation_particle.Animating(dt)

            if animation_particle.kill_themself == True: # if so, delete them ; swap to delete (O(1) complexity)
                temp = animation_particle # swapping
                self.animation_queue[i] = self.animation_queue[-1]
                self.animation_queue[-1] = temp
                self.animation_queue.pop()

        if type(self.rigid_animation) == RigidAnimation:
            self.rigid_animation.Animating(dt)
            if self.rigid_animation.kill_themself == True:
                self.rigid_animation = None
    
    def CutsceneInProcess(self):
        if self.rigid_animation == None:
            return False
        return not self.rigid_animation.kill_themself
        

    

class Animation:
    """
    - unknown fps -> ?dt (given const; spontaneous)
    - run from 0 to 1 linearly in a given constrained time
    NOTE: U CAN ERASE IT
    # y = smoothstep(x) # linear -> non linear
    # lerp(y) # lerp(x): linear transformation | => lerp(y): non linear transformation
    """
    def __init__(self, milisecond_interval: float,  
                 object_w_pposition: Graphic,
                 destinated_pposition: list[float, float],
                 ):
        assert hasattr(object_w_pposition, "pposition"), "[Animation]: the given object does not have pposition attribute!"
        self.object_w_pposition: Graphic = object_w_pposition

        self.current_pposition: list[float, float] = [0, 0]
        self.current_pposition[0] = object_w_pposition.pposition[0]
        self.current_pposition[1] = object_w_pposition.pposition[1]

        self.destinated_pposition: list[float, float] = destinated_pposition

        self.interval = milisecond_interval / 1000 # set its unit as seconds

        self.t = 0
        self.kill_themself: bool = False # flag to commit suicide :pensive:

        self.velocity = 1 / self.interval # stay const
        

    def Animating(self, dt) -> tuple[float, float]: 
        self.t += self.velocity * dt
        if self.t > 1:
            self.t = 1 
            self.kill_themself = True
        k = self.t # y = x
        k = self.SmoothStep(self.t) # y = f(x)
        lerp_x = self.Lerp(self.current_pposition[0], self.destinated_pposition[0], k) # linear path first
        lerp_y = self.Lerp(self.current_pposition[1], self.destinated_pposition[1], k) # linear path first
        self.object_w_pposition.pposition[0] = lerp_x
        self.object_w_pposition.pposition[1] = lerp_y
        return (lerp_x, lerp_y)
        
            
        

    @staticmethod
    def Lerp(a, b, t):
        assert 0 <= t <= 1, "The t value is supposed to be between 0 and 1."
        return a * (1 - t) + b * t

    @staticmethod
    def SmoothStep(t):
        return 3 * (t * t) - 2 * (t * t * t)

    @staticmethod
    def SmoothLand(t):
        pass

class RigidAnimation(Animation):
    """
    work like particle system (QUEUE), but only 1 set of particle exist and the flag would return true if done the procedure animation
    if self.in_process is True, the event button check would be skippeds
    constraint:
    - only one exist, doing 1 thing at the time, or just buying time for the animation particle
    - 
    """
    def __init__(self, milisecond_interval: float, 
                 object_w_pposition: Graphic, 
                 destinated_pposition: list[float]):
        super().__init__(milisecond_interval, object_w_pposition, destinated_pposition)


class FadeIn(Animation):
    """
    Is not supposed to have multiple call in the same object, multiple call of this effect upon an object would result in overwriting alpha value, which the show the lastest alpha value in the queue 
    """
    def __init__(self, milisecond_interval: int,
                 graphic: Graphic,
                 ):
        self.interval: float = milisecond_interval / 1000
        self.graphic: Graphic = graphic
        self.graphic.TextureGetSetAlpha(0)
        self.kill_themself = False
        self.t = 0
        self.velocity = 1 / self.interval
    
    def Animating(self, dt):
        self.t += self.velocity * dt
        if self.t > 1:
            self.t = 1 
            self.kill_themself = True
        k = self.t
        alpha_value = self.Lerp(0, 255, k)
        self.graphic.TextureGetSetAlpha(alpha_value)

class FadeOut(FadeIn):
    def Animating(self, dt):
        self.t += self.velocity * dt
        if self.t > 1:
            self.t = 1 
            self.kill_themself = True
        k = 1 - self.t
        alpha_value = self.Lerp(0, 255, k)
        self.graphic.TextureGetSetAlpha(alpha_value)