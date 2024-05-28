# def make_pretty(func):
#     def inner():
#         print("I got decorated")
#         func()
#     return inner
#
# @make_pretty
# def ordinary():
#     print("I am ordinary")
#
# ordinary()
# # Output: I am ordinary
#

def smart_div(fun):
    def inner(a,b):
        print("I am going to do division")
        if b==0:
            print("division is not possible")
            return
        return fun(a,b)
    return inner
@smart_div
def div(a,b):
    print(a/b)

div(10,2)