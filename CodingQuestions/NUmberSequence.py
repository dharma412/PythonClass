#if number is even divide by 2 if odd mul by 3 and add 1 value, and print till you get 1

n=7
numseq=[n]

if n<1:
    print(" ")
while n>1:
    if n%2==0:
        n=n//2
    else:
        n=3*n+1
    numseq.append(n)

for i in numseq:
    print(i, end=' ')