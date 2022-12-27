def pattern(n):
    for i in range(n):
        for j in range(i+1):
            print("* ",end="")
        print("\r")


n=5
pattern(n)


n=5;i=0
while(i<=n):
  print(" " * (n - i) +"*" * i)
  i+=1

n=5;i=1
while(i<=n):
  #print(" " * (n - i) +"*" * i)
  print(i*"*"+" "*(n-i))
  i+=1