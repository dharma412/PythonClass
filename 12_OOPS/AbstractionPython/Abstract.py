#https://www.youtube.com/watch?v=PDMe3wgAsWg

from abc import ABC,abstractmethod

class Shape(ABC):

    @abstractmethod
    def area(self):
        pass

    @abstractmethod
    def perimeter(self):
        pass

s=Shape()
