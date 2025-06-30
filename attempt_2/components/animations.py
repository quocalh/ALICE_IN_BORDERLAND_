




class CustomAnimation:
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
    def __init__(self, custom_animation: CustomAnimation, wakeup_tick: float, smoothstep_function = None):
        self.wakeup_tick: float = wakeup_tick
        self.custom_animation = custom_animation
        self.smoothstep_function = smoothstep_function

    def UpdateInterpolation(self, dt: float) -> float:
        return self.custom_animation.UpdateInterpolation(dt, self.smoothstep_function)

    def Kayaking(self, time_pointer: float):
        if (time_pointer - self.wakeup_tick) > 0:
            self.activated = True
        if (time_pointer - self.wakeup_tick - self.custom_animation.interval_duration) > 0:
            print("done animating ...")
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
            if leaf.Kayaking(self.time_pointer):
                leaf.UpdateInterpolation(dt)

    def Reset(self):
        for leaf in self.timelineleaves_list:
            leaf.Reset()
        self.time_pointer = 0

