a=10 #global avriable
def display():
    global a
    a=a+1
    print(a)
(display())

def display2():
    print(a)
display2()