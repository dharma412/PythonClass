#https://www.geeksforgeeks.org/is-python-call-by-reference-or-call-by-value/

# Python code to demonstrate
# call by reference

def add_more(list):
	list.append(50)
	print("Inside Function", list)

# Driver's code
mylist = [10,20,30,40]

add_more(mylist)
print("Outside Function:", mylist)


str1="teja"
print(id(str1))

list1=[1,2,3,4]
print(id(list1))
#2141474045056
list2=list1.append(56)
print(id(list2))