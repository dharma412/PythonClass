# strings are immutable i.e elements we can not changed once they have assigned ,
# we can simply reassign new string to it
# string order collection.
#conversion of character to numbers is called encoding , and the reverse process is decoding.
#ASCII and unicode or the popular encodings used.

str1="hello"
str2='hell1'
print(type(str2))

str3='''string can be write in multipe
    lines using the 
    triple quotes 
    bgyftfyhb'''
print(str3)

# we can access the elements of string  using the index
# index must be integer can not use floate or other type which leads to typeError.

# strings are immutable i.e elements we can not changed once they have assigned ,
# we can simply reassign new string to it.
#+ve index is left to right and start from 0 to n-1
# -ve index is right to left and strat from -1 to -n

mystring='This is python'

for var in mystring:
    print(var, end=',')

#print(len(mystring))
print(len(mystring[0:5]))

#print(mystring[0])
print(mystring[-6:-2])


mystring='This is python'
print(id(mystring))

mystring2='This is python2'

print(id(mystring2))
#print(mystring[6])
print(mystring[0:12:3])
print(mystring[:8])
print(id(mystring))
#mystring='u'
#mystring=[1,2,4,56]

#python string operators
# string operations

a=2
b=3
c=a+b
print(c)

a=9
b="this is pythn"
print(str(a)+b)

mystr1='This'
mystr2=' is python'
print(mystr1+mystr2)

# operator overloading addition "+"
# type casting to change object from one type to another type.

list1=[1,2,3,44]
#print(type(list1))
b=str(list1)
print(b)
print(type(b))

n=1
print("hello"+str(n))

#iteration Through a string
letter1="i am manikanta"
for i in letter1:
    print(i, end=',')

list1=[1,4,2,2,6,3,6,3,5]
for i in list1:
    if i==2:
        print("true")

print(letter1)

# find
itestring='hello ramya'
count=0
for letter in itestring:
    if letter=='a':
        count=count+1
print(count)

print(itestring, end=',')


itestring1="this is india"
for letter in itestring1:
    print(letter, end=',')

def sumofdigit(n):
    sum=0
    while n>0:
        r=n%10  #7 #9 #8
        sum=sum+r # 7 #16 # 24
        n=n//10 #89 #8 #0
    return sum

res=sumofdigit(8975456)
if res>10:
    print(sumofdigit(res))
else:
    print(res)

def palindormer():
    str222='madam'
    print(str222[::-1])

str='This is python'
print(list(enumerate(str)))

#use triple quotes to print double and single quotes in string.

print('''He said, "What's there?"''')
print('He said, "What\\ there?\"')



#Task
#1.create string and print individual elemnets separateed by '_' ex: python o/p:p_y_t_h_o_n_
#2.create string and print each elements twice and separtaed by $ ex:python o/p:pp$yy$tt$hh$oo$nn$
#note use only for and if loop

# string functions
# capitalize--It will change the first letter of string into upper case.
str1="Hello world to email academy"
print(str1.capitalize())
#if first letter of string is alredy upper case it won't change.

str1="Hello world to email academy"
# title- it will capitalise the each word of the string in given string
print(str1.title())


# count ---gives the count of given word or letter in given string.
str1=""" python is python python is best pyton is"""
print(str1.count("python"))
print(str1.count("p"))

# endswith- it will return true if string end with particual string
str1="google.com"
print(str1.endswith(".com"))
print(str1.endswith(".com1"))

#find -- it return the index of the given letter or word
str1="amuls academy"
print(str1.find('a'))
print(str1.find("am"))
print(str1.find('academy'))
print(str1.find('aca'))

# len --it return the len of the given string
str1="this is python"
print(len(str1))

# split - it return the list of words in the given string
str2="Hello,welcome,to,amuls,academy"
#b=list(str2)
#print(type(b))
b=str2.split(',')
print(b)

# lower - it will convert all letter into lower case
str1="AmuLS ACADEmY"
print(str1.islower())
str2=str1.lower()
print(str2)


# upper - it will conver all letters into upper case letter
str1="pytho is programming language"
str2=str1.upper()
print(str2)
print(str2.isupper())

#swap- it conver all lower to upper and upper to lower case
str1="hello Welcome to AMULS Academy"
print(str1.swapcase())

# replace function
str1= "hello welcome nisha"
str2=str1.replace("nisha","234")
print(str2)
str3=str2.replace("o","r")
print(str3)

# isdigit - return True if string has all digit else False
str1="123445353&34%$"
print(str1.isdigit())

str2="1233jr783hr93hf83hf"
print(str2.isdigit())

#isalpha - retunr True if string has all alphabhates letters
str1="helloiamlearningpython"
print(str1.isalpha())


# strip - removes extra characters left and right side of string
str1="!!!hello !!!!!!!!python&&&"
print(str1.strip("!"))  # strip only removes extra characters from left and right not from the middle.

str1="!!!hello !!!!!!!!python!!!!"
print(str1.lstrip('&'))

str1="!!!hello !!!!!!!!python!!!!!!"
print(str1.rstrip('!'))

dict={}
with open(r'/DataTypes/file.txt') as f:
    for i in f.readlines():
        (key,val)=i.split('=')
        dict[key]=val
print(dict)

# traslate --


# maketrans --

str1="hello guys and welcome"
dic1={"a":"1","b":"2","c":"3","d":"4"}
table=str1.maketrans(dic1)
print(table)

# maketrans with two arguments
string1="hello guys and welcome"
str1="abcde"
str2="12345"
t=string1.maketrans(str1,str2)
print(t)
t1=string1.translate(t)
print(t1)
print(t)

# maketrans with three arguments
string1="hello guys and welcome$&"
str1="abcde"
str2="12345"
str3="($&"
t=string1.maketrans(str1,str2,str3)
print(string1.translate(t))
print(t)


print(ord('u '))
print(chr(147))


# *************************** Problem **********************
# palindrome : reverse == original

str1="madam"
str2=str1[::-1]

str1='python'
print(str1[::-1])




str1='madam'
str2=""
for i in str1:
    #print(i)
    str2=i+str2
    #print(str2)
#print(str2)
if str1==str2:
    print("This is palindorme")
else:
    print("Not palindrome")




