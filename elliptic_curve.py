#!/usr/bin/python

from finite_fields import *

class EllipticCurve:
    def __init__(self, a=None, b=None, field=None):
        if field.is_finite:
            self.p = field.order
            self.a = FiniteFieldElement(a, field)
            self.b = FiniteFieldElement(b, field)
        self.field = field
        self.id = EllipticCurvePoint(float('inf'), float('inf'), self)

    def is_member(self, x, y):
        if type(x) == float and type(y) == float:
            return True
        else:
            return y**2 == x**3+self.a*x+self.b

    def list(self, length=10):
        if not self.field.is_finite:
            raise Exception("Cannot list infinite points.")
        squares = self.field.squares
        points = [EllipticCurvePoint(float('inf'), float('inf'), self)]
        for i in range(min(self.p, length)):
            y_squared = (FiniteFieldElement(i, self.field)**3 + self.a*FiniteFieldElement(i, self.field) + self.b).val
            if (squares.has_key(y_squared)):
                points.append(EllipticCurvePoint(i, squares[y_squared][0], self))
                if (y_squared != 0):
                    points.append(EllipticCurvePoint(i,squares[y_squared][1], self))
        return points

  
         

class EllipticCurvePoint:
    def __init__(self, x, y, curve):
        if type(x) == float and type(y) == float:
            self.x = float('inf')
            self.y = float('inf')
        elif not curve.is_member(FiniteFieldElement(x, curve.field), FiniteFieldElement(y, curve.field)):
            raise Exception("Coordinates are not on the curve.")
        else:
            self.x = FiniteFieldElement(x, curve.field)
            self.y = FiniteFieldElement(y, curve.field)

        self.curve = curve

    def is_id(self):
        if (isinstance(self.x, float) and isinstance(self.y, float)):
            return True

    def __add__(self, Q):
        if not isinstance(Q, EllipticCurvePoint):
            raise Exception("Both points must be EllipticCurvePoints.")
        if self.is_id():
            return Q
        elif Q.is_id():
            return self
        elif self == Q:
            return self.dbl()
        elif Q.x == self.x:
            print("farrttin")
            return self.curve.id
        else:
            s = (Q.y - self.y) / (Q.x - self.x)
            x = s**2 - self.x - Q.x
            y = -self.y-s*(x - self.x)
            return EllipticCurvePoint(x, y, self.curve)

    def copy(self):
        return EllipticCurvePoint(self.x, self.y, self.curve)
        
    def __eq__(self, Q):
        return self.__dict__ == Q.__dict__

    def dbl(self):
        if self == self.curve.id:
            return self.copy()
        elif self.y == FiniteFieldElement(0, self.curve.field): # self inverse
            return self.curve.id
        else:
            s = (FiniteFieldElement(3, self.curve.field)*self.x**2+self.curve.a) / (FiniteFieldElement(2, self.curve.field)*self.y)
            x = s**2 - FiniteFieldElement(2, self.curve.field)*self.x
            y = s*(self.x-x)-self.y
        return EllipticCurvePoint(x,y, self.curve)              


    def order(self, max=100):
        n = 1
        Pn = self
        while Pn.x != float('inf'):
            Pn += self
            n += 1
            if n > max:
               raise Exception("Maximum order exceeded.")
        return n

    def __mul__(self, n): #from that website--cite the url
        if n == 0:
            return (float('inf'), float('inf'))
        P = self.copy()
        R = self.curve.id
        i = 1    
        while i <= n:
          if i&n:
            R += P
          P += P
          i <<= 1
        return R

    def __str__(self):
        return "("+repr(self.x)+", "+repr(self.y)+")"
    def __repr__(self):
        return self.__str__()   
