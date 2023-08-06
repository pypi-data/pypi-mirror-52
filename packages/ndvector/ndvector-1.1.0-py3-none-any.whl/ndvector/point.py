# -*- encoding: utf-8 -*-

# Python compatibility
from __future__ import print_function

#import from module
from .vector import Vector


class Point():
    '''
    Model a point in n dimensional space where n is a non zero positive integer
    '''

    def __init__(self, *args):
        '''
        Create from a single tuple, single list, or parameter list
        '''
        if 0 == len(args):
            raise ValueError("Point must be composed of 1 or more components")

        self.components = []
        if 1 < len(args):
            for i in range(0,len(args)):
                if type(args[i]) is float:
                    self.components.append(args[i])
                else:
                    raise ValueError("Points components must be specified as real numbers (float)")
        else: 
            if type(args[0]) is float:
                self.components.append(args[0])
            else: # be forgiving if passed a tuple or list
                for i in range(0,len(args[0])):
                    if type(args[0][i]) is float:
                        self.components.append(args[0][i])
                    else:
                        raise ValueError("Points components must be specified as real numbers (float)")


    def __getattr__(self, name):
        if 'dimension' == name:
            return len(self.components)
        else:
            raise AttributeError()


    def __setattr__(self, name, value):
        immutable = ['dimension']
        if name in immutable:
            raise NotImplementedError("'{}' can not be set directly".format(name))
        else:
            object.__setattr__(self, name, value)


    def __eq__(self, other):
        '''
        Test for equality. Return True iff parameter is a Point with the same
        dimension as self and all of the components of other are no more than
        a certain epsilon different
        '''
        if not isinstance(other, self.__class__) or self.dimension != other.dimension:
            return False

        for i in range(0, self.dimension):
            delta = abs(self.components[i] - other.components[i])
            if delta > 0.000001:
                return False

        return True


    def __add__(self, other):
        '''
        Add Vector to a Point to find Point at tip of Vector when tail of Vector is at Point
        '''
        if not isinstance(other, Vector) or self.dimension != other.dimension:
            raise ValueError("Only a Vector of the same dimension can be added")

        p = []
        for i in range(0, self.dimension):
            p.append(self.components[i] + other.components[i])
        
        return Point(p)


    def __sub__(self, other):
        '''
        Subtract Point 2 from Point 1 to find Vector from Point 1 to Point 2
        '''
        if not isinstance(other, self.__class__) or self.dimension != other.dimension:
            raise ValueError("Only Points of the same dimension can be subtracted")

        v = []
        for i in range(0, self.dimension):
            v.append(other.components[i] - self.components[i])
        
        return Vector(v)


    def __repr__(self):
        return 'Point ‹Dimension: {} Components: {}›'.format(self.dimension, str(self))


    def __str__(self):
        pieces = []
        for piece in self.components:
            pieces.append(str(piece))
        return ", ".join(pieces)
