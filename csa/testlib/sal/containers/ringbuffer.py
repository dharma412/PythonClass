"""A container object with a fixed size.

From ASPN:

Title: Ring buffer
Submitter: Sebastien Keim
Last Updated: 2001/09/24
Version no: 1.1
Category: Algorithms

Description:
A ring buffer is a buffer with a fixed size. When it fills up, adding another element overwrites the first. It's particularly useful for the storage of log information. There is no direct support in Python for this kind of structure but it's easy to construct one.

Here is a suggestion of implementation optimized for element insertion.

Discussion:
This recipe use class dynamic setting. This allows to have different implementations for the same interface and to select which one to use, according to object state.
This may not work with new classes of Python 2.2 (eg classes derived from built-in types).

http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/68429

>>> x=RingBuffer(5)
>>> x.append(1); x.append(2); x.append(3); x.append(4)
>>> print x.__class__,x.get()
sal.containers.ringbuffer.RingBuffer [1, 2, 3, 4]
>>> x.append(5)
>>> print x.__class__,x.get()
sal.containers.ringbuffer.RingBufferFull [1, 2, 3, 4, 5]
>>> x.append(6)
>>> print x.data,x.get()
[6, 2, 3, 4, 5] [2, 3, 4, 5, 6]
>>> x.append(7); x.append(8); x.append(9); x.append(10)
>>> print x.data,x.get()
[6, 7, 8, 9, 10] [6, 7, 8, 9, 10]
"""
from __future__ import absolute_import


#: Reference Symbols: ringbuffer

class RingBuffer:
    """A container object with a fixed size.
    """

    def __init__(self, size_max):
        self.max = size_max
        self.data = []

    def append(self, x):
        """append an element(x) at the end of the buffer
        Return: None """
        self.data.append(x)
        if len(self.data) == self.max:
            self.cur = 0
            self.__class__ = RingBufferFull

    def get(self):
        """ return a list of elements from the oldest to the newest"""
        return self.data


class RingBufferFull:
    def __init__(self, n):
        raise "Do not call this class directly. You should use RingBuffer"

    def append(self, x):
        self.data[self.cur] = x
        self.cur = (self.cur + 1) % self.max

    def get(self):
        return self.data[self.cur:] + self.data[:self.cur]
