# all iterator is object thta contains the number of values.

#  list, tuple, string etc. are iterables.
# ithe iter function (whihc internallu calles __iter__() method) retunrs an iterator from them.
# if iterator must implememt two methods __next__ and __iter__().

# iterating throguh the itrable

list=[34,5,24,53,256,2663,98]

myiter=iter(list)
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(next(myiter))
print(myiter.__next__())# next(iterator) and iterator.__next__() both are same.
print(myiter.__next__())
print(myiter.__next__())
print(myiter.__next__()) # raise error stopIteration.


#building custome iterators.
class powerofTwo:
    def __init__(self,max):
        self.max=max
    def __iter__(self):
        self.n=0
        return self
    def __next__(self):
        if self.n<=self.max:
            result=2**self.n
            self.n +=1
            return result
        else:
            raise StopIteration
num=powerofTwo(9)
i=iter(num)
print(next(i))
print(next(i))
print(next(i))
print(next(i))
print(next(i))