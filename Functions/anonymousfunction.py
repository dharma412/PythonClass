#anonymous function is a function without name.
# anonymous function we define with lamda keyword.

# lambda arguments:expression
# lambda function can have any number of arguments but only one expression , The expression is eval and returned.
# Lambda functions can be used wherever function objects are required.

#syntax
val=lambda variable:expression

double=lambda x,y,w:x*2+y-w
print(double(5,9,2))

def double(x,y):
   return x * 2+y
print(double(5,9))

#Lambda functions are used along with built-in functions like filter(), map() etc.
# Program to filter out only the even items from a list
#The function is called with all the items in the list and a new list is returned which contains items for which the function evaluates to True.


def even(my_list):
   newlist = []
   for i in my_list:
      if (i%2)==0:
         newlist.append(i)
   print(newlist)
even([1, 5, 4, 6, 8, 11, 3, 12])

my_list = [1, 5, 4, 6, 8, 11, 3, 12]
#print(lambda x:x%2==0 , my_list)
#use filter when there is a condition
new_list = list(filter(lambda x:x%2==0 , my_list))

print(new_list)

#list comprehesnions
list=[12,4,5,67,5,3]

list1=[x*x for x in range(0,19)]
print(list1)

# lambda function with map()
# Program to double each item in a list using map()
#The map() function in Python takes in a function and a list.

#The function is called with all the items in the list and a new list is returned which contains items returned by that function for each item.

#Here is an example use of map() function to double all the items in a list.




def mul(a):
   return a*2

my_list = [1, 5, 4, 6, 8, 11, 3, 12]

for i in my_list:
   result=mul(i)
   print(result,end=' ')




my_list = [1, 5, 4, 6, 8, 11, 3, 12]
new_list = list(map(lambda x: x * 2 , my_list))

print(new_list)

# differnece between filter and map.
