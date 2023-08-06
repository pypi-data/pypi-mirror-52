# -*- encoding: utf-8 -*-

# Import from Python Standard Library
from math import acos, sqrt

class Vector():
    '''
    Model a vector of dimension n in a cartesian system
    '''

    def __init__(self, *args):
        '''
        Create from a single tuple, single list, or parameter list
        '''
        if 0 == len(args):
            raise ValueError("Vectors must be composed of 1 or more components")

        self.components = []
        if 1 < len(args):
            for i in range(0,len(args)):
                if type(args[i]) is float:
                    self.components.append(args[i])
                else:
                    raise ValueError("Vector components must be specified as real numbers (float)")
        else: 
            if type(args[0]) is float:
                self.components.append(args[0])
            else: # be forgiving if passed a tuple or list
                for i in range(0,len(args[0])):
                    if type(args[0][i]) is float:
                        self.components.append(args[0][i])
                    else:
                        raise ValueError("Vector components must be specified as real numbers (float)")


    def __getattr__(self, name):
        if 'dimension' == name:
            return len(self.components)
        elif 'magnitude':
            # lazy calculation
            sum = 0
            for c in self.components:
                sum += c**2
            
            magnitude = sqrt(sum)
            object.__setattr__(self, 'magnitude', magnitude)
            return self.magnitude
        else:
            raise AttributeError()


    def __setattr__(self, name, value):
        immutable = ['dimension', 'magnitude']
        if name in immutable:
            raise NotImplementedError("'{}' can not be set directly".format(name))
        else:
            object.__setattr__(self, name, value)


    def __eq__(self, other):
        if not isinstance(other, self.__class__) or self.dimension != other.dimension:
            return False

        for i in range(0, self.dimension):
            delta = abs(self.components[i] - other.components[i])
            if delta > 0.000001:
                return False

        return True


    def __add__(self, other):
        '''
        Add a Vector to this Vector
        '''
        if not isinstance(other, self.__class__) or self.dimension != other.dimension:
            raise ValueError("Only Vectors of the same dimension can be added")

        v = []
        for i in range(0, self.dimension):
            v.append(self.components[i] + other.components[i])
        
        return Vector(v)


    def __sub__(self, other):
        '''
        Subtract a Vector from this Vector
        '''
        if not isinstance(other, self.__class__) or self.dimension != other.dimension:
            raise ValueError("Only Vectors of the same dimension can be added")

        v = []
        for i in range(0, self.dimension):
            v.append(self.components[i] - other.components[i])
        
        return Vector(v)


    def __mul__(self, other):
        '''
        Scale this vector by a scalar or find the scalar aka dot product of
        this vector with another.
        '''
        if type(other) is float:
            v = []
            for i in range(0, self.dimension):
                v.append(self.components[i] * other)

            return Vector(v)
        else:
            if not isinstance(other, self.__class__) or self.dimension != other.dimension:
                raise ValueError("Only Vectors of the same dimension can be multiplied")

            product = 0.0
            for i in range(0, self.dimension):
                product += self.components[i] * other.components[i]

            return product


    def __matmul__(self, other):
        '''
        Find the vector aka cross product of this vector with another
        '''
        if not isinstance(other, self.__class__) or self.dimension != 3 or other.dimension != 3:
            raise ValueError("Only Vectors of dimension three(3) can be multiplied")

        i = self.components[1] * other.components[2] - self.components[2] * other.components[1]
        j = self.components[2] * other.components[0] - self.components[0] * other.components[2]
        k = self.components[0] * other.components[1] - self.components[1] * other.components[0]

        return Vector(i,j,k)


    def angle(self, other):
        '''
        Find the angle in radians between this vector and another should their
        tails originate from a common point.
        '''
        if not isinstance(other, self.__class__) or self.dimension != other.dimension:
            raise ValueError("Only Vectors of the same dimension can be added")

        scalar_product = self * other
        magnitude_product = self.magnitude * other.magnitude

        return acos(scalar_product / magnitude_product)


    def normalize(self):
        '''
        Find a unit vector is the same direction as this vector
        '''
        v = []
        for i in range(0, self.dimension):
            v.append(self.components[i] / self.magnitude)
        
        return Vector(v)


    def __repr__(self):
        return 'Vector ‹Dimension: {} Components: {}›'.format(self.dimension, str(self))


    def __str__(self):
        pieces = []
        for piece in self.components:
            pieces.append(str(piece))
        return ", ".join(pieces)
