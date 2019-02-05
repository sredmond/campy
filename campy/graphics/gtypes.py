"""
This module defines classes for representing points, dimensions, and rectangles.
"""
from collections import namedtuple as _nt

GPoint = _nt('GPoint', ['x', 'y'])
GPoint.__new__.__defaults__ = (0.0, 0.0)

GDimension = _nt('GDimension', ['width', 'height'])
GDimension.__new__.__defaults__ = (0.0, 0.0)

class GRectangle(object):
    '''
    This type contains real-valued x, y, width, and height fields. It is used to
    represent the bounding box of a graphical object
    '''
    def __init__(self, x=0.0, y=0.0, width=0.0, height=0.0):
        '''
        Initializes a GRectangle object with the specified fields. If these
        parameters are not supplied hte default values are set to 0.0

        @type x: float
        @param x: x coordinate of upper left corner
        @type y: float
        @param y: y coordinate of upper left corner
        @type width: float
        @param width: width of rectangle
        @type height: float
        @param height: height of rectangle
        @rtype: void
        '''
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def is_empty(self):
        '''
        Returns if the rectangle is empty.

        @rtype: boolean
        '''
        return self.width <= 0 or self.height <= 0

    def __contains__(self, point):
        '''
        Returns true if the rectangle contains the given point, which may be
        specified either as a GPoint or distinct coordinates

        @type pt: GPoint
        @param pt: GPoint to check, will override x and y
        @type x: float
        @param x: x coordinate of point to check
        @type y: float
        @param y: y coordinate of point to check
        @rtype: boolean
        '''
        x, y = point
        return self.x <= x <= self.x + self.width and \
               self.y <= y <= self.y + self.height

if __name__ == '__main__':
    print("Testing gtypes.py")
    print("--------------------------------------------------")

    print("Create GPoint default values")
    gp1 = GPoint()
    x = gp1.x
    y = gp1.y
    tostring = str(gp1)
    gp2 = GPoint()
    eq = (gp1 == gp2)
    ne = (gp1 != gp2)
    if(x != 0.0 or y != 0.0 or tostring != "GPoint(x=0.0, y=0.0)" or eq != True or ne != False):
        print("FAILED")
    print("PASSED")

    print("Create GPoint non-default values")
    gp1 = GPoint(5, -2.5)
    x = gp1.x
    y = gp1.y
    tostring = str(gp1)
    gp2 = GPoint(5, -2.5)
    eq = (gp1 == gp2)
    ne = (gp1 != gp2)
    if(x != 5.0 or y != -2.5 or tostring != "GPoint(x=5, y=-2.5)" or eq != True or ne != False):
        print("FAILED")
    print("PASSED")
    print

