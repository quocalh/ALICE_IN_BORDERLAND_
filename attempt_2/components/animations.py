from components.UI import *

class CustomAnimation:
    """
    1 object can only be binded with 1 Custom Animation
        multiple binding can cause unexpected behaviors (weird movements) upon the binding object
    This kind of rigid animation is used for servers-client animation synchronization idk
        For client - local animation, the thing can be developed to be more sophisticate, good looking
    """
    def __init__(self, interval_duration: float):
        self.linear_t: float = 0
        
        self.interval_duration: float = interval_duration
        self.linear_velocity = 1 / interval_duration

        self.done = False

        self.t = 0
        self.smoothstep_function = None

    def UpdateInterpolation(self, dt: float, overwrite_smoothstep_function = None):
        if self.done == True:
            return 1
        self.linear_t += self.linear_velocity * dt
        self.linear_t = min(self.linear_t, 1)
        if self.linear_t == 1:
            self.done = False

        non_linear_warping_t = overwrite_smoothstep_function(self.linear_t) if overwrite_smoothstep_function != None else self.linear_t
        non_linear_warping_t = self.smoothstep_function(self.linear_t) if self.smoothstep_function != None  else self.linear_t

        self.t = non_linear_warping_t
        return non_linear_warping_t


    @staticmethod
    def Smoothstep():
        pass

    def Reset(self):
        self.linear_t = 0
        self.done = False

    @staticmethod
    def Lerp(a: float, b: float, t):
        return a * t + b * ( 1 - t)
    

class TimelineLeaf:
    def __init__(self, custom_animation: CustomAnimation, wakeup_tick: float, binding_object: Graphic, animating_function, smoothstep_function = None):
        self.wakeup_tick: float = wakeup_tick
        self.custom_animation = custom_animation
        self.smoothstep_function = smoothstep_function
        self.activated: bool = False
        self.binding_object: Graphic = binding_object
        self.animating_function = animating_function

    def UpdateInterpolation(self, dt: float) -> float:
        t = self.custom_animation.UpdateInterpolation(dt, self.smoothstep_function)
        self.animating_function(self.binding_object, t)
        return t


    def Kayaking(self, time_pointer: float):
        
        # the momment the time pointer passes over its birth (wake up tick)
        if (time_pointer - self.wakeup_tick) > 0:
            self.activated = True

        # the time pointer already passed its birth and death (useless)
        if (time_pointer - self.wakeup_tick - self.custom_animation.interval_duration) > 0:
            self.activated = False
        return self.activated
        
    def Reset(self):
        self.custom_animation.Reset()
        self.activated = False
        
class TimelineTree:
    def __init__(self, timelineleaves_list: list[TimelineLeaf]):
        self.timelineleaves_list = timelineleaves_list 
        self.time_pointer = 0

    def Tick(self, dt: float):
        self.time_pointer += dt
    
    def Update(self, dt: float):
        self.Tick(dt)
        for leaf in self.timelineleaves_list:
            if leaf.Kayaking(self.time_pointer) == True:
                leaf.UpdateInterpolation(dt)

    def Render(self, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        # for leaf in self.timelineleaves_list:
        #     try:
        #         leaf.binding_object.Draw(surface, WIDTH, HEIGHT)
        #     except:
        #         pass
        #     try:
        #         leaf.binding_object.Draw(surface)
        #     except:
        #         pass
        
        # that shit hides errors so i wont use it, this still hide but it will cause crashes - which is good
        for leaf in self.timelineleaves_list:
            try:
                leaf.binding_object.Draw(surface, WIDTH, HEIGHT)
            except:
                leaf.binding_object.Draw(surface)

        
    def UpdateAndRender(self, dt: float, surface: pg.surface.Surface, WIDTH: int = WIDTH, HEIGHT: int = HEIGHT):
        self.Tick(dt)
        for leaf in self.timelineleaves_list:
            if leaf.Kayaking(self.time_pointer) == True:
                leaf.UpdateInterpolation(dt)
            leaf.binding_object.Draw(surface, WIDTH, HEIGHT)


    def Reset(self):
        for leaf in self.timelineleaves_list:
            leaf.Reset()
        self.time_pointer = 0
    
    def get_t(self, index: int):
        return self.timelineleaves_list[index].custom_animation.t

