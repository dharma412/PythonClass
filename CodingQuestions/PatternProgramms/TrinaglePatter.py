n=6
k=n-1
for i in range(0,n):
    for m in range(0,k):
        print(end=" ")
    k=k-1
    for j in range(0,i+1):

        print("* ", end="")

    print("\r")

print(end=" ")