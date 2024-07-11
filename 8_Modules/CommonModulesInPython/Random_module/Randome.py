#seed
import random
random.seed(10)

#get state
import random

print(random.getstate())

#setstate
import random

#print a random number:
print(random.random())

#capture the state:
state = random.getstate()

#print another random number:
print(random.random())

#restore the state:
random.setstate(state)

#and the next random number should be the same as when you captured the state:
print(random.random())

#randrange  random.randrange(start, stop, step)

import random

print(random.randrange(3, 9))

# randint   random.randint(start, stop)
import random

print(random.randint(3, 9))

# choice
import random
mylist = ["apple", "banana", "cherry"]

print(random.choice(mylist))

# choices
import random

mylist = ["apple", "banana", "cherry"]

print(random.choices(mylist, weights = [10, 1, 1], k = 14))

# random

import random

print(random.random())

# sample
import random

mylist = ["apple", "banana", "cherry"]

print(random.sample(mylist, k=2))

#shuffle
import random

mylist = ["apple", "banana", "cherry"]
random.shuffle(mylist)

print(mylist)

# uniform Return floating value between those two number including both
import random

print(random.uniform(20, 60))

# triangular
#The triangular() method returns a random floating number between the two specified numbers (both included),
# but you can also specify a third parameter, the mode parameter.
import random

print(random.triangular(20, 60, 50))