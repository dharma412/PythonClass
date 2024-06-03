# try except finally

def divi(a,b):
    try:
        print(a/b)
    except ZeroDivisionError:
        print(" i am hadndled")
    else:
        print("I am happy no exception")
    finally:
        print("I am doing divison")
divi(10,3)

# try except
def divi(a,b):
    try:
        print(a/b)
    except ZeroDivisionError:
        print(" i am hadndled")
divi(10,0)

# try multiple except
def divi(a,b):
    try:
        print(a/b)
    except (ZeroDivisionError):
        print(" i am hadndled")
    except FileNotFoundError:
        print("I got file not found no exception")
    finally:
        print("I am doing divison")
divi(10,3)

# try except else and else. Not possible

# def divi(a,b):
#     try:
#         print(a/b)
#     except (ZeroDivisionError):
#         print(" i am hadndled")
#     else:
#         print("I am happy no exceptiono exception")
#
#     else:
#         print("I am happy no exceptiono exception")
#
#     finally:
#         print("I am doing divison")
# divi(10,3)
