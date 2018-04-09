#!/usr/bin/python

from miller_rabin import is_probable_prime

 
class FiniteField():
    def __init__(self, n=None):         #Finite fields must have prime-power order (power can be 1)

      #the following was removed due to miller-rabin detecting NIST primes as composite--not sure why
      #  if not float(n).is_integer():
      #      raise("Order of the field must be an integer.")
      #  R = self.getPower(n)
      #  if not is_probable_prime(R[1]):
      #      raise Exception("This field order is probably invalid. The order must be a prime power.")


        self.order = n
        self.is_finite = True


    def getPower(self, n):                              #Check every whole-number root to see if any roots are integers
        for i in range(n.bit_length()-1, 0, -1):        #this is the range of all possible whole-number roots starting form the largest and ending at 1
            if round(n**(1.0/i), 14).is_integer():      #floating point b/s requires rounding to the last float decimal--is there a better way?               
                return (i, int(round(n**(1.0/i), 14)))                
        return None                                     #Would be very strange if this ever returned None--should return 1 if no other root found   

    def getSquares(self):
        if not self.is_finite:
            raise Exception("Field is not finite.")
        squares = {};
        for i in range(0, self.order):
            if (i**2 % self.order not in squares):
                squares[i**2 % self.order] = [i, (self.order-i) % self.order]
        return squares

        

class FiniteFieldElement:
    def __init__(self, a, field):
        try:
            a = int(a)
        except:
            raise Exception("An attempt to turn " +repr(a)+ " an integer failed.")
        if not isinstance(field, FiniteField):
            raise Exception("The second argument must be a field.")
        self.val = a % field.order
        self.field = field
        
    def getPower(self, n):                              #Check every whole-number root to see if any roots are integers
        for i in range(n.bit_length()-1, 0, -1):        #this is the range of all possible whole-number roots starting form the largest and ending at 1
            if round(n**(1.0/i), 14).is_integer():      #floating point b/s requires rounding to the last float decimal--is there a better way?               
                return (i, int(round(n**(1.0/i), 14)))                
        return None                                     #Would be very strange if this ever returned None--should return 1 if no other root found   

    def __int__(self):
        if isinstance(self, FiniteFieldElement):
            return self.val
        else:
            raise Exception("This cannot be made into an integer.")

    def __add__(self, b):
        if not isinstance(b, FiniteFieldElement):
            try:
                b = FiniteFieldElement(int(b), self.order)
            except:
                raise Exception("An attempt failed to turn " +repr(b)+" into a FiniteFieldElement.")
        if self.field.order != b.field.order:
            raise Exception("Elements are not from the same field.")
        return FiniteFieldElement(self.val + int(b.val) % self.field.order, self.field)

    def __neg__(self):
        return FiniteFieldElement(self.field.order - self.val, self.field)

    def __sub__(self, b):
        return self+-b

    def __mul__(self, b):
        if not isinstance(b, FiniteFieldElement):
            try:
                b = FiniteFieldElement(int(b), self.field)
            except:
                raise Exception("An attempt failed to turn " +repr(b)+" into a FiniteFieldElement.")
        if self.field.order != b.field.order:
            raise Exception("Elements are not from the same field.")
        return FiniteFieldElement(self.val * b.val, self.field)

    def __invert__(self):
        return FiniteFieldElement(pow(self.val, self.field.order-2, self.field.order), self.field)

    def __div__(self, b):
        return self * b.__invert__()

    def __str__(self):
        return str(self.val) + " mod " + str(self.field.order)

    def __pow__(self, e):
        if type(e) != int:
            raise Exception("Exponent must be an integer.")
        return FiniteFieldElement(pow(self.val, e, self.field.order), self.field)

    def __eq__(self, b):
        if hasattr(b, 'val'):          
            return self.val % self.field.order == b.val % self.field.order and self.field.order==b.field.order
        else:
            return False

    def __repr__(self):
        return str(self.val)

        
    
