# anonymous function is a function without name.
# anonymous function we define with lamda keyword.

# lambda arguments:expression
# lambda function can have any number of arguments but only one expression , The expression is eval and returned.
# Lambda functions can be used wherever function objects are required.

def addone(x,y):
   print(x,y)

print(addone(5,7))

result=lambda x,y:print(x+y)
print(result(5,7))


#
list1=[1,2,3,4,5,6]
output=[1,4,9,16,25,36]

#syntax
va=lambda x:x*x
#val1=lambda x:x*x
print(va(59))

double=lambda x,y,w:x*2+y-w
print(double(5,9,2))

def double(x,y,w):
   return x*2+y-w
print(double(5,9,2))

double=lambda x=3,y=6,w=8:x*2+y-w
print(double(6,3,87))

# integrer [1,4,2,5,35,36,3]   [10,40,20,50,350,360,30]
va2=[lambda x=i: x*10 for i in [1,4,2,5,35,36,3]]

for i in va2:
   print(i())


for v in va2:
   print(v(4))

def mul(li):
   for i in li:
      print(i*10)
mul([1,24,5,353,5])




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

resul=[lambda x=i:x%2==0 for i in my_list]

for i in resul:
   print(i())

#print(lambda x:x%2==0 , my_list)
#use filter when there is a condition

my_list = [1, 5, 4, 6, 8, 11, 3, 12]
result=list(filter(lambda x:x%2==0,my_list))
print(result)

new_list = list(filter(lambda x:x%2==0 , my_list))

#based on some





print(new_list)

#list comprehesnions
list=[12,4,5,67,5,3]

list1=[x*x for x in range(0,19)]
print(list1)

# lambda function with map()
# Program to double each item in a list using map()
#The map() function takes two argumenets a function and a iterator.

#The function is called with all the items in the list and a new list is returned which contains items returned by that function for each item.

#Here is an example use of map() function to double all the items in a list.


def mul(a):
   return a*2

my_list = [1, 5, 4, 6, 8, 11, 3, 12]

for i in my_list:
   result=mul(i)
   print(result,end=' ')


list23=['python','class','version','selenium']
#conver each value in given list to upper case
#['PYTHON','CLASS','VERSION','SELENIUM']


my_list = [1, 5, 4, 6, 8, 11, 3, 12]
new_list = list(map(lambda x: x ** 2,my_list))

print(new_list)

# differnece between filter and map.
