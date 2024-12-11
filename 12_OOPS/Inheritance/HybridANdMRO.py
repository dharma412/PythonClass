class A:
    pass
class B(A):
    pass
# class C(A):pass
class D(B,A):
    pass

print(A.mro())
print(B.mro())
# print(C.mro())
print(D.mro())



# example 2

class A:pass
class B:pass
class C:pass
class X(A,B):pass
class Y(B,C):pass
class P(X,Y,C):pass
print(A.mro())#AO
print(X.mro())#XABO
print(Y.mro())#YBCO
print(P.mro())#PXAYBCO