def divisors_prime(n):
    primenumber=True
    if n>1:
        for i in range(2,int(n/2)+1):
            if n%i==0:
                primenumber=False
                break
    if primenumber==False:
        i=1
        while i<=n:
            if n%i==0:
                print(i, end=' ')
            i=i+1
    else:
        print(str(n) +" is a prime number")
n=int(input("enter the Number :"))
result=divisors_prime(n)

