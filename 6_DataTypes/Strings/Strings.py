# strings are immutable i.e elements we can not changed once they have assigned ,
# we can simply reassign new string to it
# string order collection.
#conversion of character to numbers is called encoding , and the reverse process is decoding.
#ASCII and unicode or the popular encodings used.
import codecs

str1="This is p'ython"
print((str1))

str1='This is p"ython'
print((str1))

str1="This is p\"ython"
print(str1)

str1='This is p\"ython'
print('This is p\"ython')

str1="This is p\'ython"
print(str1)

str1='''He said, "What's there?"'''
print(str1)

str2="either sine"
str1="either sune"
print(str1==str2)




str1="This is p'ython"
print((str1))

str1='This is p"ython'
print((str1))

str1="This is p\"ython"
print(str1)

str1='This is p\"ython'
print('This is p\"ython')

str1="This is p\'ython"
print(str1)

str1='''He said, "What's there?"'''
print(str1)

str2="either sine"
str1="either sune"
print(str1==str2)




list1=[1,2,3,4,5,56,4]
print(list1[0])
str1="!!!!!!!!hello hellohe sdsdudcdhcuSDFDFFFR!!!!!!!!"
#print(str1.lstrip('!'))
print(str1.swapcase())
print(str1.index('h'))
print(str1.count('h'))
print(str1.title())
print(str1.capitalize())
print(str1.upper())
out=str1.split(" ")
print(out)
print(" ".join(out))
str2='hello'
print(type(str2))

str3='''string 46436 can be write in multipe
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


# string methods

# string methods start from here

# capitalize--It will change the first letter of string into upper case.
str1="ello world to email academy"
result=str1.capitalize()
print(result)

#if first letter of string is alredy upper case it won't change.

str1="Hello world to email academy"
# title- it will capitalise the each word of the string.
result1=str1.title()
print(result1)


# count ---gives the count of given word or letter in given string.
str1=""" python is python python is best pyton is"""
count1=str1.count("python")
print(count1)
count2=(str1.count("p"))
print(count2)

# endswith- it will return true if string end with particual string
str1=".com.googlem"
# result=str1.endswith("lem")
# print(result)
result=str1.endswith(".com1")
print(result)

#find -- it return the index of the given letter or word,it returns -1 if word or char is not presentin string
str1="amuls acdemy"

# result=str1.find('a',3)
# print(result)

result=str1.find('z',3,9)
print(result)

# print(str1.find('a'))
# print(str1.find("am"))
print(str1.find('acdemy'))
# print(str1.find('aca'))

# len --it return the len of the given string function
str1="this is python"
lenth=len(str1)
list1=[1,2,3,4,5,6,7,7]
lenth1=len(list1)
print(lenth1)

# split - it return the list of words in the given string
str2="Hello " \
     "welcome to " \
     "amuls academy"
b=str2.split(' ')
print(b)

str2="this is python"
#b=list(str2)
#print(type(b))
b=str2.split(' ')
print(b)
result=" ".join(b)
print(result)


#join --- it joines the given data with some seprator

list1=['this','is','python']
# this is python
str1=","
result=str1.join(list1)
print(result)

# lower - it will convert all letter into lower case
str1="AmuLS ACADEmY"
result=str1.lower()
print(result)






# upper - it will conver all letters into upper case letter
str1="pytho is progMMMMamming language"
str2=str1.upper()
print(str2)



#swap- it conver all lower to upper and upper to lower case
str1="hello Welcome to AMULS Academy"
result=str1.swapcase()
print(result)

# replace --- it replace given string with existing values
str1= "hello welcome nishaoo"
str2=str1.replace('o','z')
print(str2)




# format--
str1="Hello {name} world 2 {name3}"
result=str1.format(name2=2,name3=4,name="taja")



# format--
str1="Hello {name} world 2 {name2}"
result=str1.format(name2=2,name="teja")
print(result)

#Formatting string using % Operator

str1="This is python %s and I am paying for %s and cost is %d"%("class","class",25000)
print(str1)

#floating precision precesion
result=3.141592
print(result)
print("%5.9f" %(result))

# using format() method

str2="{1} {2} {0}".format("Teja0","leela2","raja1")
print(str2)

str2="{a} {b} {c}".format(a=65,b="leela",c="raja")
print(str2)

#{[index]:[width][.precision][type]}
var ="class"
str4=f"This is python {var}"
print(str4)

# strip - removes extra characters left and right side of string
str1="   hello !!!!!!!!python&&&  "
print(str1)
result=str1.strip(" ") # strip only removes extra characters from left and right not from the middle.
print(result)

str1="!!!hello !!!!!!!!python!!!!"
result=str1.lstrip("!")
print(result)


str1="!!!hello !!!!!!!!python!!!!!!"
result=str1.rstrip('!')
print(result)

#casefold- it converts all charecters into lower case
#both lower and cascade lower the given string , however , they gives different results when delaing with strings from other languages.

str1="STRAßE"
print(str1.casefold())
print(str1.lower()) #ascii


#center  - method will center align the string using specified character , space is default

str1="g"
result=str1.center(7,'O')
print((result))

#isalnum---
str1="version32455rfsdf"
result=str1.isalnum()
print(result)

# isdigit - return True if string has all digit else False
str1="123445353&34%$"
result=str1.isdigit()
print(result)

#isalpha - retunr True if string has all alphabhates letters
str1="helloiamlearningpython"
result=str1.isalpha()
print(result)

#isnumeric--- check if all characters in string are numaric
str1="576778.88"
result=str1.isnumeric()
print(result)

#istitile --- check if given string in title formate
str1="HEllo And Welcome"
result=str1.istitle()
print(result)

#islower - it will check string in lower caseornot
str1="AmuLS ACADEmY"
result=str1.islower()
print(result)

#isupper -  it will check string in upper case or not
str1="ACADE"
result=str1.isupper()
print(result)

#isspace --- check if all charecters in the strign are whitespaces
str1="66868    979"
result=str1.isspace()
print(result)

#isidentifier----  check if the strign is identifier or variables
str1="22Demo343"
result=str1.isidentifier()

print(result)

#Formatting string using % Operator

str1="This is python %s and I am paying for %s and cost is %d"%("class","class",25000)
print(str1)

#floating precision precesion
result=3.141592
print(result)
print("%5.9f" %(result))

# using format() method

str2="{1} {2} {0}".format("Teja","leela","raja")
print(str2)

str2="{a} {b} {c}".format(a=65,b="leela",c="raja")
print(str2)

#{[index]:[width][.precision][type]}
var ="class"
str4=f"This is python {var}"

print(str4)


# strip - removes extra characters left and right side of string
str1="!!!hello !!!!!!!!python&&&"
result=str1.strip("!") # strip only removes extra characters from left and right not from the middle.

str1="!!!hello !!!!!!!!python!!!!"
result=str1.lstrip('&')

str1="!!!hello !!!!!!!!python!!!!!!"
result=str1.rstrip('!')


#casefold-

str1="helloiamlDFGDGDGearningpython"
result=str1.casefold()
print(result)

#center  - method will center align the string using specified character , space is default

str1="g"
result=str1.center(30,'O')
print((result))

#isalnum---
str1="version32455rfsdf"
result=str1.isalnum()
print(result)

# isdigit - return True if string has all digit else False
str1="123445353&34%$"
result=str1.isdigit()
print(result)

#isalpha - retunr True if string has all alphabhates letters
str1="helloiamlearningpython"
result=str1.isalpha()
print(result)

#isnumeric--- check if all characters in string are numaric
str1="576778.88"
result=str1.isnumeric()
print(result)

#istitile --- check if given string in title formate
str1="HEllo And Welcome"
result=str1.istitle()
print(result)

#islower - it will check string in lower caseornot
str1="AmuLS ACADEmY"
result=str1.islower()
print(result)

#isupper -  it will check string in upper case or not
str1="ACADE"
result=str1.isupper()
print(result)

#isspace --- check if all charecters in the strign are whitespaces
str1="66868    979"
result=str1.isspace()
print(result)

#isidentifier----  check if the strign is identifier
str1="Demo343"
result=str1.isidentifier()
print(result)


#splitlines --
str1='This is python  this is python\n     jsdadcsdjsd ncjdhjd\n     wdhasjkdhjk jdhjs'
result=str1.splitlines()
print(result)
#reverse method---- it retunrs the given string.


#splitlines --
str1='This is python  this is python\n    jsdadcsdjsd ncjdhjd\n  wdhasjkdhjk jdhjs'
print(str1)

result=str1.splitlines()
print(result)
#reverse method---- it retunrs the given string.


#Encode
# str1='This is python  this is python'
# result=str1.encode('ASCII')
# result.decode()



str1="H\te\tl\tl\to"
print(str1)
print(str1.expandtabs(2))


str1.format_map()
str1.partition()
str1.ljust()
str1.isprintable()
str1.zfill()
str1.removeprefix()
str1.removesuffix()
str1.startswith()
str1.rindex()
str1.rfind()
str1.rjust()



# traslate --

# maketrans --

str1=""
dic1={"a":"1","b":"2","c":"3","d":"4"}
table=str1.maketrans(dic1)
print(table)

# maketrans with two arguments
string1=""
str1="abcde"
str2="12345"
t=string1.maketrans(str1,str2)
print(t)
str2="aeiuou"
t1=str2.translate(t)
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
# madam = madam --
#malayalam  = malayalam
#reverse the given string
str1="helloworld"
result=str1[::-1]
print(result)

str2=""
for var in str1:
    str2=var+str2  #e+h=eh=olleh
print(str2)



# find if string is palindrome or not

str1="madam"
str2=str1[::-1]

str1='python'
print(str1[::-1])

print(ord('*'))
print(chr(42))


dict={}
with open(r'/6_DataTypes/file.txt') as f:
    for i in f.readlines():
        (key,val)=i.split('=')
        dict[key]=val
print(dict)



str2='''aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\
bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb\
ccccccccccccccccccccccccccccccccccc\
ddddddddddddddddddddddddddddddddddd'''
print(str2)
print(str2.splitlines())


print(34<<5)

print((3*6+18//3+18%3+18/4+4**5*10&2))
