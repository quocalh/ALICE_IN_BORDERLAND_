import numpy as np


class CustomAnimation:
    """ 
        now there is only one animation instance, provides tons of ways to manipulate the object's motion
            no long only constraint to basic things like moving motion and fade in fade out
        we provide the t-interpolation, figure out how to interpolate by yourself (using the Lerp function)

        if done, then, destroy from inside, left with o(1) run time (shall we?)
            and will enable it back when leaving or entering the state, idk
    """
    def __init__(self, milisecond_interval: int = 1000):

        self.linear_t: float = 0

        self.time_interval: float = milisecond_interval / 1000 # stored in seconds
        self.linear_velocity: float =  1 / self.time_interval # we will run it linearly, eventually warping it with a non_linear function also run from 0 to 1 
        self.done = False

        self.t = 0

        self.smoothstep_function = None # function

        self.UpdateInterpolation_reserved = self.UpdateInterpolation

    def UpdateInterpolation(self, dt: float, smoothstep_function = None):
        if self.done == True:
            return 1
        self.linear_t += self.linear_velocity * dt

        # clamping
        self.linear_t = min(self.linear_t, 1) 
        if self.linear_t == 1:
            self.done = True

        non_linear_t = self.linear_t if (self.smoothstep_function == None) else self.smoothstep_function(self.linear_t) # remains as x if no obj smoothstep func found
        non_linear_t = self.linear_t if (smoothstep_function == None) else smoothstep_function(self.linear_t) # remains as x if no imported smoothstep func found
        self.t = non_linear_t
        print(non_linear_t)
        return non_linear_t

    @staticmethod
    def Smoothstep(x: float):
        return x
    
    @property
    def get_t(self):
        return self.t

    def Reset(self):
        self.linear_t = 0
        self.done = False

    @staticmethod
    def Lerp(a: float, b: float, t: float) -> float:
        return a * t + b * (1 - t)



class TimelineLeaves:
    def __init__(self, animation_particle: CustomAnimation, trigger_ticks: int = 1000, smoothstep_function = None): # give time in ticks
        # hard-coded items
        self.trigger_schedule: float = trigger_ticks / 1000 # after {self.trigger_schedule} amount of time, the timeline will trigger
        self.animation_particle: CustomAnimation = animation_particle

        self.activated = False
        self.trigger_momment: float = -1

        self.smoothstep_function = None
    
    def Update(self, dt: float):
        self.animation_particle.UpdateInterpolation(dt)

    def IsActivated(self, time_pointer: float):
        if self.activated == True: # always has been True
            return self.activated
        elif (time_pointer - self.trigger_schedule) > 0: # self.activated being True for the first time
            self.activated: bool =  True 
            self.trigger_momment = time_pointer
        elif (time_pointer - self.trigger_schedule - self.animation_particle.time_interval) > 0: # have done animating => deactivate em!
            # self.activated 
            print("done animating")
        else: # not yet being True
            return self.activated
    
    def Reset(self):
        self.animation_particle.Reset()
        print("not yet done")
        self.activated = False
        self.trigger_momment = -1
        

    
        

class TimeLineTree:
    """
    the object moves like the timeline, execute any programe it runs into that has past its "time-pointer"
    the bounding box hierarchy fits it best i think, but for now, just brute force through it
    think of it like a sub-tick servers 
    """
    def __init__(self, animation_particle_list: list[TimelineLeaves] = []):
        self.timeline_leaves_list: list[TimelineLeaves] = animation_particle_list
        self.time_pointer: float = 0
    
    def Update(self, dt: float):
        self.time_pointer += dt
        # print("wait")
        self.Check(dt)
    
    def Check(self, dt: float):
        # as i said before, i have no idea but brute force through the nodes
        for timeline_leaf in self.timeline_leaves_list:
            if timeline_leaf.IsActivated(self.time_pointer):
                timeline_leaf.Update(dt)
            else: 
                pass

    def Reset(self):
        for timeline_leaf in self.timeline_leaves_list:
            timeline_leaf.Reset()
        print("not done yet")



if __name__  == "__main__":
    import pygame as pg
    from pygame.locals import *
    import time

    print("hello")

    running = True
    WIDTH, HEIGHT = 800, 800
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    clock = pg.time.Clock()
    FPS = 10

    # in the real program each of them will be allocated with the corresponded graphic objects
    time_line_tree = TimeLineTree(
        [
            TimelineLeaves(CustomAnimation(1000), 3000),
            TimelineLeaves(CustomAnimation(1000), 5000),
            TimelineLeaves(CustomAnimation(2000), 7000),
        ]
    )

    previous_time = time.time()

    while running:
        dt = time.time() - previous_time
        previous_time = time.time()

        screen.fill((0, 0, 0))
        for event in pg.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        time_line_tree.Update(dt)
        
        pg.display.update()
        pg.display.set_caption(f"{clock.get_fps():.4f}")
        clock.tick(FPS)