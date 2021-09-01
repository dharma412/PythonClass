def divisors_prime(n):
    primenumber=True
    counter=0
    list1=[1]
    if n>1:
        for i in range(2,n+1):
            if n%i==0:
                print(i)
                counter=counter+1
                primenumber=False
                if counter!=1:
                    list1.append(str(i))
                    print("composite numbers "+ str(list1))
        if counter==1:
                print(str(n) +" is a prime number")
    '''if primenumber==False:
        for i in range(2, n + 1):
            if (n % i == 0):
                print(i,end=',')
    else:
        print(str(n) +" is a prime number")'''
n=int(input("enter the Number :"))
result=divisors_prime(n)

