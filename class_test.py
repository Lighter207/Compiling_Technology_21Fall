import math

class Complex:
    '''A simple class of complex numbers'''
    kind = 'complex number' # class variable shared by all instances
    def __init__(self,realpart,imgpart):
        self.r = realpart # instance variable unique to each instance
        self.i = imgpart # instance variable unique to each instance
    
    def mod(self):
        mod = math.sqrt(pow(self.r,2)+pow(self.i,2)) 
        return (mod)

    def display(self):
        return f"Complex number is {self.r}+{self.i}i."


x = Complex(2,3)
print(x.__doc__) #prints out the doc string of Complex class

#To access the class attributes
print(x.r,x.i)
#class attributes can be changed
x.r = 4


#To call a method
print(x.mod())

#You can call a method object without the "()" and call it later
display = x.display
print(display())