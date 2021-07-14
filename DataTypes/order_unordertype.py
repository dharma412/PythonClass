#lists, strings and tuples are ordered collection of objects and
# sets and dictionaries are unordered collection of objects.

letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
print(set(letters))
#string_letters = tuple(letters)
#print(string_letters)

lists_letters = list(letters)
tuples_letters = tuple(letters)
sets_letters = set(letters)


#print("String: ", string_letters)
print() # for new line
print("Lists: ", lists_letters)
print() # for new line
print("Tuples: ", tuples_letters)
print() # for new line
print("Sets: ", sets_letters)

#strings, lists and tuples, they are in same order as they are specified intially

#if we look at the result of sets and dictionary, initial order, the order in which we specified the elements, is not maintained.
#So sets and dictionaries are unordered collections of objects.

list=[1,2,3,45,44,'teja',3.5]

tuple=(1,2,34,2)
for i in tuple:
    print(i,end='.')

dic1={'key':'value'}

str1="manikanta"

for i in str1:
    print(i,end='@')

# strings are immutable
# list mutable
#tuple immutable
# dic is mutable but keys are immutble  and values are mutable

#In list,tuple,string we give index and gets value
#In dictionary we give Key and gets value

# iteration through list , typle, string we use for loop.
# list , tuple, strings iterable objects.


# list has only pop method, we give index in list
# dictinary has pop and popitem, we give key in dict for pop method only and nothing for popitem.




