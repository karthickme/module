from math import sqrt, acos, pi
from decimal import Decimal, getcontext

# Need to fix bugs related to Decimal conversion lot of decimal and float multiplication issues 


getcontext().prec = 30

class Vector(object):
    
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = "Cannot normalize the zero vector"
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = "No uniqie ortho"
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = "No uniqiei para"
    ONLY_DEFINED_TWO_THREE_DIMENSTION_MATRIX = "Defined two, 2 Dimentions matrix please"
    
    
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([x for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def add(self, v):
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
        
    def minus(self, v):
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
        
    def times_scalar(self, c):
        new_coordinates = [c*x for x in self.coordinates]
        return Vector(new_coordinates)
    
    def magnitude(self):
        square = sum([x*x for x in self.coordinates])
        return sqrt(square)
        
    def normalized(self):
        try:
            return self.times_scalar(1/self.magnitude())
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
            
    def dot(self, v):
        prodsum = sum([x*y for x,y in zip(self.coordinates,v.coordinates)])
        return prodsum
        
    def anglerad(self,v,in_degrees=False):
        try:
            if in_degrees==False:
                return acos(self.dot(v)/(self.magnitude()*v.magnitude()))
            else:
                return acos(self.dot(v)/(self.magnitude()*v.magnitude()))*180.0/pi
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception("Cannot compute angle for with 0 Vector")
            else:
                raise e
    
    def is_parallel_to(self,v):
        return (self.is_zero() or v.is_zero() or self.anglerad(v)==0 or self.anglerad(v)==pi)

    def is_zero(self, tolerance=1e-10):
        return self.magnitude()<tolerance

    def is_orthogonal_to(self, v, tolerance=1e-10):
        return abs(self.dot(v)) < tolerance

    # def projection(self,v, tolerance = 1e-10):
    #     vnom = v.normalize()
    #     print(vnom)
    #     return self.dot(v.normalize())

    def component_orthogonal_to(self, basis):
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e

    def component_parallel_to(self, basis):
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def cross(self, v):
        try:
            x1,y1,z1= self.coordinates
            x2,y2,z2= v.coordinates
            new_coordinates = [y1*z2 - y2*z1 , -( x1*z2 - x2*z1 ), x1*y2 - x2*y1]
            return Vector(new_coordinates)
        except ValueError as e:
            msg = str(e)
            if msg == "need more than 2 values to unpack":
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(v.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif msg == "too many values to unpack" or msg == "need more than 1 value to unpack":
                raise Exception(self.ONLY_DEFINED_TWO_THREE_DIMENSTION_MATRIX)
            else:
                raise e

    def area_of_trainge_with(self, v):
        return self.area_of_parallelogram_with(v) / Decimal('2.0')
    
    def area_of_parallelogram_with(self, v):
        cross_prod = self.cross(v)
        return cross_prod.magnitude()