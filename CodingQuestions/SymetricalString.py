def symetric(str1):

    n=len(str1)
    flag=0
    if n%2:
        mid=n//2+1
    else:
        mid=n//2
    start1=0
    start2=mid
    while(start1<mid and start2<n):
        if (str1[start1]==str1[start2]):
            start1=start1+1
            start2=start2+1
        else:
            flag=1
            break
    if flag ==0:
        print("The entered string is symmetrical")


