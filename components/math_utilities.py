import numba as nb
import numpy as np
# from numba import 
from numba.experimental import jitclass
import pygame as pg



PointSpecification = [
    ("x", nb.float64),
    ("y", nb.float64),
    ("array", nb.float64[:]),
]
@jitclass(PointSpecification)
class PointsNB:
    # x: float
    # y: float
    def __init__(self, x, y):
        self.x: float = x
        self.y: float = y
        self.array: np.ndarray = np.array((x, y), dtype = np.float64)


# Points_type = nb.deferred_type()
# print(Points_type.define(Points.class_type.instance_type))
# does not needed but alr
# here is a link: https://github.com/numba/numba/blob/deb27e3a08665af7c70d0ddfd62814bdf0af51f5/examples/linkedlist.py#L38


SegmentSpecification = [
    ("p1", PointsNB.class_type.instance_type),
    ("p2", PointsNB.class_type.instance_type),
    ("vector12", nb.float64[:]),
]
@jitclass(SegmentSpecification)
class SegmentsNB:
    def __init__(self, P1, P2):
        self.p1 = P1
        self.p2 = P2
        print("hello human")
        self.vector12 = self.p2.array - self.p1.array
    def SegmentSegmentIntersection(this, that: PointsNB):
        """
        THIS IS RELATIVELY EASY TO PROVE (just isolate the parameter(t and t') and that is it !), 
        THE DETERMINANT ANNOTATION USED IN THE FORMULA LOOKS DAUNTING AS FUCK NOT GONNA LIE
        """
        # check segment of (x1, y1) and (x2, y2) intersects with one (x3, y3) and (x4, y4)
        x1, x2, x3, x4 = this.p1.x, this.p2.x, that.p1.x, that.p2.x
        y1, y2, y3, y4 = this.p1.y, this.p2.y, that.p2.y, that.p2.y

        t_numerator = (x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        t = t_numerator / denominator

        if not (0 <= t <= 1):
            return None
        return this.p1.array + this.vector12 * t

class Points:
    def __init__(self, x: float, y: float):
        self.point = PointsNB(x, y)
    
    def Draw(self, surface: pg.surface.Surface):
        pg.draw.circle(surface, (255, 255, 255), self.point.array.tolist(), 10)

class Segments:
    def __init__(self, P1: Points, P2: Points):
        pass

point1 = PointsNB(5, 5)
point2 = PointsNB(6, 6)
print(point1.x, "done creating points")
segment = SegmentsNB(point1, point2)
print(segment.p1.x, "done creating segments")
print("god-complex creature :smirk:")
# print(segment)

    