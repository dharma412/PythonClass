# we can access the elements of string  using the index
# index must be integer can not use floate or other type which leads to typeError.

# strings are immutable i.e elements we can not changed once they have assigned ,
# we can simply reassign new string to it.
#+ve index is left to right and start from 0 to n-1
# -ve index is right to left and strat from -1 to -n

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