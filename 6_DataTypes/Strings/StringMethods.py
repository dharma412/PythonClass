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
result=str1.endswith("lem")
print(result)

#find -- it return the index of the given letter or word,it returns -1 if word or char is not presentin string
str1="amuls acdemy"

# result=str1.find('a',3)
# print(result)

result=str1.find('e',4,10)
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


#splitlines --
str1='This is python  this is python\n     jsdadcsdjsd ncjdhjd\n     wdhasjkdhjk jdhjs'
result=str1.splitlines()
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

str1="5850"
str1="785585"
print(str1)



# format--
str1="Hello {name} world 2 {name3}"
result=str1.format(name3=4,name="teja")
print(result)


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
d=" "
str4=f"This is {d} {var}"
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
result=str1.center(10,'*')
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
str1="helloiamlearning44545python"
result=str1.isalpha()
print(result)

#isnumeric--- check if all characters in string are numaric
str1="576778.88"
result=str1.isnumeric()
print(result)

#istitile --- check if given string in title formate
str1="Hello And Welcome"
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
str1=" gfhfg "
result=str1.isspace()
print(result)

#isidentifier----  check if the strign is identifier or variables
str1="22Demo343"
result=str1.isidentifier()
print(result)


# maketrans and traslate --
str1=""
dic1={"a":"1","b":"2","c":"3","d":"4"}
table=str1.maketrans(dic1)
print(table)

# maketrans with two arguments
string1=""
str1="abcde"
str2="12348"
t=string1.maketrans(str1,str2)
print(t)
str2="aeiuou"
t1=str2.translate(t)
print(t1)


# maketrans with three arguments
string1="hello guys and welcome$&123"
str1="abcde"
str2="12345"
str3="($&(*"
t=string1.maketrans(str1,str2,str3)
print(string1.translate(t))
print(t)


# More Methods
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
str1.expandtabs