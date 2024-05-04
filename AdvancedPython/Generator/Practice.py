def gen(a):

    yield a

    a=a+1
    yield a

genob=gen(5)
print(next(genob))
print(next(genob))
print(next(genob))