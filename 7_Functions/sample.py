
c=10

def outter():
    m=10
    d=10
    global c
    print(c+1)

    def inner():
        global c
        print(c+1)
        nonlocal  m  # to modify  the nonlocal variable we need to use nonlocal keyword explicitly
        m=m+1
        print(m)
    inner()

outter()
