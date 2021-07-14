'''

https://www.geeksforgeeks.org/python-program-to-test-if-all-elements-in-list-are-maximum-of-k-apart/

Given a list of numbers, the task is to write a Python program to test if all elements are maximum of K apart.

Examples:

Input : test_list = [475, 503, 425, 520, 470, 500], K = 100

Output : True

Explanation : Maximum element is 520 and minimum is 425, 520-425 = 95, which is less than 100, hence elements are in range.
'''

test_list = [475, 503, 425, 540, 470, 500]
k = 100

res=max(test_list)-min(test_list)<k
print(res)
