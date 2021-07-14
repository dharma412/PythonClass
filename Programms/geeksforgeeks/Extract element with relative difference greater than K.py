#def method(list1,K):
'''
https://www.geeksforgeeks.org/python-extract-element-with-relative-difference-greater-than-k/

Given a list of numbers, the task is to write a Python program to extract all numbers with differences of the next and previous element with a current is greater than K.

Input : test_list = [2, 7, 4, 1, 9, 2, 3, 10, 1, 5], K = 4

Output : [9, 10]

Explanation : 9 has 1 as preceding element and 2 as succeeding. 8 and 7 are its difference respectively which are greater than 4.

'''


list1=[2, 7, 4, 1, 9, 2, 3, 10, 1, 5]
k=4
list2=[]
for i in range(0,len(list1)-1):
    if abs(list1[i]-list1[i+1])>k  and abs(list1[i]-list1[i-1])>k:
        list2.append(list1[i])
print(list2)


# usin list comprehensions
list1=[2, 7, 4, 1, 9, 2, 3, 10, 1, 5]
k=4
res=[list1[i] for i in range(len(list1)-1) if abs(list1[i]-list1[i+1])>k  and abs(list1[i]-list1[i-1])>k]
print(res)

